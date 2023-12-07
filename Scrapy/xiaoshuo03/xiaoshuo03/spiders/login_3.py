import scrapy


class Login3Spider(scrapy.Spider):
	name = "login_3"
	# allowed_domains = ["17k.com"]
	start_urls = ["https://user.17k.com/ck/user/myInfo/102430995?bindInfo=1&appKey=2406394919"]

	def start_requests(self):
		# 重写start_requests方法, 通过body传递账号密码进行登录, 获取到cookies
		login_url = 'https://passport.17k.com/ck/user/login'
		# yield scrapy.Request(login_url, method='post',
		#                      body='loginName=19713055472&password=Clb12345',
		#                      callback=self.log_in)
		form_data = {
			'loginName': ' 19713055472',
			'password': 'Clb12345'
		}
		# 直接通过FormRequest进行请求, 默认为post请求
		yield scrapy.FormRequest(login_url, formdata=form_data, callback=self.log_in)

	def log_in(self, respone):
		# print(respone.text)
		for url in self.start_urls:
			yield scrapy.Request(url)

	def parse(self, response):
		print(response.text)
