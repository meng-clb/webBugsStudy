import scrapy
from scrapy import Request
from ..items import DoubanItem


class DoubanMysqlSpider(scrapy.Spider):
	name = "db"
	# allowed_domains = ["movie.douban.com"]
	start_urls = ["https://movie.douban.com/chart"]

	def parse(self, response):
		# 实例化对象
		item = DoubanItem()
		url_list = response.xpath('//div[@class="indent"]//table/tr[@class="item"]//div['
		                          '@class="pl2"]/a/@href').extract()

		# print(url_list)
		# 获取到每个电影详情页页面的url
		for url in url_list:
			# 创建request对象, 发起请求到详细链接, 并指定回调函数处理下一页页面
			yield Request(url, callback=self.parse_detail)

	def parse_detail(self, response):
		item = DoubanItem()
		# 获取电影名字
		name = ''.join(response.xpath('//h1//text()').extract()).replace(' ' and '\n', '').strip()
		# 获取电影图片的地址
		img_src = response.xpath('//div[@id="mainpic"]//img/@src').extract_first()
		# 获取主演
		actor = response.xpath('//div[@id="info"]//span[@class="actor"]//span['
		                       '@class="attrs"]//a/text()').extract()
		# print(name)
		# print(img_src)
		# print(actor)
		# print('--------------')

		item['img_src'] = img_src
		item['name'] = name
		item['actor'] = actor
		# break
		yield item
