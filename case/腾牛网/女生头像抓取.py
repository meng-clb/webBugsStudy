import time

import requests
from lxml import etree
import os

url = 'https://www.qqtn.com/tx/nvshengtx_1.html'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

# 全局变量下载图片计数
img_num = 0


# 获取图片
def get_img(url):
	res = requests.get(url, headers=headers)
	res.encoding = 'gbk'
	html = etree.HTML(res.text)
	path = 'img'

	if not os.path.exists(path):
		os.mkdir(path)

	url_list = html.xpath('//ul[@class="g-gxlist-imgbox"]/li/a/img/@src')
	for url in url_list:
		# print(url)
		name = url.split('/')[-1]
		img = requests.get(url)

		with open(os.path.join(path, name), 'wb') as f:
			res = requests.get(url)
			f.write(res.content)
		global img_num
		img_num += 1
		print(f'已抓取{img_num}张小黄图')
		print(f'{name}      over!!')
		time.sleep(0.2)


def get_page(url):
	res = requests.get(url, headers=headers)
	res.encoding = 'gbk'
	html = etree.HTML(res.text)
	pages = html.xpath('//ul[@class="g-gxlist-imgbox"]//div[@class="tsp_count"]/text()')
	pages = pages[-2].split(' ')[0].split('/')[-1]
	print(f'共有{pages}页数据')
	start = int(input(f'输入你要开始抓取的页数(1-{pages}): '))
	end = int(input(f'输入你要抓取结束的页数(1-{pages}): '))
	print('开始抓取')

	for x in range(start, end + 1):
		url = f'https://www.qqtn.com/tx/nvshengtx_{x}.html'
		get_img(url)
		print(f'page{x}over!!')


if __name__ == '__main__':
	get_page(url)
