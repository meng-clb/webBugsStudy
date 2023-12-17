import requests
from lxml import etree
from urllib.parse import urljoin
import os

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
}


# 把url获取到的源码直接处理为xpath对象返回
def get_html(url):
	"""
	把url获取到的源码直接处理为xpath对象返回
	:param url: 要获取源码的url
	:return: xpath对象
	"""
	resp = requests.get(url, headers=headers)
	# print(resp.content.decode())
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	return html


# 获取菜单类型的url
def get_menu_urls(html, url_front):
	"""
	获取每个类型的url
	:param html: 首页源码的xpath对象, 直接通过首页源码获取菜单内各种类型的url
	:param url_front: 拼接字符串的前半部分
	:return: 返回菜单内各种类型的url列表
	"""
	menu_url_end = html.xpath('//li[@class="menu-item menu-item-has-children"]/ul/li/a/@href')
	# print(menu_url_end)
	menu_urls = []
	for url_end in menu_url_end:
		url = urljoin(url_front, url_end)
		menu_urls.append(url)
	# print(menu_urls)
	return menu_urls


# 获取预览页一共有多少个页面
def get_detail_page(html):
	"""
	获取预览页一共有多少个页面
	:param html: 获取一共有多少个页面
	:return: 页面的数量
	"""
	# 获取预览页一共有多少页
	page_count = int(html.xpath('//div[@class="page"][1]/span/strong/text()')[0])
	# print('一共', page_count)
	return page_count


# 获取每个类型预览页所有的url
def get_detail_urls(url, html):
	"""
	获取每个类型预览页所有的url
	:param url: 上一级url链接, 用来拼接下一级详情页的url
	:param html: 类型详情页的源码xpath对象
	:return: 每个详情页所有对象的url
	"""
	detail_urls = []
	# print(url)
	detail_url_end = html.xpath('//ul[@class="update_area_lists cl"]/li/a/@href')
	for detail in detail_url_end:
		detail_url = urljoin(url, detail)
		detail_urls.append(detail_url)
	# print(detail_urls)
	# print('一共: ', page_count)
	return detail_urls


# 获取每个类型的名字, 用来做类型文件夹名
def get_classify_name(html):
	"""
	获取每个类型的名字, 用来做类型文件夹名
	:param html: 详情页的源码对象
	:return: 当前分类的名字
	"""
	classify_name = html.xpath('//h1/a[2]/text()')[0]
	return classify_name


# 获取图片的url地址
def get_img_url(html, detail_url):
	"""
	获取当前页面图片的url地址
	:param html: 当前页面源码的xpath对象
	:param detail_url: 上一级页面的url, 用来拼接图片的url地址
	:return: 所有图片的url
	"""
	img_urls = []
	img_url_end = html.xpath('//div[@class="content"][2]/p/img/@src')
	for img_url in img_url_end:
		url = urljoin(detail_url, img_url)
		img_urls.append(url)
	# print(img_urls)
	return img_urls


# 获取图片页的页码
def get_img_page():
	return


# 获取到当前图片的出镜人名字, 做细一级的文件夹名
def get_men_name(html):
	"""
	获取到当前图片的出镜人名字, 做细一级的文件夹名
	:param html: 图片页的源码对象
	:return: 出镜人姓名
	"""
	men_name = html.xpath('//div[@class="item_info"]/div/a[3]/span/text()')[0]
	return men_name


# 获取图片的bytes数据
def get_img_content(url):
	"""
	获取图片的bytes数据
	:param url: 图片的url
	:return: 图片的bytes数据
	"""
	resp = requests.get(url)
	return resp.content


# 下载图片到本地
def down_img(classify_name, men_name, img_name, img_content):
	path = os.path.join('img', classify_name, men_name)
	if not os.path.exists(path):
		os.makedirs(path)
		print(img_name + '开始下载')
	with open(path + '/' + img_name, 'wb') as f:
		f.write(img_content)


if __name__ == '__main__':
	# 秀人集首页url
	home_url = 'https://www.xr06.xyz/'
	home_html = get_html(home_url)  # 首页源码xpath对象
	menu_urls = get_menu_urls(home_html, home_url)  # 菜单内分类的url
	for detail_url in menu_urls:
		print('开始获取类型')
		detail_html = get_html(detail_url)  # 菜单内每一类的源码xpath对象
		detail_page_count = get_detail_page(detail_html)  # 详情页的所有页数
		classify_name = get_classify_name(detail_html)  # 获取当前的类型, 用来做类型文件夹名称
		for i in range(detail_page_count):  # 总共有多少页预览, 就抓取多少页的预览
			print('开始获取详情页内容')
			if i == 1:  # 第一页url最特别, 单独拿出来
				detail_urls = get_detail_urls(detail_url, detail_html)  # 获取到每个预览详情页的url
				for url in detail_urls:
					print('开始获取图片链接')
					imgs_html = get_html(url)  # 图片页的源码xpath对象
					img_urls = get_img_url(imgs_html, url)  # 获取图片页所有图片的url
					men_name = get_men_name(imgs_html)  # 图片出镜人的名字
					for img_url in img_urls:
						print('开始下载图片')
						img_name = img_url.split('/')[-1]  # 分割图片的链接, 用来做图片名
						img_content = get_img_content(img_url)  # 获取到图片的bytes数据
						down_img(classify_name, men_name, img_name, img_content)  # 下载图片
			else:
				new_detail_url = detail_url + f'/index{i}.html'  # 处理预览页新的url
				detail_urls = get_detail_urls(new_detail_url, detail_html)  # 获取到每个预览详情页的url
				for url in detail_urls:
					print('开始获取图片链接')
					imgs_html = get_html(url)  # 图片页的源码xpath对象
					img_urls = get_img_url(imgs_html, url)  # 获取图片页所有图片的url
					men_name = get_men_name(imgs_html)  # 图片出镜人的名字
					for img_url in img_urls:
						print('开始下载图片')
						img_name = img_url.split('/')[-1]  # 分割图片的链接, 用来做图片名
						img_content = get_img_content(img_url)  # 获取到图片的bytes数据
						down_img(classify_name, men_name, img_name, img_content)  # 下载图片
