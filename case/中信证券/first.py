"""
url = 'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index.html'
1. 正常抓取每一行数据
2. 可以抓取多页
3. 变成可以手动输入页码, 并且判断当前页面是否大于1页, 以及 不超出最大页面
"""

import requests
from lxml import etree
num_page = 1
url = 'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index.html'
url_page = f'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index_{num_page}.html'
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
html = etree.HTML(resp.text)
lis = html.xpath('//ul[@class="list-con"]/li')
for li in lis:
	li_content = li.xpath('./span/text()')
	print(li_content)