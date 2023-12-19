# 在python中链接CMD的那个东西是subprocess里面的Popen
# 解决execjs的问题
# 在引入execjs之前, 加上以下代码
import subprocess
from functools import partial  # 作用, 用来锁定某个参数的固定值

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs  # 用的是node.js

import requests
import json

url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
}
# song_id = 2071935674  # 改变歌曲id可以获取这首歌曲的url
song_id = 2103764064

data = {  # 真实的参数
	"ids": f"[{song_id}]",
	"level": "standard",
	"encodeType": "aac",
	"csrf_token": ""
}

js = execjs.compile(open('decode.js', 'r', encoding='utf-8').read())
result = js.call('decode', json.dumps(data))  # 获取加密后的参数, 传递字符串
# print(result)

real_data = {  # 传递真是参数加密后的参数
	'params': result['encText'],
	'encSecKey': result['encSecKey']
}
resp = requests.post(url, headers=headers, data=real_data)  # 请求到歌曲的url
print(resp.text)

