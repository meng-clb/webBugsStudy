import asyncio


async def run():
	print('我是run函数')


coroutine = run()
asyncio.run(coroutine)

