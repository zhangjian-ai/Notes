# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter


class BaiduDemoPipeline:
    """
    优化结构，以实现前后置操作
    前置：def __init__(self):, def open_spider(self, spider):
    后置：def close_spider(self, spider):
    """
    def __init__(self):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download', 'home_hot.txt')
        self.file = open(file_path, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        [self.file.write(content + '\n\n') for content in item['hot_point']]

        return item

    def close_spider(self, spider):
        self.file.close()
