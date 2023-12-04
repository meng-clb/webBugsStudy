# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BiedoulmysqlPipeline:
	# 开启爬虫的时候执行一次
	def open_spider(self, item):
		# 链接数据库
		self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root',
		                          database='meng')
		# 设置字符编码
		self.db.set_charset('utf8')
		# 创建游标对象, 用于执行sql语句
		self.cursor = self.db.cursor()

	# 实现对item对象数据的处理
	def process_item(self, item, spider):
		try:
			# 把标题和内容写入数据库内
			print('开始写入')
			print(item['title'] + '\n')
			print(item['con'] + '\n')
			sql = f'insert into duanzi values(null, "{item["title"]}", "{item["con"]}")'
			# 执行sql语句
			self.cursor.execute(sql)
			self.db.commit()
			print('写入完成')
		except:
			self.db.rollback()
		return item

	# 关闭爬虫的时候执行一次
	def close_spider(self, item):
		self.db.close()
