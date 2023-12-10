import requests
from lxml import etree
from urllib.parse import urljoin

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


if __name__ == '__main__':
	# 秀人集首页url
	home_url = 'https://www.xr06.xyz/'
	home_html = get_html(home_url)
	menu_urls = get_menu_urls(home_html, home_url)
	for url in menu_urls:
		html = get_html(url)
		page_count = get_detail_page(html)
		for i in range(1, page_count):
			if i == 1:
				# print(url)
				html = get_html(url)
				detail_urls = get_detail_urls(url, html)
				print(f'{url}页面的链接: {detail_urls}')
				for detail_url in detail_urls:
					# print(detail_url)
					html = get_html(detail_url)
					img_urls = get_img_url(html, detail_url)
					for img_url in img_urls:
						resp = requests.get(img_url, headers=headers)
						name = img_url.split('/')[-1]
						print(f'开始保存{img_url}页面的图片')
						with open('img/' + name, 'wb') as f:
							f.write(resp.content)
					# break
			else:
				# new_url = f'{url}/index{i}.html'
				# # print(new_url)
				# html = get_html(new_url)
				# detail_urls = get_detail_urls(url, html)
				# print(f'{new_url}页面的链接: {detail_urls}')
				# for detail_url in detail_urls:
				# 	# print(detail_url)
				# 	html = get_html(detail_url)
				# 	get_img_url(html, detail_url)
				# 	break
				pass
		break
