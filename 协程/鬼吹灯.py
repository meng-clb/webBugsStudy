import requests
import aiohttp
from lxml import etree
import os

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'https://www.51shucheng.net/daomu/guichuideng'


def get_book_url(url):
	"""
	获取book每个章节的链接
	:param url: 目录页的url
	:return: 章节链接列表
	"""
	resp = requests.get(url)
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	# 获取章节链接
	section_urls = html.xpath('//div[@class="mulu-list quanji"]/ul/li/a/@href')
	return section_urls


def get_section_info(section_url):
	"""
	获取到章节的所有信息, 存储在字典内
	:param section_url: 章节的url
	:return: 存储章节信息的字典
	"""
	book = {}
	# 处理抓取到的数据存储位置
	book_name = str(section_url).rsplit('/', 2)[-2]
	book['location'] = book_name

	resp = requests.get(section_url)
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	# 章节名称
	section_title = str(html.xpath('//h1/text()')[0]).strip().replace(':', '_')
	# 章节内容
	section_con = '\n\n'.join(html.xpath('//div[@class="neirong"]/p/text()'))
	book['title'] = section_title
	book['content'] = section_con
	return book


def download_section(book):
	# 每本书单独建立文件夹
	path = f'鬼吹灯/{book["location"]}'
	if not os.path.exists(path):
		os.mkdir(path)
	with open(os.path.join(path, f'{book["title"]}.txt'), 'w', encoding='utf-8') as f:
		f.write(book["content"])


def main():
	# 创建鬼吹灯文件夹
	path = '鬼吹灯'
	if not os.path.exists(path):
		os.mkdir(path)
	for section_url in get_book_url(url):
		book = get_section_info(section_url)
		download_section(book)


if __name__ == '__main__':
	main()
