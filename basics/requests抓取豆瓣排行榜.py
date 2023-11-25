import requests

url = 'https://movie.douban.com/j/chart/top_list'

f = open('comedy.txt', "a", encoding='utf-8')

start = 0  # 设置初始值,模仿滚轮滑动, 获取页面滚轮滑动后加载出来的内容
# 使用get请求携带的参数
param = {
	'type': '24',
	'interval_id': '100:90',
	'action': '',
	'start': start,
	'limit': 20
}

# 请求头信息
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/118.0.0.0 Safari/537.36'
}

# 抓取1-5页的数据
for x in range(5):
	resp = requests.get(url=url, params=param, headers=headers)
	f.write(resp.text)
	start = start + 20
	param['start'] = start
	x = x + 1
	resp.close()

f.close()
print('写入完成')
# resp = requests.get(url=url, params=param, headers=headers)
