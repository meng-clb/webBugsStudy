import scrapy


class BiedouSpider(scrapy.Spider):
	name = "biedou"
	# allowed_domains = ["biedoul.com"]  # 要抓取的域名
	start_urls = ["https://biedoul.com/wenzi/"]  # 爬虫起始网站

	def parse(self, response):
		# 使用xpath获取标题
		article_list = response.xpath('//dl[@class="xhlist"]')
		dict_list = []
		for article in article_list:
			# extract() 解析所有的字符串返回列表
			# title = article.xpath('./span//strong/text()').extract()
			# extract_first() == element[0].extract() 解析第一个对象返回字符串
			# title = article.xpath('./span//strong/text()')[0].extract()
			dic_data = {}
			# 获取标题
			title = article.xpath('./span//strong/text()').extract_first()
			# 获取内容
			con = article.xpath('./dd/text()').extract()  # 解析所有字符串返回列表
			con = ''.join(con)  # 处理列表为字符串
			dic_data['title'] = title
			dic_data['con'] = con
			yield dic_data
		# print(title)
		# print(con)
		# print('---------------')

# def parse(self, response):
# 获取解析后的页面源代码
# print(response.text)
# bytes
# print(response.body)
# 获取响应的url地址
# print(response.request.url)
# 获取响应头
# print(response.headers)
# # 获取响应的请求头
# print(response.request.headers)
# # 响应状态码
# print(response.status)
