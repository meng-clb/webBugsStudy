"""
1. 获取到首页内的所有图片链接
2. 通过每个图片的链接去到图片所在的子页面
3. 通过每个子页面的链接获取所有的图片
4. 将图片输出保存到文件夹
"""
import requests
from bs4 import BeautifulSoup
import csv
import re

# 主页面所有图片的链接的列表
pic_list = []


def home():
	"""
	获取到主页面所有前往子页面图片的链接
	把所有的链接放到pic_list内
	:return: 无
	"""
	# 设置访问的页数
	home_page_num = 1
	for x in range(10):
		home_url = f'http://www.umeituku.com/bizhitupian/meinvbizhi/{home_page_num}.htm'
		resp = requests.get(home_url)
		resp.encoding = 'utf-8'
		home_text = BeautifulSoup(resp.text, "html.parser")
		# 获取到所有图片元素的超链接元素a
		a_list = home_text.find('div', class_="TypeList").find_all('a')
		for a in a_list:
			# 拿到所有子页面的超链接
			pic_list.append(a.get('href'))

		resp.close()
		x = x + 1
		home_page_num = home_page_num + 1


def child(pics: list):
	"""
	处理子页面的图片信息,将其图片保存到img文件夹内
	:param pics: 主页面中所有子页面的图片链接
	:return:
	"""
	for it in pics:
		# 先处理访问子页面的链接
		resp = requests.get(it)
		resp.encoding = 'utf-8'
		child_text = BeautifulSoup(resp.text, 'html.parser')
		img_a = child_text.find('div', class_="ImageBody").find('img')
		img_src = img_a.get('src')
		img_name = img_src.split('/')[-1]
		# 下载图片
		img_resp = requests.get(img_src)
		# img_resp.content # 拿到的是图片的字节码
		with open('img/' + img_name, "wb") as f:
			f.write(img_resp.content)
			print('over!!!  ' + img_name)

		resp.close()
		img_resp.close()


# def str_href(url: str):
# 	'http://www.umeituku.com/bizhitupian/meinvbizhi/203957.htm'
# 	num = 1
# 	u_list = url.split('.')
# 	u_list.insert(-1, f'_{num}')
# 	href = ''
# 	for it in u_list:
# 		href = href + it + '.'
#
# 	print(href)


if __name__ == '__main__':
	home()
	child(pic_list)
	print('over_all!!')
