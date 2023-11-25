# 导包,导入url请求包
from urllib.request import urlopen

url = 'http://www.baidu.com/'

resp = urlopen(url)

# 把抓取到的内容写入到新的文件内
with open("myBaidu.html", "w", encoding="utf-8") as f:
	f.write(resp.read().decode("utf-8")) # 读取到页面的源代码

print('over')
resp.close()