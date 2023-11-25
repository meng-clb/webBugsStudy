# 安装 bs4
# pip install bs4

import requests
from bs4 import BeautifulSoup
import csv

f = open('read_book.csv', 'w', encoding='utf-8')
csvwrite = csv.writer(f)

# 读书网首页
home_url = 'https://www.dushu.com/'

page_num = 1

for i in range(10):
	url = f'https://www.dushu.com/book/1176_{page_num}.html'
	# 获取到页面
	resp = requests.get(url)

	# 解析数据
	# 1. 把页面源代码交给BeautifulSoup进行处理,生成bs对象
	page = BeautifulSoup(resp.text, 'html.parser')
	# 2. 从bs对象中查找数据
	data = page.find_all('div', class_="book-info")
	# 3. 进一步从data中拿到书籍的数据
	# 生成一个字典来保存数据
	dic = {}
	for it in data:
		book_name = it.find('h3')
		book_author = it.find('p')
		book_url = it.find('a')
		# 获取到标签的属性
		href = book_url.get('href').strip('/')
		book_href = home_url + href
		# 书本定价页面
		resp_book = requests.get(book_href)
		resp_book_information = resp_book.text
		# 获取的页面生成bs4对象
		book_page = BeautifulSoup(resp_book_information, 'html.parser')
		# 获取当前书本的价格
		book_price = book_page.find('span', class_="num").text.strip('¥')
		dic['book_name'] = book_name.text
		dic['book_author'] = book_author.text
		dic['book_price'] = book_price
		csvwrite.writerow(dic.values())
		resp_book.close()
	# 进行迭代, 爬取更多页面的数据
	i = i + 1
	page_num = page_num + 1
	resp.close()

f.close()

print('over!')
