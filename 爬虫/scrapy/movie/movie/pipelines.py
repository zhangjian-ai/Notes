# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import A4567Detail


class MoviePipeline:
    def process_item(self, item, spider):
        if item:
            if isinstance(item, A4567Detail):
                print(item['title'])
                print(item['detail'])
