# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import NewsItem


class WangyiPipeline:
    def process_item(self, item, spider):
        # 处理news爬虫类的持久化
        if isinstance(item, NewsItem):
            if item.get('cate'):
                spider.file.write(item['title'][0])
                for text in item['content']:
                    spider.file.write(text)

        return item
