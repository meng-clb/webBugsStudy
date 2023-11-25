import os.path
import re
import asyncio

import aiofiles
import aiohttp

url = 'https://www.91mjtv.com/meiju/ruwozhilangdierji/1-1.html'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


async def get_ts_all(path, ts_file, url):
	"""
	获取所有的ts链接,存储到文件内
	:param ts_file: ts文件链接存放文件
	:param url: 通过视频页获取index_m3u8数据
	:return:
	"""
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(url) as resp:
			# 获取index_m3u8的url
			index_m3u8 = re.search(r'"url":"(?P<index_url>.*?)"', await resp.text(), re.S).group(
				'index_url').replace('\\', '')
	async with aiohttp.ClientSession(headers=headers) as session:
		async with session.get(index_m3u8) as resp:
			# 通过index_m3u8获取ts文件存储链接
			index_m3u8_url_end = (await resp.text()).split('\n')[-1]
			index_m3u8_url_front = index_m3u8.rsplit('/', 1)[0]
			# 完整的index_m3u8_url链接
			index_m3u8_url = index_m3u8_url_front + '/' + index_m3u8_url_end
			# ts文件链接的前半部分
			ts_url_front = index_m3u8_url.rsplit('/', 1)[0]
	# print(ts_url_front)
	async with aiohttp.ClientSession(headers=headers) as session:
		# 通过完整的index_url获取ts文件的所有链接后半部分
		async with session.get(index_m3u8_url) as resp:
			content = await resp.text()
			# 将index.m3u8文件存储起来, 用于处理合并视频
			with open(os.path.join(path, 'index.m3u8'), 'w', encoding='utf-8') as f:
				f.write(content)
			# 获取到的ts链接存储到文件内
			with open(ts_file, 'w', encoding='utf-8') as f:
				ts_list = (await resp.text()).strip().split('\n')
				for ts in ts_list:
					if not ts.startswith('#'):
						f.write(ts_url_front + '/' + ts + '\n')
	print('ts链获取完成')


async def down_load(path, url):
	"""
	通过ts文件下载ts文件到本地
	:param path: 存储到' '文件夹下
	:param url: ts文件的链接
	:return:
	"""
	# ts文件名
	ts_name = url.rsplit('/', 1)[-1].strip()
	while True:
		async with aiohttp.ClientSession(headers=headers) as session:
			async with session.get(url) as resp:
				# 异步读取文件
				content = await resp.read()
				try:
					print(f'{ts_name}开始下载....')
					async with aiofiles.open(os.path.join(path, ts_name), 'wb') as f:
						await f.write(content)
					print(f'{ts_name}下载完成')
					break
				except:
					print(f'{ts_name}下载失败,重新下载....')


async def main(ts_file, path):
	tasks = []
	async with aiofiles.open(ts_file, 'r', encoding='utf-8') as f:
		lines = await f.readlines()
		for url in lines:
			url = url.strip()
			task = asyncio.create_task(down_load(path, url))
			tasks.append(task)
		await asyncio.wait(tasks)


def merge(path, filename='output'):
	"""
	合并所有的ts文件, 合成一个完整的视频
	:param path: ts文件路径
	:param filename: 输出的文件名
	"""
	print('开始合并....')
	os.chdir(path)
	cmd = f'ffmpeg -i index.m3u8 -c copy {filename}.mp4'
	os.system(cmd)
	print('合并完成!')


if __name__ == '__main__':
	path = 'ts'
	ts_file = 'ts.txt'
	if not os.path.exists(path):
		os.mkdir(path)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(get_ts_all(path, ts_file, url))
	asyncio.run(main(ts_file, path))
	print('视频全部下载完成!')
	merge(path)
	print('over!')
"""
													  '2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/index.m3u8
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/a2e6ddf9e34000142.ts'
"""
