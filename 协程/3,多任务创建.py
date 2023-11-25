import asyncio
import time


async def run(i):
	print('我是run函数开始', i)
	await asyncio.sleep(2)
	print('我是run函数结束', i)


async def main():
	# 创建任务列表
	tasks = []
	# 循环创建三个任务
	for i in range(1, 4):
		# 创建 run() 协程
		coroutine = run(i)
		# 使用 asyncio.create_task() 创建任务
		task = asyncio.create_task(coroutine)
		# 将任务添加到任务列表中
		tasks.append(task)

	# 等待所有任务完成
	await asyncio.wait(tasks)


if __name__ == '__main__':
	t1 = time.time()
	# 运行主函数 main()
	asyncio.run(main())
	# 打印总运行时间
	print(time.time() - t1)
