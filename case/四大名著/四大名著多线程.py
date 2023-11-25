import os.path
import re
import time
import random
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


def get_html(url):
	"""
	获取页面的源代码, 将之处理为etree对象返回
	:param url: 传递进来的地址
	:return: 网页etree对象
	"""
	resp = requests.get(url, headers=headers)
	time.sleep(random.randint(1, 3))
	html = etree.HTML(resp.content.decode())
	return html


def get_book_info(html):
	"""
	获取书本的名称和书的url
	:param html: 页面源码生成的etree对象
	:return: 将书的信息返回 {'三国演义':'http://....'}
	"""
	book_list = html.xpath('//div[@class="card bookmark-list"]//div[@class="book-item"]')
	book_info = {}
	for book in book_list:
		book_name = book.xpath('./h3/a/text()')[0]
		book_url = 'https://www.shicimingju.com' + book.xpath('./h3/a/@href')[0]
		book_info[book_name] = book_url

	return book_info


def get_book_mulu(book_url):
	"""
	获取章节名称章节的url
	:param book_url: 书的url
	:return: 每本书的章节和章节url    {'第一回.....': 'http:// ....'}
	"""
	book_mulus = get_html(book_url).xpath('//div[@class="book-mulu"]/ul/li')
	chapter_info = {}
	for mulu in book_mulus:
		title = mulu.xpath('./a/text()')[0]
		chapter_url = 'https://www.shicimingju.com' + mulu.xpath('./a/@href')[0]
		chapter_info[title] = chapter_url
	return chapter_info


def get_content(book_mulus):
	"""
	获取章节的内容
	:param book_mulus: 书的目录名和链接
	:return: 返回每一章的章节名和内容 {'第一回....': '章节的内容'}
	"""
	book_text = {}
	# 循环抓取每一章的内容
	for section in book_mulus:
		content = get_html(book_mulus[section]).xpath('//div[@class="chapter_content"]/text()')
		text_list = []
		# 将抓取到的内容进行处理, 将'\u3000'空格去除
		for txt in content:
			txt = str(txt).strip()
			text = re.sub(r'\s+', '\n', txt, re.S)
			text_list.append(text)
		book_text[section] = text_list
		print('获取内容+1')
	return book_text


def save_txt(path, book_content):
	"""
	将获取到的内容存储到文件内
	:param path: 存储的文件夹名
	:param book_content: 抓取到的书本内容
	:return:
	"""
	# 判断文件是否存在, 如果不存在则创建文件夹
	if not os.path.exists(path):
		os.mkdir(path)
	# 循环书的每一章节, 将每一章节写入到文件内.
	for book in book_content:
		with open(os.path.join(path, book + '.txt'), 'w', encoding='utf-8') as f:
			f.write('\n'.join(book_content[book]))
		print(book)
		print(f'{book}章节写入完成')


def process_book(book_name, book_url):
	print(f'{book_name}开始获取目录')
	book_mulus = get_book_mulu(book_url)
	print('目录获取完成')
	print('开始获取内容')
	book_content = get_content(book_mulus)
	print('内容获取完成')
	print(f'文件名: {book_name}')
	path = book_name
	print('开始保存数据')
	save_txt(path, book_content)
	print(f'{book_name}写入完成')


def main(url):
	print('开始获取书籍信息')
	book_info = get_book_info(get_html(url))
	print('获取书籍信息完成')

	with ThreadPoolExecutor(100) as pool:  # 增加线程池数量，根据需求调整
		# 提交每本书的抓取任务到线程池
		for book_name, book_url in book_info.items():
			pool.submit(process_book, book_name, book_url)


if __name__ == '__main__':
	t1 = time.time()
	url = 'https://www.shicimingju.com/bookmark/sidamingzhu.html'
	main(url)
	print(f'用时: {time.time() - t1}')