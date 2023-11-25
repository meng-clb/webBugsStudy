import os.path
import requests
from multiprocessing import Pool
from lxml import etree

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}


def get_img_list(page):
	"""
	获取页面所有图片的链接
	:param page: 抓取到第几页
	:return:
	"""
	for i in range(1, page + 1):
		url = f'https://www.pkdoutu.com/zz/list?page={i}'
		resp = requests.get(url, headers=headers)
		html = etree.HTML(resp.content.decode())
		# 获取所有图片的链接
		print(f'获取第{i}页链接')
		img_list = html.xpath('//div[@class="page-content"]/a/img/@data-backup')
		# 利用生成器, 调用一次, 提供一个页面的链接
		yield img_list


def download_img(src_list):
	"""
	传入页面图片的链接, 下载图片
	:param src_list: 页面的所有链接
	:return:
	"""
	path = 'img'
	if not os.path.exists(path):
		os.mkdir(path)
	for src in src_list:
		img_name = str(src).split('_')[-1]
		print(img_name)
		res = requests.get(src)
		with open(os.path.join(path, img_name), 'wb') as f:
			f.write(res.content)


if __name__ == '__main__':
	# 创建进程池
	pool = Pool(5)  # 启用的进程数
	pool.map(download_img, get_img_list(5))
	print('over')
