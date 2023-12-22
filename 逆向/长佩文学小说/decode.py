import requests
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
import base64

chatper_id = 5241236  # 章节的id

url = f'https://m.gongzicp.com/webapi/novel/chapterGetInfo?cid={chatper_id}&server=0'

headers = {
	'Cookie': '_c_n_=bc5d852bfcad2c0e60bc0c8aac0047d2; PHPSESSID=tkisdlg9kk04dj0okdk5nfi4j6',
	'Token': '426e9ecd47712da625f3ac863b02b3e2',
	'Referer': 'https://m.gongzicp.com/read-5484072.html',
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
}

# 获取到返回的数据
resp = requests.get(url, headers=headers)
# print(resp.text)

dic_data = json.loads(resp.text)
# print(dic_data)

# 章节信息
chapter_info = dic_data['data']['chapterInfo']
chapter_name = chapter_info['name']  # 章节名称
decode_content = chapter_info['content']  # 返回的章节内容加密后的数据
# print(type(decode_content))
# print(chapter_name)
# print(decode_content)

# 解密
iv = '$h$b3!iGzsYnnshj'
key = 'u0LRrbu$Enm84koA'
aes = AES.new(key=b'u0LRrbu$Enm84koA', mode=AES.MODE_CBC, iv=b'$h$b3!iGzsYnnshj')
text_bytes = base64.b64decode(decode_content)
text_bytes = aes.decrypt(text_bytes)
text = unpad(text_bytes, AES.block_size).decode('utf-8')  # 自动获取字节填充量大小
print(text)



