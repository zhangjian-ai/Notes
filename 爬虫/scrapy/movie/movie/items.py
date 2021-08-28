# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class MovieItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class A4567kpItem(scrapy.Item):
    href = scrapy.Field()


class A4567Detail(scrapy.Item):
    title = scrapy.Field()
    detail = scrapy.Field()
