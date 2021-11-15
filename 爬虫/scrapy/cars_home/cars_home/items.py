# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarsHomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NewsItem(scrapy.Item):
    """
    新闻消息Item
    """
    title = scrapy.Field()
    summary = scrapy.Field()
    detail_url = scrapy.Field()
    img_url = scrapy.Field()
    tag = scrapy.Field()

