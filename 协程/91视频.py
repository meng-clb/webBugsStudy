import os.path

import requests
import re

url = 'https://www.91mjtv.com/meiju/ruwozhilangdierji/1-1.html'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


def get_ts_all(ts_file, url):
	"""
	获取所有的ts链接,存储到文件内
	:param ts_file: ts文件链接存放文件
	:param url: 通过视频页获取index_m3u8数据
	:return:
	"""
	resp = requests.get(url, headers=headers)
	# 获取index_m3u8的url
	index_m3u8 = re.search(r'"url":"(?P<index_url>.*?)"', resp.text, re.S).group(
		'index_url').replace('\\', '')

	# 通过index_m3u8获取ts文件存储链接
	res = requests.get(index_m3u8)
	index_m3u8_url_end = res.text.split('\n')[-1]
	index_m3u8_url_front = index_m3u8.rsplit('/', 1)[0]
	res.close()
	# 完整的index_m3u8_url链接
	index_m3u8_url = index_m3u8_url_front + '/' + index_m3u8_url_end
	# ts文件链接的前半部分
	ts_url_front = index_m3u8_url.rsplit('/', 1)[0]
	# print(ts_url_front)
	# 通过完整的index_url获取ts文件的所有链接后半部分
	res = requests.get(index_m3u8_url, headers=headers)
	# 获取到的ts链接后半部分存储到文件内
	with open(ts_file, 'w', encoding='utf-8') as f:
		ts_list = res.text.strip().split('\n')
		for ts in ts_list:
			if not ts.startswith('#'):
				f.write(ts_url_front + '/' + ts + '\n')
	print('ts链获取完成')
	resp.close()
	res.close()


def down_load(path, url):
	"""
	通过ts文件下载ts文件到本地
	:param path: 存储到' '文件夹下
	:param url: ts文件的链接
	:return:
	"""
	# ts文件名
	ts_name = url.rsplit('/', 1)[-1].strip()
	resp = requests.get(url, headers=headers)
	print(f'{ts_name}开始下载')
	with open(os.path.join(path, ts_name), 'wb') as f:
		f.write(resp.content)


if __name__ == '__main__':
	path = 'ts'
	ts_file = 'ts.txt'
	if not os.path.exists(path):
		os.mkdir(path)
	get_ts_all(ts_file, url)
	with open(ts_file, 'r', encoding='utf-8') as f:
		for url in f.readlines():
			# print(url)
			url = url.strip()
			down_load(path, url)

"""
													  '2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/index.m3u8
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/a2e6ddf9e34000142.ts'
"""
