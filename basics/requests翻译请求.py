import requests

url = 'https://fanyi.baidu.com/sug'

word = input('请输入要翻译的单词: ')

dat = {
	"kw": word
}

# 使用post请求, 发送的数据必须放在字典内, 通过data参数进行传递
resp = requests.post(url, data=dat)

print(resp.json())  # 将服务器传回来的内容输出为json格式
resp.close()
