import requests
import json
import re

headers = {
	'Referer': 'http://www.sse.com.cn/',
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
}

# 数据展示的url
data_url = 'http://query.sse.com.cn/commonSoaQuery.do'

params = {
	'jsonCallBack': 'jsonpCallback13267574',
	'isPagination': 'true',
	'pageHelp.pageSize': 25,
	'pageHelp.pageNo': 2,  # 当前页
	'pageHelp.beginPage': 2,  # 从第几页显示数据
	'pageHelp.cacheSize': 1,
	'pageHelp.endPage': 1,
	'sqlId': 'BS_KCB_GGLL',
	'siteId': 28,
	'channelId': '10743,10744,10012',
	'order': 'createTime|desc,stockcode|asc',
	'_': '1702437855386'
}

page_count = 20  # 数据一共多少页


# 获取页面数据
def get_data(url, headers, params, page_count):
	"""
	获取页面数据
	:param url: 要抓取页面的url
	:param headers:  请求头
	:param params: 传递参数, 主要用来改变页面显示的数据
	:param page_count: 数据一共有多少页
	"""
	for i in range(1, page_count):
		params['pageHelp.pageNo'] = i  # 改变获取那页数据
		params['pageHelp.beginPage'] = i  # 页面数据开始显示的页数
		resp = requests.get(url, headers=headers, params=params)
		# print(resp.text)
		obj = re.compile('\((?P<text>.*)\)', re.S)
		result = obj.findall(resp.text)
		# print(result[0])
		print(f'第{i}页数据')
		datas = json.loads(result[0])['result']
		# print(datas)
		write_data(datas)


"""
extSECURITY_CODE    公司代码
extGSJC             公司简称
createTime          发函日期
extWTFL             监管问询类型
docTitle            标题
docURL              标题文档url, pdf, doc
"""


# 把数据写入到csv文件内
def write_data(datas):
	"""
	把数据写入到csv文件内
	:param datas: 数据列表, 列表内是对象
	"""
	for data in datas:
		# print(type(data))
		gs_code = data['extSECURITY_CODE']  # 公司简称
		gs_jc = data['extGSJC']  # 公司简称
		createTime = str(data['createTime']).split(' ')[0]  # 发函日期
		extWTFL = data['extWTFL']  # 监管问询类型
		title = data['docTitle']  # 标题
		url = data['docURL']  # 标题文档url
		# print(gs_code, gs_jc, createTime, extWTFL, title, url)
		with open('shanghai.csv', 'a', encoding='utf-8') as f:
			f.write(gs_code)
			f.write(',')
			f.write(gs_jc)
			f.write(',')
			f.write(createTime)
			f.write(',')
			f.write(extWTFL)
			f.write(',')
			f.write(title)
			f.write(',')
			f.write(url)
			f.write('\n')


if __name__ == '__main__':
	get_data(data_url, headers, params, page_count)