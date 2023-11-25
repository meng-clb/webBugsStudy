# 1. 获取网页源代码
# 2. 通过源码处理解析数据
import requests
from lxml import etree

url = 'https://www.zbj.com/fw/?k=cps'
resp = requests.get(url)
html = etree.HTML(resp.text)
div_list = html.xpath('/html/body//div[@class="search-result-list-service"]/div/div')

for div in div_list:
	com_name = div.xpath('./a/div[2]/div/div/text()')[0]
	price = div.xpath('.//div[@class="price"]/span/text()')[0].strip('¥')
	title = 'cps'.join(div.xpath('.//div[@class="name-pic-box"]/a/text()'))

	print(com_name, price, title)