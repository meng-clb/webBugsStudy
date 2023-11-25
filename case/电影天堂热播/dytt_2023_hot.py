"""
1. 从首页获取要抓取的部分
2. 从抓取的部分获取子页面链接
3. 从子页面中抓取需要的数据
"""
import requests
import re
import csv

mainUrl = 'https://dytt89.com/'
# 获取到需要抓取的模块
reObj1 = re.compile(r"2023必看热片.*?<ul>(?P<ul>.*?)</ul>", re.S)
# 抓取模块每条数据
re_href = re.compile(r"<li><a href='(?P<href>.*?)' title", re.S)
# 抓取子页面的电影名称和下载地址
re_download = re.compile(
	r'title_all.*?<h1>(?P<name>.*?)</h1></div>.*?<tr>.*?<td style="WORD-WRAP: break-word" '
	r'bgcolor="#fdfddf"><a href="(?P<download>.*?)">magnet',
	re.S)
headers = {
	"User-Agent":
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
		"Chrome/118.0.0.0 "
		"Safari/537.36"
}
resp = requests.get(mainUrl, headers=headers)
resp.encoding = 'gb2312'
result = reObj1.finditer(resp.text)
# 子页面的链接列表
child_href_list = []
for it in result:
	# 获取到模块下所有的li数据
	href = re_href.finditer(it.group())
	for child in href:
		# 获取子页面的链接, 组装链接, 将子页面的链接放到列表内
		child_href = mainUrl + child.group('href').strip('/')
		child_href_list.append(child_href)

resp.close()

# 通过每个子页面的链接去抓取需要的数据
f = open('dytt_2023hot', 'w', encoding='utf-8')
dyttwrite = csv.writer(f)
for it in child_href_list:
	child_table = requests.get(it, headers=headers)
	child_table.encoding = 'gb2312'
	child_table_data = child_table.text
	download = re_download.finditer(child_table_data)
	for dw in download:
		dic = dw.groupdict()
		dyttwrite.writerow(dic.values())
		# print(dw.group('name'))
		# print(dw.group('download'))

child_table.close()
f.close()

print('over')