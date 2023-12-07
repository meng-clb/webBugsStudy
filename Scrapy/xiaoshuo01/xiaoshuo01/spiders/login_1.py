import scrapy


class ExampleSpider(scrapy.Spider):
    name = "login_1"
    # allowed_domains = ["17k.com"]
    start_urls = ["https://user.17k.com/ck/user/myInfo/102430995?bindInfo=1&appKey=2406394919"]

    def parse(self, response):
        print(response.text)
