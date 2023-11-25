import os.path
import requests
import re
from concurrent.futures import ThreadPoolExecutor, wait


def get_ts_url(home_url):
	"""
	获取所有ts文件的链接
	:param home_url: 通过首页链接去获取m3u8文件的链接
	:return: 所有ts文件的列表
	"""
	resp = requests.get(home_url, headers=headers)
	# 获取到index.m3u8文件, 通过这个地址获取ts文件url
	index_m3u8_url = re.search(r'"yun":true,"url":"(?P<index_m3u8>.*?)"', resp.text).group(
		'index_m3u8').replace('\\', '').strip()
	# 通过ts文件url得到ts所有文件的url
	res = requests.get(index_m3u8_url, headers=headers)
	# 获取ts所有文件请求链接的后半部分
	ts_url_end = res.text.split('\n')[-1]
	# ts所有文件请求链接的前半部分
	ts_url_front = index_m3u8_url.rsplit('/', 1)[0]
	# ts所有文件链接
	ts_url = ts_url_front + '/' + ts_url_end

	# 单个ts文件的前半部分
	ts_front = ts_url.rsplit('/', 1)[0]

	# 通过ts链接获取所有的ts文件
	resp = requests.get(ts_url, headers=headers)

	# 将获取到所有的ts文件写入文件
	with open('ts.txt', 'w', encoding='utf-8') as f:
		f.write(resp.text)

	# ts文件url后半部分
	ts_end_list = []
	# 对ts文件后半部分进行处理
	with open('ts.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			if not line.startswith('#'):
				line = line.strip()
				ts_end_list.append(line)
	ts_url_list = []
	for ts_end in ts_end_list:
		ts = ts_front + '/' + ts_end
		ts_url_list.append(ts)
	return ts_url_list


def download_ts(path, ts_url):
	"""
	下载单个的ts文件
	:param path: ts文件存储的文件夹名称
	:param ts_url:单个ts文件的下载链接
	:return:
	"""
	while True:
		try:
			ts_name = str(ts_url).rsplit('/', 1)[-1]
			resp = requests.get(ts_url, headers=headers, timeout=60)
			print(f'{ts_name}开始下载....')
			with open(os.path.join(path, ts_name), 'wb') as f:
				f.write(resp.content)
			print(f'{ts_name}下载完成')
			break
		except:
			ts_name = str(ts_url).rsplit('/', 1)[-1]
			print(f'{ts_name}下载失败, 重新下载...')


def download_all_ts(path, home_url):
	"""
	下载所有的ts文件
	:param path: ts文件存储的文件夹名称
	:param home_url: 首页的url
	:return:
	"""
	if not os.path.exists(path):
		os.mkdir(path)
	pool = ThreadPoolExecutor(100)
	tasks = []
	ts_url_list = get_ts_url(home_url)
	for url in ts_url_list:
		ts_url = url.strip()
		tasks.append(pool.submit(download_ts, path, ts_url))
	# 集体等待
	wait(tasks)


if __name__ == '__main__':
	url = 'https://www.91mjtv.com/meiju/ruwozhilangdierji/1-1.html'

	headers = {
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/119.0.0.0 Safari/537.36'
	}
	path = 'ts'

	download_all_ts(path, url)
