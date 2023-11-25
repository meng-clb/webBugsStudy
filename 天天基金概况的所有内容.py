import requests
from lxml import etree

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'http://fundf10.eastmoney.com/jbgk_004400.html'

resp = requests.get(url, headers=headers)
html = etree.HTML(resp.content.decode())
# 获取基本概述的所有行信息
basic_tr = html.xpath('//div[@class="txt_in"]/div[1]//tr')
info = {}
for tr in basic_tr:
	# 拿到所有标题和内容
	th = tr.xpath('./th')
	td = tr.xpath('./td')
	for h, d in zip(th, td):
		# 拿到每一个标题和对应的内容
		title = h.xpath('./text()')[0]
		print(title)
		body = d.xpath('./text()')
		info[title] = body

print(info)

