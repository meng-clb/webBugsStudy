import os.path

import requests
import re

url = 'https://www.91mjtv.com/meiju/ruwozhilangdierji/1-1.html'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

resp = requests.get(url, headers=headers)
# 获取到index.m3u8文件, 通过这个地址获取ts文件url
index_m3u8_url = re.search(r'"yun":true,"url":"(?P<index_m3u8>.*?)"', resp.text).group(
	'index_m3u8').replace('\\', '').strip()

# 通过ts文件url得到ts所有文件的url
# res = requests.get(index_m3u8_url, headers=headers)

# 通过url获取的index.m3u8文件的链接写入到文件
# with open('index.txt', 'w', encoding='utf-8') as f:
# 	f.write(res.text)

# 读取ts所有文件所在url的
with open('index.txt', 'r', encoding='utf-8') as f:
	index_ts = f.read()

# 获取所有ts文件的拼接代码
url_end = index_ts.split('\n')[-1]
url_front = index_m3u8_url.rsplit('/', 1)[0].strip()
# ts文件的url
ts_index_url = url_front + '/' + url_end
# 通过拼接得到的url, 获取所有的ts文件url
# resp = requests.get(ts_index_url, headers=headers)
# print(resp.text)

# 获取到的ts所有文件链接写入文件
# with open('ts.txt', 'w', encoding='utf-8') as f:
# 	f.write(resp.text)

with open('ts.txt', 'r', encoding='utf-8') as f:
	ts_txt = f.read()

# 处理ts文件的链接
ts_url_front = ts_index_url.rsplit('/', 1)[0]
print(ts_url_front)


def ts_url_end(path):
	"""
	获取所有的ts文件url的后半部分
	:param path: 存储ts文件返回的所有ts路径文件
	:return: ts文件url后半部分
	"""
	ts_list = []
	with open(path, 'r', encoding='utf-8') as f:
		for line in f:
			if line[0] != '#':
				ts_list.append(line.strip())
	return ts_list


def download_ts(path, ts_end):
	"""
	根据传入的ts链接下载ts文件
	:param path: 文件存放位置
	:param ts_end: ts文件的后半部分url
	:return:
	"""
	# 拼接ts文件完整的链接
	ts_url = ts_url_front + '/' + ts_end
	# 请求到文件之后下载保存到本地
	resp = requests.get(ts_url, headers=headers)
	with open(os.path.join(f'{path}', f'{ts_end}'), 'wb') as f:
		f.write(resp.content)


if __name__ == '__main__':
	path = 'ts'
	if not os.path.exists(path):
		os.mkdir(path)

	ts_list = ts_url_end('ts.txt')
	for ts in ts_list:
		download_ts(path, ts)
		# 只下载第一个ts文件用于测试
		break

'''
分析,
获取ts文件
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/index.m3u8'
													 '2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'

ts文件
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/index.m3u8'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/a2e6ddf9e34000058.ts'
'https://cdn1.vip-vip-yzzy.com/20231031/4576_eee33622/2000k/hls/a2e6ddf9e34000059.ts'

'''
