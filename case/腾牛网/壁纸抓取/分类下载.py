from getHomeUrl import *

lis = select_classify()

for item in lis:
	download_img(item)