import scrapy
from ..items import JianshiItem


class GaoxiaoSpider(scrapy.Spider):
	name = "gaoxiao"
	# allowed_domains = ["6jianshi.com"]
	start_urls = ["https://www.6jianshi.com/zuiguo/hot-0/pic-0/page-1"]

	def parse(self, response):
		# https://www.6jianshi.com/zuiguo/hot-0/pic-0/page-2
		# https://www.6jianshi.com/zuiguo/hot-0/pic-0/page-3
		for i in range(1, 11):
			# 对网站进行分页请求
			url = f'https://www.6jianshi.com/zuiguo/hot-0/pic-0/page-{i}'
			yield scrapy.Request(url, callback=self.parse_detail, meta={'url': url})

	def parse_detail(self, response):
		# 获取详情页的数据
		art_list = response.xpath('//div[@class="art-list"]')
		for art in art_list:
			item = JianshiItem()
			url = response.meta.get('url')
			# print(url)
			content = art.xpath('./div[@class="art-list-content"]/a/text()').extract_first()
			print(url, content)
			item['content'] = content
			yield item
