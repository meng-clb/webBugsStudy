import requests
import aiohttp
from lxml import etree
import os
import asyncio
import aiofiles

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'https://www.51shucheng.net/daomu/guichuideng'


async def get_book_url(url):
	"""
	获取book每个章节的链接
	:param url: 目录页的url
	:return: 章节链接列表
	"""
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text(encoding='utf-8'))
			# 获取章节链接
			section_urls = html.xpath('//div[@class="mulu-list quanji"]/ul/li/a/@href')
	return section_urls


async def get_section_info(section_url):
	# 处理抓取到的数据存储位置
	book_name = str(section_url).rsplit('/', 2)[-2]

	async with aiohttp.ClientSession() as session:
		async with session.get(section_url) as resp:
			html = etree.HTML(await resp.text(encoding='utf-8'))
			# 章节名称
			section_title = str(html.xpath('//h1/text()')[0]).strip().replace(':', '_')
			# 章节内容
			section_con = '\n\n'.join(html.xpath('//div[@class="neirong"]/p/text()'))
			# 每本书单独建立文件夹
			path = f'鬼吹灯/{book_name}'
			if not os.path.exists(path):
				os.mkdir(path)
			# 将抓取到的内容下载到本地
			print(f'{section_title}开始下载')
			# 使用异步写入文件
			async with aiofiles.open(os.path.join(path, f'{section_title}.txt'), 'w',
			                         encoding='utf-8') as f:
				await f.write(section_con)


async def main(url):
	# 创建鬼吹灯文件夹
	path = '鬼吹灯'
	if not os.path.exists(path):
		os.mkdir(path)
	tasks = []
	section_urls = await get_book_url(url)
	for section_url in section_urls:
		task = asyncio.create_task(get_section_info(section_url))
		tasks.append(task)

	await asyncio.wait(tasks)


if __name__ == '__main__':
	asyncio.run(main(url))
	print('over!')
