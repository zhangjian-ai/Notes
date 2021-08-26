# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 下面的item类，是创建工程时自动创建，直接启用，后续根据spider定义独立的item类
# ----------------------------------------------------------------
# class WangyiItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class NewsItem(scrapy.Item):
    cate = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
