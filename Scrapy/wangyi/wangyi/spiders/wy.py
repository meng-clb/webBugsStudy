import scrapy
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from ..items import WangyiItem


class WySpider(scrapy.Spider):
	name = "wy"
	# allowed_domains = ["news.163.com"]
	start_urls = ["https://news.163.com/"]

	# 创建Chrome无头模式选项
	chrome_options = Options()
	chrome_options.add_argument("--headless")  # 设置无头模式
	chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速

	# 创建Chrome WebDriver并传入无头模式选项
	driver = Chrome(options=chrome_options)

	page_index = [1]  # 获取列表内国内和世界的url下标
	page_urls = []

	def parse(self, response):
		li_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div['
		                         '2]/div/ul/li/a/@href').extract()
		# print(li_list)
		# 将要抓取的页面url存储起来
		for i in range(len(li_list)):
			if i in self.page_index:
				url = li_list[i]
				self.page_urls.append(url)
				yield scrapy.Request(url=url, callback=self.parse_detail)

	def parse_detail(self, response):
		detail_urls = response.xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div['
		                             '1]/div/ul/li/div/div/a/@href').extract()
		print(detail_urls)
		for url in detail_urls:
			yield scrapy.Request(url, callback=self.parse_detail_content)

	def parse_detail_content(self, response):
		item = WangyiItem()
		title = response.xpath('//h1/text()').extract_first()
		con_list = response.xpath('//div[@class="post_body"]/p//text()').extract()
		content = '\n'.join(con_list).strip()
		item['content'] = content
		item['title'] = title
		yield item
