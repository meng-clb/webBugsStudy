import base64
import json
import requests


# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
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

# TODO 图鉴:http://www.ttshitu.com/docs/python.html
if __name__ == "__main__":
	headers = {
		'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
			'Chrome/119.0.0.0 Safari/537.36'
	}

	# 实例化session对象
	session = requests.Session()

	# 获取到验证码的url
	code_url = 'https://so.gushiwen.cn/RandCode.ashx?t=1699363129582'
	resp = session.get(code_url, headers=headers)
	img_path = "yzm.jpg"
	# 下载验证码图片
	with open(img_path, 'wb') as f:
		f.write(resp.content)
	# 验证码识别
	result = base64_api(uname='账号(ameng011022)', pwd='密码(qq账号)', img=img_path, typeid=3)
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
