import os.path
import requests
from lxml import etree
import aiohttp
import asyncio


async def get_section_url(url):
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			html = etree.HTML(await resp.text(encoding='utf-8'))
			# 获取书本的名字
			book_name = html.xpath('//h1/text()')[0]
			# 获取所有章节的链接_后半部分
			section_urls_end = html.xpath(
				'//dl[@class="Volume"][position() > 1 and position() < last()]//dd/a/@href')
	return section_urls_end


async def down_load(i, path, section_url):
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(section_url) as resp:
			html = etree.HTML(await resp.text(encoding='utf-8'))
			# 章节标题
			title = str(
				html.xpath('//div[@class="readAreaBox content"]/h1/text()')[0]).strip().replace(
				' ', '_')
			# 章节内容
			content = '\n'.join(html.xpath('//div[@class="readAreaBox content"]/div[@class="p"]/p['
			                               'position() < last()]/text()'))

			# 写入到文件内
			print(f'{title}开始下载')
			with open(os.path.join(path, f'{i}_{title}.txt'), 'w', encoding='utf-8') as f:
				f.write(content)
			print(f'{title}下载完成')


async def main(url):
	i = 1
	path = '修罗武神'
	if not os.path.exists(path):
		os.mkdir(path)
	# 小说章节链接前半部分
	section_url_front = url.rsplit('/', 2)[0]
	# 小说章节链接后半部分
	section_urls_end = await get_section_url(url)
	tasks = []
	for url_end in section_urls_end:

		section_url = section_url_front + url_end
		task = asyncio.create_task(down_load(i, path, section_url))
		i += 1
		tasks.append(task)
	await asyncio.wait(tasks)

	print('over ! ')


if __name__ == '__main__':
	headers = {
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/119.0.0.0 Safari/537.36'
	}

	url = 'https://www.17k.com/list/493239.html'

	asyncio.run(main(url))
