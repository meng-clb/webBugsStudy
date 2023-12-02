"""
py的web框架
请求文件接口, 返回可用ip
"""
# pip install flask
from flask import Flask
from proxy_redis import ProxyRedis

# 实例化flask类
app = Flask(__name__)


# http://127.0.0.1:5000/
# @app.route('/get_ip/')
@app.route('/')
def index():
	p_r = ProxyRedis()
	# 获取一个可用性较高的ip
	ip = p_r.get_ip()
	if ip:
		return ip
	return 'ip不可用'


# 只要调用run 就可以运行当前的flask框架
def run():
	app.run()  # 运行flask


if __name__ == '__main__':
	app.run()  # 运行flask
