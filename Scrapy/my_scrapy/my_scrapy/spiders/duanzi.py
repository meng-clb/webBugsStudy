import scrapy


class DuanziSpider(scrapy.Spider):
    name = "duanzi"  # 爬虫名称
    # allowed_domains = ["duanzi.cn"]  # 只爬取的域名
    start_urls = ["https://duanzi.cn"]  # 开始爬取的网站

    def parse(self, response):
        print(response.text)
