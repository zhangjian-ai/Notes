# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # define correct filed for your crawl class
    hot_point = scrapy.Field()
