import asyncio
import time
import requests
from lxml import etree
import aiohttp

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'https://movie.douban.com/chart'


async def get_detail_url():
	"""
	获取页面中所有电影的详情页链接
	:return: 详情页链接列表
	"""
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text())
			detail_url = html.xpath('//tr[@class="item"]/td[1]/a/@href')
	return detail_url


async def get_detail(url):
	"""
	获取详情页面的电影标题
	:param url: 要抓取页面的url
	:return: 无
	"""
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text())
			detail = html.xpath('//*[@id="content"]/h1/span[1]/text()')
			print(detail)
	return detail


if __name__ == '__main__':
	t1 = time.time()
	loop = asyncio.get_event_loop()
	detail_url = loop.run_until_complete(get_detail_url())
	# 使用列表创建异步任务列表
	tasks = [get_detail(url) for url in detail_url]
	loop.run_until_complete(asyncio.gather(*tasks))

	print(time.time() - t1)
