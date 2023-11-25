import requests


url = 'https://xueqiu.com/'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

# 生成会话对象
session = requests.Session()
# 请求网址,拿到cookie, 下次请求自动携带cookie
session.get(url, headers=headers)
url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=558137&size=15'
# 这里请求时, 自动携带了cookie
res = session.get(url, headers=headers)
print(res.json())

