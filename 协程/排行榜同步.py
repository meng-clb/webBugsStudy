import time

import requests
from lxml import etree

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'https://movie.douban.com/chart'


def get_detail_url():
	"""
	获取页面中所有电影的详情页链接
	:return: 详情页链接列表
	"""
	resp = requests.get(url, headers=headers)
	html = etree.HTML(resp.content.decode())
	detail_url = html.xpath('//tr[@class="item"]/td[1]/a/@href')
	return detail_url


def get_detail(url):
	"""
	获取详情页面的电影标题
	:param url: 要抓取页面的url
	:return: 无
	"""
	resp = requests.get(url, headers=headers)
	html = etree.HTML(resp.content.decode())
	detail = html.xpath('//*[@id="content"]/h1/span[1]/text()')
	print(detail)


if __name__ == '__main__':
	t1 = time.time()
	detail_url = get_detail_url()
	for url in detail_url:
		get_detail(url)
	print(time.time() - t1)
