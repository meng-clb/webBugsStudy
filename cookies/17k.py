import requests

url = 'https://passport.17k.com/login/'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}
from_data = {
	'loginName': '19713055472',
	'password': 'Clb12345'
}
# 实例化session对象, 是对话保持
session = requests.Session()
# 登录之后可以访问的url
url = 'https://user.17k.com/www/bookshelf/index.html'

resp = session.get(url, headers=headers, data=from_data)

print(resp.content.decode())
