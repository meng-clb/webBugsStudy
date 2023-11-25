from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
import requests
from datetime import datetime

hot_file = open('one_hot.txt', 'w', encoding='utf-8')
comment_file = open('one_comment.txt', 'w', encoding='utf-8')

# 找到想要抓取的音乐的id,写入这里, 运行文件即可
music_Id = '2089114348'

e = '010001'
f = \
	'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = '2XX6DUZivbiNfp60'
encText = "02OXoWNVd/IReeGhk8nhZgBXrYETzd2sh/YosveGYDinRSxkDWGnKn0uPTBzrEnS"

# 第一页

data = {
	"rid": f"R_SO_4_{music_Id}",  # 后边是歌曲id
	"threadId": f"R_SO_4_{music_Id}",
	"pageNo": 1,
	"pageSize": 20,
	"cursor": -1,
	"offset": 0,
	"orderType": 1
}

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

'------------------------网易云反破解---------------------------------------------------'


def get_encSecKey():
	return \
		"cd2b05e66c7e6908af62e52109705074cfe949ecc29e9b2cc7858101ba53e7931172216cbed6f8f0df2fbc16422bd477487794f7daf3648f02e2c2bf122ffb7dc69d8f4e74d6b9bfa60b5bd5467bca1254d39d6387f148081acf900cf8e0bdff8918f017421340294397b07b6d6fddfdd56803fb255530feb22e198ab0f28810"


def get_params(data):
	first = enc_params(data, g)
	second = enc_params(first, i)
	return second


def to_16(data):
	pad = 16 - len(data) % 16
	data += chr(pad) * pad
	return data


def enc_params(data, key):  # 加密过程
	iv = '0102030405060708'
	data = to_16(data)
	aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
	bs = aes.encrypt(data.encode('utf-8'))
	return str(b64encode(bs), 'utf-8')


'-------------------------------------------------------------------------------'

'---------获取时间--------------'


def date_time(t):
	timestamp = int(t) / 1000
	date = datetime.fromtimestamp(timestamp)
	return date.date()


'-----------------------'

resp = requests.post(url, data={
	"params": get_params(json.dumps(data)),
	"encSecKey": get_encSecKey()
})

hot_comments = json.loads(resp.text)['data']['hotComments']
for user in hot_comments:
	text = user['content']
	timer = user['time']
	time = date_time(timer)
	text = text.strip()
	hot_file.write(f'\n------------------------------{time}-------------------------------------\n')
	hot_file.write(text)
	hot_file.write('\n-------------------------------------------------------------------\n')


print('热评抓取完成 over!!!')

comments = json.loads(resp.text)['data']['comments']
for user in comments:
	text = user['content']
	timer = user['time']
	time = date_time(timer)
	comment_file.write(f'\n------------------------------'
	                   f'{time}-------------------------------------\n')
	comment_file.write(text)
	comment_file.write('\n-------------------------------------------------------------------\n')

print('当前评论抓取完成 over!!!!')
resp.close()

hot_file.close()
comment_file.close()
