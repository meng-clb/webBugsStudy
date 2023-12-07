import scrapy


class Login2Spider(scrapy.Spider):
	name = "login_2"
	allowed_domains = ["17k.com"]
	start_urls = ["https://user.17k.com/ck/user/myInfo/102430995?bindInfo=1&appKey=2406394919"]
	cookies = ('GUID=a36cdad4-a856-4702-8f24-291cf21ba5cb; c_channel=0; c_csc=web; '
	           'accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar'
	           '%252F15%252F95%252F09%252F102430995.jpg-88x88%253Fv%253D1698931480000%26id'
	           '%3D102430995%26nickname%3D%25E7%25A5%259E%25E5%25A5%2587%25E7%259A%2584%25E9%2598'
	           '%25BF%25E6%25A2%25A6%26e%3D1714909208%26s%3D43480568185e8682; '
	           'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22102430995%22%2C%22%24device_id'
	           '%22%3A%2218b9031fce35db-038e785c19353b-26031151-1327104-18b9031fce479e%22%2C'
	           '%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5'
	           '%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host'
	           '%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5'
	           '%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22a36cdad4'
	           '-a856-4702-8f24-291cf21ba5cb%22%7D; '
	           'Hm_lvt_9793f42b498361373512340937deb2a0=1699356351,1700623243,1701942606; '
	           'Hm_lpvt_9793f42b498361373512340937deb2a0=1701947940')

	# 将cookies转化为字典格式, 推导式, 具体实现可查看test.py文件
	cookie_dict = {item.split('=')[0].strip(): item.split('=')[1].strip() for item in
	               (cookies.split(';'))}

	# 重写Spider内的start_requests方法, 直接spider内设置cookie
	def start_requests(self):
		for url in self.start_urls:
			yield scrapy.Request(url, cookies=self.cookie_dict)

	def parse(self, response):
		print(response.text)
