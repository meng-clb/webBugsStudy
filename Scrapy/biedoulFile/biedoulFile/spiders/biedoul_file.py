import scrapy
from ..items import BiedoulfileItem

class BiedoulFileSpider(scrapy.Spider):
	name = "biedoul_file"
	allowed_domains = ["biedoul.com"]
	start_urls = ["https://biedoul.com/wenzi/"]

	def parse(self, response):
		# 实例化
		item = BiedoulfileItem()
		# 使用xpath获取标题
		article_list = response.xpath('//dl[@class="xhlist"]')
		dict_list = []
		for article in article_list:
			dic_data = {}
			# 获取标题
			title = article.xpath('./span//strong/text()').extract_first()
			# 获取内容
			con = article.xpath('./dd/text()').extract()  # 解析所有字符串返回列表
			con = ''.join(con)  # 处理列表为字符串
			item['title'] = title
			item['con'] = con
			yield item
