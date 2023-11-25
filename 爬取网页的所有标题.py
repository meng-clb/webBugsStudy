import requests
from lxml import etree

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/119.0.0.0 Safari/537.36'
}

url = 'http://bbs.chinaunix.net/'

resp = requests.get(url, headers=headers)
# print(resp.content.decode('gbk'))
html = etree.HTML(resp.content.decode('gbk'))
# 获取到前5个div模块, 每个模块内包含了标题
divs = html.xpath('//div[@class="mn"]/div[position()<=5]')

date = {}  # 存储数据
num = 1
for div in divs:
	# 获取到模块内的每一行
	tr_list = div.xpath('./table/tbody[2]/tr')
	for tr in tr_list:
		title = []
		# 获取到每一行的td, td内包含了数据
		td_list = tr.xpath('./td')
		for td in td_list:
			# 从每个td中拿出数据进行保存
			name = td.xpath('.//td[@class="bold subject"]/a/text()')
			title.append(name)
		date[f'第{num}行'] = title
		num += 1

print(date)