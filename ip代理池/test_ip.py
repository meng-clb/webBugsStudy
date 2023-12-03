"""
测试代理ip是否可用
"""
import asyncio
import time
import aiohttp
from proxy_redis import ProxyRedis


async def test_ip(ip, p_r, sem):
	try:
		# 信号量并发控制
		async with (sem):
			async with aiohttp.ClientSession() as session:
				async with session.get('http://httpbin.org/ip', proxy='http://' + ip,
				                       timeout=10) as resp:
					con = await resp.text()
					if con:
						# 代理可用, 设置权重为100
						p_r.zset_zadd(ip)
					else:
						# 代理不可用, 降低权重
						p_r.zset_zincrby(ip)
						print(ip, '降低权重')
	except Exception as e:
		print(ip, e)


async def main():
	# 实例化ip类的处理
	p_r = ProxyRedis()
	ip_lise = p_r.zset_zrange()
	sem = asyncio.Semaphore(100)  # 并发控制
	if ip_lise:
		tasks = []
		for ip in ip_lise:
			task = asyncio.create_task(test_ip(ip, p_r, sem))
			tasks.append(task)

		await asyncio.wait(tasks)


def run():
	while True:
		try:
			asyncio.run(main())
			time.sleep(30)
		except Exception as e:
			print('ip测试异步出现错误', e)


if __name__ == '__main__':
	run()
