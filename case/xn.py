import requests
import re

# 获取页面的标题
obj1 = re.compile(r'<title>(?P<title>.*?)</title>', re.S)
# 获取子页面的所有链接
obj2 = re.compile(r'<div class="sub_list">.*?</ul></div>', re.S)
# 获取首页面中各个子页面的链接
obj3 = re.compile(r'<a href="(?P<href>.*?)"', re.S)

home_url = 'https://www.xyafu.edu.cn/zsxxw/'
url = 'https://www.xyafu.edu.cn/zsxxw/yjsks.htm'
home = requests.get(url)
home.encoding = 'utf-8'

home_data = home.text
home_title = obj1.findall(home_data)
ul = obj2.finditer(home_data)
child_href_list = []
for it in ul:
	ul_data = it.group()
	children_url= obj3.finditer(ul_data)
	for child in children_url:
		child_href = child.group('href')
		if child_href[0] != 'h':
			child_href = home_url + child_href
		child_href_list.append(child_href)

home.close()

for it in child_href_list:
	# 爬取到信农研究生考试的相关内容链接
	print(it)
