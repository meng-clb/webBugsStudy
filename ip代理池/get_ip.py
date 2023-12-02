"""
获取代理ip
"""
import time
import requests
from lxml import etree
from proxy_redis import ProxyRedis

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36',
	'Cookie':
		'https_waf_cookie=aa2f1f63-7313-4d68fad37cceb6d7c8a3553ab8810933f0e8; '
		'Hm_lvt_f9e56acddd5155c92b9b5499ff966848=1701439420; '
		'Hm_lpvt_f9e56acddd5155c92b9b5499ff966848=1701439420'
}


def get_ip(url):
	"""
	通过url获取当前页面的所有ip
	:param url: ip代理页面
	:return: 当前页面处理后的ip
	"""
	p_r = ProxyRedis()
	resp = requests.get(url, headers=headers)
	html = resp.text
	# with open('ip.html', 'r', encoding='utf-8') as f:
	# 	html = f.read()
	html = etree.HTML(html)
	ip_list = html.xpath(
		'//table[@class="layui-table"]/tbody/tr/td[1]/text()|//table['
		'@class="layui-table"]/tbody/tr/td[2]/text()')
	# 将每页的每个ip和端口进行拼接处理
	for i in range(0, len(ip_list), 2):
		ip = str(ip_list[i]).strip() + ':' + str(ip_list[i + 1]).strip()
		print(ip)
		p_r.zset_zadd(ip)  # ip添加到redis有序集合中


def get_all_ip(page=1, end=30):
	"""
	循环获取所有页面的ip, 默认抓取30页
	:param page: 当前抓取ip的页数
	:param end: 要抓取的免费ip代页数
	"""
	while True:
		url = f'https://www.89ip.cn/index_{page}.html'
		try:
			time.sleep(30)
			get_ip(url)
			if page >= end:
				break
			else:
				page += 1
		except Exception as e:
			print(f'已抓取{page}页代理, 如未达到你的目标, 请检查代码或者重新抓取')
			print(e)
			break


if __name__ == '__main__':
	get_ip('url')
