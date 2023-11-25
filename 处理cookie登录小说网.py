# 1. 登录网站
# 2. 拿到cookie,使用cookie请求网站
import requests
import json

url = 'https://passport.17k.com/ck/user/login'
headers = {
	'Cookie': 'GUID=a36cdad4-a856-4702-8f24-291cf21ba5cb; sajssdk_2015_cross_new_user=1; '
	          'Hm_lvt_9793f42b498361373512340937deb2a0=1698931423; c_channel=0; c_csc=web; '
	          'Hm_lpvt_9793f42b498361373512340937deb2a0=1698931610; '
	          'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22a36cdad4-a856-4702-8f24'
	          '-291cf21ba5cb%22%2C%22%24device_id%22%3A%2218b9031fce35db-038e785c19353b-26031151'
	          '-1327104-18b9031fce479e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22'
	          '%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22'
	          '%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6'
	          '%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C'
	          '%22first_id%22%3A%22a36cdad4-a856-4702-8f24-291cf21ba5cb%22%7D'
}

data = {
	'loginName': '19713055472',
	'password': 'clb1234'
}

# session可以缓存cookie, 相当于会话模式
session = requests.session()
session.post(url, data=data)
# 获取到我的书架
resp = session.get('https://user.17k.com/ck/author2/shelf?page=1&appKey=2406394919')
# 获取到的数据处理为json
bookshelf = resp.json()
# 获取data列表, 里边包含书籍信息
book_data_list = bookshelf['data']
book_name_list = []
for item in book_data_list:
	book_name = item['bookName']
	book_name_list.append(book_name)

# 打印书名
for name in book_name_list:
	print(name)