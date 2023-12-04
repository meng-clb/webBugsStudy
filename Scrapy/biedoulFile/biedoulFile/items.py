# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiedoulfileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义要存储的字段 定义title, con, 只能存储这两个字段, 存入其它则报错
    title = scrapy.Field()
    con = scrapy.Field()
