# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class DeskPipeline:
	def process_item(self, item, spider):
		return item


class Imgspipline(ImagesPipeline):
	# 1. 发送请求(下载图片, 文件, 视频, xxx)
	def get_media_requests(self, item, info):
		# 获取到图片的url
		url = item['img_urls']
		# 进行请求
		yield scrapy.Request(url=url, meta={'url': url})  # 直接返回一个请求对象即可

	# 2. 图片存储路径
	def file_path(self, request, response=None, info=None, *, item=None):
		# file_name = item['down_img'].split('/')[-1]  # 使用item拿到url
		file_name = request.meta['url'].split('/')[-1]  # 用meta传递参数
		return file_name

	# 3. 可能需要对item进行更新
	def item_completed(self, results, item, info):
		# for r in results:
		# 	# 获取每个图片的路径
		# 	print(r[1]['path'])
		for success, image_info in results:
			if success:
				# 获取每个图片的路径
				print(image_info['path'])
		return item  # 一定要return item 把数据传递给下一个管道


