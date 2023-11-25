import asyncio
import os
from lxml import etree
import requests
import aiohttp

url = 'https://www.51shucheng.net/daomu/guichuideng'
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


async def get_chapter_url():
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text(encoding='utf-8'))
			a_list = html.xpath('//div[@class="mulu-list quanji"]/ul/li/a/@href')
	return a_list


async def download_chapter(url):
	"""
	通过url获取章节内容并下载到本地
	:param url: 每一章节的url
	:return:
	"""
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:

			html = etree.HTML(await resp.text(encoding='utf-8'))
			# 获取每一章节的标题, 作为文件名
			title = html.xpath('//h1/text()')[0]
			book_title = ''.join(str(title).split(' ')).replace(':', '_')
			print(book_title)
			# 获取章节内容并处理
			content = '\n\n'.join(html.xpath('//*[@id="neirong"]/p/text()'))
			# print(content)
			path = str(url).split('/')[-2]
			if not os.path.exists(path):
				os.mkdir(path)
			# 写入文件
			with open(os.path.join(path, book_title + '.txt'), 'w', encoding='utf-8') as f:
				f.write(content)
			print(f'{book_title}写入完成')


if __name__ == '__main__':
	# 老版本的写法
	loop = asyncio.get_event_loop()
	a_list = loop.run_until_complete(get_chapter_url())
	tasks = [download_chapter(url) for url in a_list]
	loop.run_until_complete(asyncio.gather(*tasks))
