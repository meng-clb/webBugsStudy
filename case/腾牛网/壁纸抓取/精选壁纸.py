from getHomeUrl import *
from lxml import etree

# 获取精选链接列表
dic = get_top_img()

if __name__ == '__main__':
	download_img(dic)
