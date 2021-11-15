# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from .items import NewsItem


class CarsHomePipeline:
    def process_item(self, item, spider):
        return item


class NewsPipeline:
    """
    新闻消息管道类
    """

    def process_item(self, item, spider):
        sql = "insert into chatroom.news(title, summary, detail_url, img_url, tag) values (%s, %s, %s, %s, %s)"
        if isinstance(item, NewsItem):
            spider.db_pool.execute_one(sql=sql, param=(item.get("title"), item.get("summary"), item.get("detail_url"),
                                                       item.get("img_url"), item.get("tag")))

            spider.count += 1
            # 因为配置了控制台只打印 error 级别及以上的日志消息，所以这里用error
            # spider基类已经配置了logger属性，本质就是调用的logging.getLogger()
            spider.logger.error(f"写入数据库成功 {spider.count} 条！")
