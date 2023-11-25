import json
import time

from selenium.webdriver import Chrome

web = Chrome()
web.get('https://so.gushiwen.cn/user/collect.aspx')

with open('json_cookies.txt', 'r') as f:
	cookies = json.loads(f.read())

# 添加cookie
for cookie in cookies:
	cook_dict = {}
	for k, v in cookie.items():
		cook_dict[k] = v
	web.add_cookie(cook_dict)
# 刷新网页
web.refresh()
web.get('https://so.gushiwen.cn/user/collect.aspx')
time.sleep(20)