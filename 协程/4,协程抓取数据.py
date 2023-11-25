import time

import requests
import aiohttp
from lxml import etree
import asyncio

url = 'https://movie.douban.com/chart'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


async def get_url(url):
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text())
			url_list = html.xpath('//div[@class="indent"][1]//table//a/@href')
	return url_list


async def get_info(detail_url):
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(detail_url) as resp:
			movie = {}
			html = etree.HTML(await resp.text())
			# 获取电影名称
			title_list = html.xpath('//h1/span/text()')
			title = title_list[0] + title_list[1]
			# 获取电影简介
			info = str(html.xpath('//div[@class="related-info"]//span/text()')[0]).strip()
			movie[title] = info
			print(movie)
	return movie


async def main(url):
	url_list = await get_url(url)
	tasks = []
	for url in url_list:
		task = asyncio.create_task(get_info(url))
		tasks.append(task)
	await asyncio.wait(tasks)

if __name__ == '__main__':
	t1 = time.time()
	asyncio.run(main(url))
	print(time.time() - t1)
