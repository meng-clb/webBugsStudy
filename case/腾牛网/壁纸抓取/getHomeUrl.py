import os
import requests
from lxml import etree

# 首页主页面
url = 'https://www.qqtn.com/pf/'

# 图片页面, 需要拼接使用
img_url = 'https://www.qqtn.com'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


# 传递链接,抓取此链接的html
def resp_get(url: str):
	resp = requests.get(url, headers=headers)
	resp.encoding = 'gbk'
	return resp.text


# 创建文件夹
def mkdir_name(name: str):
	path = name
	if not os.path.exists(path):
		os.mkdir(path)


# 通过链接下载图片
def download_img(dic: dict):
	"""
	调用获取链接函数得到一个dic字典， 将dic字典如函数内
	:param dic:
	:return:
	"""
	for key, value in dic.items():
		mkdir_name(key)
		print(value)
		resp = resp_get(value)
		html = etree.HTML(resp)
		# 获取到页面内所有的壁纸链接
		p_list = html.xpath('//div[@id="zoom"]/p')[1:]
		for p in p_list:
			# 通过链接将图片下载到本地
			img_url = p.xpath('./img/@src')[0]
			img_name = str(img_url).split('/')[-1]
			# key: 文件名
			with open(os.path.join(key, img_name), 'wb') as f:
				res = requests.get(img_url)
				f.write(res.content)
			print('已抓取图片+1')
		print(f'{key}列表抓取完成')


html = etree.HTML(resp_get(url))


# 抓取top精选的壁纸
def get_top_img():
	"""
	获取首页推荐的壁纸
	mk_name:壁纸的名字 -> 文件夹名字 img_a: 壁纸的链接地址,通过链接直接下载图片
	:return: 返回一个字典,抓取到的数据放到一个字典内进行返回
	"""
	lis = html.xpath('//div[@class="g-dome-bd"]/ul/li')
	dic = {}
	for li in lis:
		mk_name = li.xpath('./a/@title')[0]
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		dic[mk_name] = img_a
	return dic


# 获取top精选的列表
def get_top_list():
	"""
	获取top精选的列表内所有的链接
	img_name: 标题 -> 文件夹名
	img_a: 壁纸所在链接
	:return: dic字典, 标题和链接
	"""
	li_list = html.xpath('//div[@class="g-topcms g-topcms2020 f-fl"]/ul/li')
	dic = {}
	for li in li_list:
		img_name = li.xpath('./a/text()')[0]
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		dic[img_name] = img_a
	return dic


# 获取排行榜
def get_list():
	"""
	获取排行榜的周榜链接,并抓取出来
	:return:
	"""
	week_list = html.xpath('//div[@class="g-rank-bd"]/div')[0].xpath('./ul/li')
	dic = {}
	for li in week_list:
		img_name = li.xpath('./a/text()')[0]
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		dic[img_name] = img_a

	return dic


# 获取皮肤精选
def get_handpick():
	"""
	获取皮肤精选的所有链接
	:return:
	"""
	lis = html.xpath('//div[@class="g-headimg-dome"]/div/ul/li')
	dic = {}
	for li in lis:
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		img_name = li.xpath('./a/text()')[0]
		dic[img_name] = img_a
	return dic


# 获取到所有的壁纸分类
def get_classify():
	"""
	获取首页中所有的分类标签, 把分类标签放到字典返回
	可直接通过字典去调用.xpath继续往下寻找需要的元素
	:return:
	"""
	classify = html.xpath('//div[@class="g-cont-box g-main-bg clearfix g-box-1200 m-margin15"]')
	dic = {}
	for item in classify:
		title = item.xpath('./h4/em/text()')[0]
		# print(item)
		dic[title] = item
	return dic


# 分类左侧展示壁纸链接获取
def get_left_img(name: str):
	"""

	:param name: 通过选择分类, 将分类的名字传入
	:return:
	"""
	classify_dic = get_classify()
	left_img = classify_dic[name].xpath('./div/div[@class="m-contpf-img f-fl"]/ul/li')
	dic = {}
	for li in left_img:
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		img_name = li.xpath('./a/@title')[0]
		dic[img_name] = img_a
	return dic


# 获取分类右侧的列表链接
def get_right_list(name: str):
	"""

	:param name: 通过选择分类, 将分类的名字传入
	:return:
	"""
	classify_dic = get_classify()
	right_list = classify_dic[name].xpath(
		'./div/div[@class="m-cont-right g-rank-li f-fr"]/ul/li')
	dic = {}
	for li in right_list:
		a = li.xpath('./a/@href')[0]
		img_a = img_url + str(a)
		img_name = li.xpath('./a/@title')[0]
		dic[img_name] = img_a
	return dic


# 选择下载的分类
def select_classify():
	"""
	通过打印的列表选择一个要下载的分类
	:return: 左侧的链接和右侧的链接
	"""
	print_classify()
	classify_name = input('请输入要下载的分类: ')
	# 将一个分类中的左侧展示和右侧的排行榜同时下载
	left_list = get_left_img(classify_name)
	right_list = get_right_list(classify_name)
	return left_list, right_list


# 调用分类获取函数, 将分类获取的标题给打印出来
def print_classify():
	"""
	打印所有的分类列表
	"""
	classify_dic = get_classify()
	classify_list = []
	for key in classify_dic:
		classify_list.append(key)
	print(classify_list)


