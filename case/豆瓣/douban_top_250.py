import requests
import re
import csv

f = open('douban_top_250_data.csv', 'w', encoding='utf-8')
csvwrite = csv.writer(f)
# 'https://movie.douban.com/top250?start=25&filter='

headers = {
	"User-Agent":
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 "
		"Safari/537.36"
}

# 获取数据的正则
reobj = re.compile(
	r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<br>(?P<year>.*?)&nbsp;.*?<span '
	r'class="rating_num" property="v:average">(?P<score>.*?)</span>.*?<span>(?P<num>.*?)人评价</span>', re.S)

start = 0
for x in range(6):
	url = f'https://movie.douban.com/top250?start={start}'
	# 拿到网页的数据
	resp = requests.get(url, headers=headers)
	data = resp.text
	# 对数据进行解析获取
	result = reobj.finditer(data)
	for it in result:
		# 将数据生成一个字典
		dic = it.groupdict()
		dic['year'] = dic['year'].strip()
		csvwrite.writerow(dic.values())
	x = x + 1
	start = start + 25
	resp.close()

# 抓取一页数据
# for it in result:
# 	# print(it.group('name'))
# 	# print(it.group('score'))
# 	# print(it.group('num'))
# 	# print(it.group('year').strip())
# 	# 将数据生成一个字典
# 	dic = it.groupdict()
# 	dic['year'] = dic['year'].strip()
# 	csvwrite.writerow(dic.values())

f.close()
print('over')
