# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class DoubanPipeline:
	# 开始爬虫后执行一次
	def open_spider(self, item):
		print('链接数据库')
		# 链接数据库
		self.db = pymysql.connect(host='127.0.0.1', user='root', password='root',
		                          database='meng', port=3306)
		# 设置字符编码
		self.db.set_charset('utf8')
		# 创建游标对象, 用于执行sql语句
		self.cursor = self.db.cursor()

	def process_item(self, item, spider):
		try:
			print('开始写入数据库')
			img_src = ''.join(item['img_src'])
			name = ''.join(item['name'])
			actor = '/'.join(item['actor'])
			print(img_src)
			print(name)
			print(actor)
			sql = f'insert into douban(img_src, name, actor) value("{img_src}", "{name}", "{actor}")'
			self.cursor.execute(sql)
			print('写入数据库完成')
			self.db.commit()
		except Exception as e:
			print(e)
			# print(sql)
			self.db.rollback()
		return item

	# 关闭爬虫后执行一次
	def close_spider(self, item):
		self.db.close()


class DoubanfilePipeline:
	# 开启爬虫的时候执行一次
	def open_spider(self, item):
		self.f = open('douban.txt', 'w', encoding='utf-8')

	# 实现对item对象数据的处理
	def process_item(self, item, spider):
		# 取出item对象中的数据
		img_src = ''.join(item['img_src'])
		name = ''.join(item['name'])
		actor = '/'.join(item['actor'])
		self.f.write(img_src + '\n')
		self.f.write(name + '\n')
		self.f.write(actor + '\n')
		self.f.write('\n-----------------\n')
		return item

	# 关闭爬虫的时候执行一次
	def close_spider(self, item):
		self.f.close()
