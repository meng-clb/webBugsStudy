import subprocess
from functools import partial  # 作用, 用来锁定某个参数的固定值

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs  # 用的是node.js
import requests
import json

headers = {
	'User-Agent':
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/120.0.0.0 Safari/537.36'
}

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='


# 获取当前评论函数
def get_user_content(comment):
	"""
	获取当前评论函数
	:param comment: 页面数据对象
	:return: 每个用户的信息
	"""
	user = comment['user']['nickname']  # 用户名
	content = comment['content']  # 评论内容
	times = comment['timeStr']  # 评论时间
	ip = comment['ipLocation']['location']  # 用户ip
	userId = comment['ipLocation']['userId']  # 用户id
	user_dic = {
		'user': user,
		'content': content,
		'times': times,
		'ip': ip,
		'userId': userId
	}
	return user_dic


# 获取以前的评论
def get_be_user_content(comment):
	"""
	获取以前的评论
	:param comment:  页面数据对象
	:return:每个用户的信息
	"""
	user = comment['beReplied'][0]['user']['nickname']  # 用户名
	content = comment['beReplied'][0]['content']  # 评论内容
	ip = comment['beReplied'][0]['ipLocation']['location']  # 用户ip
	userId = comment['beReplied'][0]['ipLocation']['userId']  # 用户id
	be_user_dic = {
		'user': user,
		'content': content,
		'ip': ip,
		'userId': userId
	}
	return be_user_dic


# 输出所有的评论
def print_content(comments):
	"""
	输出所有的评论
	:param comments: 当前的评论页抓取到的数据对象
	:return:
	"""
	for comment in comments:
		if comment['beReplied'] is not None:  # 回复的评论
			user_dic = get_user_content(comment)  # 回复的评论
			be_user_dic = get_be_user_content(comment)  # 以前的评论
			print(f'\n-----{be_user_dic["user"]}的评论-----\n')
			print(be_user_dic['content'])
			print(
				f'\n--------{user_dic["user"]} {user_dic["times"]} {user_dic["ip"]} '
				f'{user_dic["userId"]}回复{be_user_dic["user"]}---------\n')
			print(user_dic['content'])
		else:
			user_dic = get_user_content(comment)
			print(f'\n-------{user_dic["user"]} {user_dic["times"]} {user_dic["ip"]} '
			      f'{user_dic["userId"]}-------------\n')
			print(user_dic['content'])


# 获取页面的评论
def get_comments():
	"""
	获取页面的评论, 输出评论
	:return:
	"""
	page_num = 1  # pageNo -> 评论页码
	song_id = 2071935674  # 歌曲ID, 通过这个ID获取这首歌的评论
	cursor = -1  # 初始化游标, 后续的参数由上一页返回的cursor
	page_sum = 5  # 要抓取的页数

	for i in range(page_sum):
		data = {
			'csrf_token': "",
			'rid': f'R_SO_4_{song_id}',
			'threadId': f'R_SO_4_{song_id}',
			'pageNo': f'{page_num}',
			'pageSize': 20,
			'cursor': cursor,  # 游标, 上一页返回的cursor作为下一页的参数
			'offset': 0,
			'orderType': 1
		}

		js = execjs.compile(open('decode.js', 'r', encoding='utf-8').read())
		result = js.call('decode', json.dumps(data))  # 获取加密后的参数, 传递字符串

		real_data = {  # 传递真是参数加密后的参数
			'params': result['encText'],
			'encSecKey': result['encSecKey']
		}

		resp = requests.post(url, headers=headers, data=real_data)  # 请求到歌曲的url
		# print(resp.text)
		js_data = json.loads(resp.text)
		cursor = js_data['data']['cursor']  # 上一页数据返回的cursor, 为下一页的参数
		# 获取评论
		comments = js_data['data']['comments']
		page_num = page_num + 1  # 改变页数
		print_content(comments)


if __name__ == '__main__':
	get_comments()
