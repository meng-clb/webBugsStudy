import asyncio


async def run():
	print('我是run函数开始')
	await asyncio.sleep(2)
	print('我是run函数结束')


if __name__ == '__main__':
	coroutine = run()
	task = asyncio.ensure_future(coroutine)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(task)
