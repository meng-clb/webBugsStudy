# 在python中链接CMD的那个东西是subprocess里面的Popen
# 解决execjs的问题
# 在引入execjs之前, 加上以下代码
import subprocess
from functools import partial  # 作用, 用来锁定某个参数的固定值

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs  # 用的是node.js
import json

# 加载js函数
js = execjs.compile(open('wy_decode.js', 'r', encoding='utf-8').read())
# 处理传入参数, 未加密的参数
song_id = 2071935674
data = {
	"ids": f"[{song_id}]",  # 歌曲id 2071935674
	"level": "standard",
	"encodeType": "aac",
	"csrf_token": ""
}
json_data = json.dumps(data)  # 将字典转化为字符串

# 调用js函数, 拿到加密后需要传递的参数
result = js.call('decode', json_data)
# print(result)
real_data = {
	'params': result['encText'],
	'encSecKey': result['encSecKey']
}

import requests

url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
resp = requests.post(url, data=real_data, headers={
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
})
print(resp.text)
