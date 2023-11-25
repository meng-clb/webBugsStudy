import re

txt = '我的电话号码是: 10086, 你的号码是: 10010'

# search只匹配到第一个符合条件的就返回, 返回一个match对象, 拿到数据用.group()
# res = re.search(r"\d+", txt)
# print(res.group())

# findall查找到所有符合条件的, 返回一个列表
# lis = re.findall(r'\d+', txt)
# print(lis)

# finditer查找到所有符合条件的, 返回一个迭代器, 速度比findall好一点, 迭代器中那数据需要.group()
# res = re.finditer(r'\d+', txt)
# print(res)
# for it in res:
# 	print(it.group())

# match从开头开始匹配,若没有匹配到, 则返回none
# res = re.match(r'\d+', txt)
# print(res)

# 预加载正则表达式
# obj = re.compile(r'\d+')
#
# it = obj.finditer(txt)
# print(it)
# for it in it:
# 	print(it.group())


s = """
<div class='jolin'><span id='3'>大聪明</span></div>
<div class='syLar'><span id='4'>范思哲</span></div>
<div class='tory'><span id='5'>胡说八道</span></div>
"""

# (?P<群组名>正则) 可以通过群组名单独的拿出来数据
obj = re.compile(r"<div class='(?P<english>.*?)'><span id='(?P<id>\d+)'>(?P<name>.*?)</span></div>",
                 re.S)  # re.S让.可以匹配空行

result = obj.finditer(s)
for it in result:
	print(it.group('name'))
	print(it.group('id'))
