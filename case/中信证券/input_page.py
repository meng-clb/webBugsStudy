"""
url = 'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index.html'
1. 正常抓取每一行数据
2. 可以抓取多页
3. 变成可以手动输入页码, 并且判断当前页面是否大于1页, 以及 不超出最大页面
"""

import requests
from lxml import etree

num_page = 1
url = 'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index.html'  # 首页url
url_page = f'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index_{num_page}.html'
headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}
num_page = int(input('输入你要抓取的页码(2-101):'))
if num_page < 2 or num_page > 101:
	print('输入不合法, 请重新运行代码')
else:
	url_page = f'http://www.cs.ecitic.com/newsite/cpzx/jrcpxxgs/zgcp/index_{num_page-1}.html'
	resp = requests.get(url_page, headers=headers)
	resp.encoding = 'utf-8'
	html = etree.HTML(resp.text)
	lis = html.xpath('//ul[@class="list-con"]/li')
	for li in lis:
		li_content = li.xpath('./span/text()')
		print(li_content)
	print(f'------------------第{num_page}页数据抓取完成----------------------')
