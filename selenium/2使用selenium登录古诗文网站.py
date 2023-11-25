import base64
import json
import requests
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


# 打码平台使用
def base64_api(uname, pwd, img, typeid):
	with open(img, 'rb') as f:
		base64_data = base64.b64encode(f.read())
		b64 = base64_data.decode()
	data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
	result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
	if result['success']:
		return result["data"]["result"]
	else:
		# ！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
		return result["message"]
	return ""


# 实例化谷歌浏览器驱动
web = Chrome()

web.get('https://www.gushiwen.cn/')
time.sleep(2)

username = '1419148453@qq.com'
password = '1419148453'
# 点击我的标签, 到登录界面
web.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/a[6]').click()
time.sleep(2)
# 获取用户名节点并输入用户名
web.find_element(By.ID, 'email').send_keys(username)
# 获取密码节点并输入密码
web.find_element(By.ID, 'pwd').send_keys(password)
# 获取验证码图片, 并将验证码图片保存起来
img_path = 'code.png'
web.find_element(By.ID, 'imgCode').screenshot(img_path)
# 验证码识别
result = base64_api(uname='账号(ameng011022)', pwd='密码(qq账号)', img=img_path, typeid=3)
# 获取到验证码节点, 并输入验证码
web.find_element(By.ID, 'code').send_keys(result)
# 获取到登录节点并点击登录
web.find_element(By.ID, 'denglu').click()

# 获取到cookies
cookies = web.get_cookies()
json_cookies = json.dumps(cookies)
print(json_cookies)
with open('json_cookies.txt', 'w', encoding='utf-8') as f:
	f.write(json_cookies)
web.close()
time.sleep(100)


