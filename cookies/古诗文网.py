import base64
import json
import requests


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


def get_code(session, url, headers, path):
	"""
	获取到验证码图片
	:param session: 实例化session对象
	:param url: 获取到的验证码图片地址
	:param headers: 传递头
	:param path: 保存位置
	:return: 无
	"""
	resp = session.get(url, headers=headers)

	# 下载验证码图片
	with open(path, 'wb') as f:
		f.write(resp.content)


def login():
	"""
	调用函数, 直接登录
	:return:
	"""
	headers = {
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/119.0.0.0 Safari/537.36'
	}

	# 实例化session对象
	session = requests.Session()
	img_path = "yzm.jpg"
	# 获取到验证码的url
	code_url = 'https://so.gushiwen.cn/RandCode.ashx?t=1699363129582'
	get_code(session, code_url, headers, img_path)
	# 验证码识别
	result = base64_api(uname='ameng011022', pwd='密码(qq账号)', img=img_path, typeid=3)
	print(result)

	from_data = {
		'__VIEWSTATE': 'sNnAs7JxUrjVnSqQA/km8NMxBYfK6QhHeAB4ozBf'
		               '+1L6aLQ5C7rO1k3mhUlZanvSHfEkoGJE8gYdBq0bE0ZEHgkRNYOQhIVTk9t9bs3xC59LVx'
		               '+7DPO35mr2VLSHkXf'
		               '+yyZmb33uZHABPcmfDgINjCuzPJE=',
		'__VIEWSTATEGENERATOR': 'C93BE1AE',
		'from': '',
		'email': '1419148453@qq.com',
		'pwd': '1419148453',
		'code': result,
		'denglu': '登录',
	}

	log_url = 'https://so.gushiwen.cn/user/login.aspx'
	resp = session.post(log_url, headers=headers, data=from_data)
	with open('login.html', 'w', encoding='utf-8') as f:
		f.write(resp.content.decode())


if __name__ == "__main__":
	# TODO 图鉴:http://www.ttshitu.com/docs/python.html,验证码验证平台
	login()