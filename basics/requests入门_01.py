# 安装requests
# pip install requests
import requests

name = input('请输入要搜索的内容: ')
url = f'https://www.sogou.com/web?query={name}'

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
	              "like Gecko) "
	              "Chrome/118.0.0.0 Safari/537.36"}

resp = requests.get(url, headers=headers)

# print(resp.text)  # 获取网页所有内容
print(resp.request)  # 获取请求方式
print(resp.headers)  # 获取请求头
print(resp.encoding)  # 获取编码方式

resp.close()
