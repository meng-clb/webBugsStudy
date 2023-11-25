import os.path

import requests
from lxml import etree


def get_section_url(url):
	resp = requests.get(url)
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	# 获取书本的名字
	book_name = html.xpath('//h1/text()')[0]
	# 获取所有章节的链接_后半部分
	section_urls_end = html.xpath(
		'//dl[@class="Volume"][position() > 1 and position() < last()]//dd/a/@href')
	return section_urls_end


def down_load(path, section_url_front, section_url_end):
	section_url = section_url_front + section_url_end
	resp = requests.get(section_url)
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	# 章节标题
	title = str(html.xpath('//div[@class="readAreaBox content"]/h1/text()')[0]).strip().replace(
		' ', '_')
	# 章节内容
	content = '\n'.join(html.xpath('//div[@class="readAreaBox content"]/div[@class="p"]/p['
	                               'position() < last()]/text()'))
	# 写入到文件内
	print(f'{title}开始下载')
	with open(os.path.join(path, title + '.txt'), 'w', encoding='utf-8') as f:
		f.write(content)


def main(url):
	path = '修罗武神'
	if not os.path.exists(path):
		os.mkdir(path)
	# 小说章节链接前半部分
	section_url_front = url.rsplit('/', 2)[0]
	# 小说章节链接后半部分
	section_urls_end = get_section_url(url)
	for url_end in section_urls_end:
		down_load(path, section_url_front, url_end)

	print('over ! ')


if __name__ == '__main__':
	headers = {
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/119.0.0.0 Safari/537.36'
	}

	url = 'https://www.17k.com/list/493239.html'

	main(url)
