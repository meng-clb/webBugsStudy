import scrapy
from urllib.parse import urljoin

class ImgSpider(scrapy.Spider):
	name = "img"
	# allowed_domains = ["desk.zol.com.cn"]
	start_urls = ["https://desk.zol.com.cn/dongman/"]

	def parse(self, response):
		# 获取请求页的图片详情页链接
		detail_href = response.xpath('//ul[@class="pic-list2  clearfix"]/li/a/@href').extract()
		# print(detail_href)
		for href in detail_href:
			# 排除不是图片详情页的混淆链接
			if href.find('exe') != -1:
				continue
			# 拼接详情页的链接
			detail_url = urljoin('https://desk.zol.com.cn/dongman/', href)
			# print(detail_url)
			yield scrapy.Request(detail_url, callback=self.parse_detail)

	def parse_detail(self, respone):
		img_href = respone.xpath('//dd[@id="tagfbl"]/a/@href').extract()
		# print(img_href)
		if len(img_href) > 1:
			# 拼接详情页的链接
			img_url = urljoin('https://desk.zol.com.cn/dongman/', img_href[0])
			# print(img_url)
			# 传递Referer
			yield scrapy.Request(img_url, callback=self.parse_img, meta={'Referer': respone.url})

	def parse_img(self, respone):
		# 获取最终大图的url, 通过这个uel下载图片到本地
		down_url = respone.xpath('//img[1]/@src').extract_first()
		print(down_url)
		yield {'img_urls': down_url}

