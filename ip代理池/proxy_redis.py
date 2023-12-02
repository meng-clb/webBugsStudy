"""
处理代理ip
存储, ip可用不可用进行处理
"""
import random
import redis
from settings import *


class ProxyRedis:
	def __init__(self):
		# 链接redis
		self.r = redis.StrictRedis(host=HOST, port=PORT, password=PASSWORD, decode_responses=True)

	def zset_zadd(self, ip):
		"""
		# 把ip添加到redis中
		:param ip: 要添加的ip
		"""
		self.r.zadd(REDIS_NAME, {ip: SCORE})

	def zset_zincrby(self, ip):
		"""
		增加, 减少权重
		:return:
		"""
		# 获取权重
		score = self.r.zscore(REDIS_NAME, ip)
		# 判断当前权重是否小于最低权重
		if score > MIN_SCORE:
			self.r.zincrby(REDIS_NAME, -1, ip)
		else:
			# 删除ip
			# 当ip权重小于最低权重时, 删除此ip
			print('ip:', ip, '权重过低, 删除')
			self.r.zrem(REDIS_NAME, ip)

	def get_ip(self):
		"""
		返回权重高的ip
		"""
		# 获取权重100的ip
		ip = self.r.zrangebyscore(REDIS_NAME, SCORE, SCORE, 0, -1)
		if ip:
			# 返回一个随机ip
			return random.choice(ip)
		else:
			# 获取权重95-100的ip
			ip = self.r.zrangebyscore(REDIS_NAME, 95, SCORE, 0, -1)
			if ip:
				# 返回一个随机ip
				return random.choice(ip)
			else:
				# 获取权重90-100的ip
				ip = self.r.zrangebyscore(REDIS_NAME, 90, SCORE, 0, -1)
				if ip:
					# 返回一个随机ip
					return random.choice(ip)
				else:
					# 90以下的ip不使用
					print('ip全部没法使用, 请重新获取ip')

	def zset_zrange(self):
		"""
		:return:  返回所有ip, 以供test.py 进行测试
		"""
		return self.r.zrange(REDIS_NAME, 0, -1)
