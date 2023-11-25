from threading import Thread


# 多线程方法一
# def func(name):
# 	for i in range(100):
# 		print(name, i)


# if __name__ == '__main__':
# 	# 创建多线程
# 	t1 = Thread(target=func, args=('周杰伦',))
# 	t2 = Thread(target=func, args=('周姐',))
# 	t3 = Thread(target=func, args=('沫子',))
#
# 	# 启动多线程
# 	t1.start()
# 	t2.start()
# 	t3.start()

# 多线程方法2
class MyThread(Thread):
	def __init__(self, name):
		super(MyThread, self).__init__()
		self.name = name

	def run(self):
		for i in range(100):
			print(self.name, i)


if __name__ == '__main__':
	t1 = MyThread('周姐')
	t2 = MyThread('沫子')

	t1.start()
	t2.start()

