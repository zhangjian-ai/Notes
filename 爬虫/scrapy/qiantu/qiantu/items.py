# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QiantuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    author = scrapy.Field()
    theme = scrapy.Field()


class ThousandPicPages(scrapy.Item):
    """
    不同的爬虫类建议使用不同的item
        - 方便区分不同爬虫类的字段
        - 后续pipeline持久化利用item类行不同可实现不同形式的持久化
    """

    author = scrapy.Field()
    theme = scrapy.Field()


class ImageDownload(scrapy.Item):
    """
    图片爬取item
    """
    src = scrapy.Field()
    name = scrapy.Field()
