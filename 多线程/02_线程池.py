from concurrent.futures import ThreadPoolExecutor
import requests
import csv

# 使用线程池爬取新发地的菜价列表

url = 'http://www.xinfadi.com.cn/getPriceData.html'
page_num = 0
param = {
	'limit': 20,
	'current': {page_num}
}

f = open('vegetable.csv', 'w', encoding='utf-8')
csv_write = csv.writer(f)


def download(p):
	print(url)
	resp = requests.post(url, data=p)
	vege_list = resp.json()['list']
	for item in vege_list:
		csv_write.writerow(list(item.values())[1:-7])

	resp.close()


if __name__ == '__main__':
	# 开辟线程池, 在线程池内使用20个线程数
	with ThreadPoolExecutor(20) as t:
		# 爬取的页数
		for i in range(1, 20):
			print(f'爬取完成第{page_num}页')
			page_num = page_num + 1
			param['current'] = page_num
			t.submit(download, param)
