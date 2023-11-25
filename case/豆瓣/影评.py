import requests
from lxml import etree

"""
'https://movie.douban.com/j/review/15540602/full'15540602
'https://movie.douban.com/j/review/15542317/full'15542317
"""
url = 'https://movie.douban.com/review/best/'

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}
resp = requests.get(url, headers=headers)
html = etree.HTML(resp.text)
# 获取影评的链接
comment_list = html.xpath('//div[@class="short-content"]')
for item in comment_list:
	short_list = item.xpath('./text()')
	if len(short_list) == 3:
		short_comment = str(short_list[1]).strip().split('(')[0]
	else:
		short_comment = str(short_list[0]).strip().split('(')[0]
	comment_id = str(item.xpath('./a/@id')[0]).split('-')[-2]
	# print(comment_id, short_comment)

	comment_url = f'https://movie.douban.com/j/review/{comment_id}/full'
	res = requests.get(comment_url, headers=headers)
	comment = res.json()['html']
	html = etree.HTML(comment)
	info = html.xpath('string(.)')
	print(info)
	break
