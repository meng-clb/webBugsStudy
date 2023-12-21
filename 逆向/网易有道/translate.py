import time
from hashlib import md5
import requests

u = "fanyideskweb"
d = "webfanyi"
m = "client,mysticTime,product"
p = "1.0.0"
g = "web"
b = "fanyi.web"
A = 1
h = 1
f = 1
v = "wifi"
O = 0
e = str(int(time.time() * 1000))

# print(e)
# e = '1703047282670'
t = 'fsdsogkndfokasodnaso'
s = f'client={u}&mysticTime={e}&product={d}&key={t}'  # 需要解密
obj = md5()
obj.update(s.encode('utf-8'))
result = obj.hexdigest()
print(result)
word = 'dog'

from_data = {
	'i': word,
	'from': 'auto',
	'domain': 0,
	'dictResult': 'true',
	'keyid': 'webfanyi',
	'sign': result,
	'client': 'fanyideskweb',
	'product': 'webfanyi',
	'appVersion': '1.0.0',
	'vendor': 'web',
	'pointParam': 'client,mysticTime,product',
	'mysticTime': e,
	'keyfrom': 'fanyi.web',
	'mid': 1,
	'screen': 1,
	'model': 1,
	'network': 'wifi',
	'abtest': 0,
	'yduuid': 'abcdefg'
}

url = 'https://dict.youdao.com/webtranslate'
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36',
}
resp = requests.post(url, data=from_data, headers=headers)
print(resp.text)
