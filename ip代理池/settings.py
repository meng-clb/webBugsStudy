"""
当前项目全局配置文件
"""
HOST = '127.0.0.1'  # 链接主机ip地址
PORT = 6379  # 端口
PASSWORD = 'root'  # 密码
REDIS_NAME = 'proxy_ip'  # redis库的名称
SCORE = 100  # ip的权重
MIN_SCORE = 50