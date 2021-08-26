# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

from .items import QiantuItem, ThousandPicPages


class QiantuPipeline:
    def __init__(self):
        # file_path = os.path.join(os.path.abspath(__file__).rsplit('/', 2)[0], 'download', '千图网作者即作品名.txt')
        # self.file = open(file_path, 'a')
        pass

    def process_item(self, item, spider):
        # # 将item转成json字符串
        # text = json.dumps(dict(item), ensure_ascii=False)
        #
        # self.file.write(text)

        # 根据不同的item类型实现不同场景的持久化
        if isinstance(item, QiantuItem):
            with open('quantu_02.json', 'a', encoding='utf-8') as fp:
                json.dump(dict(item), fp, ensure_ascii=False)
        if isinstance(item, ThousandPicPages):
            if dict(item).get('author'):
                for author, theme in zip(item['author'], item['theme']):
                    # self.file.write(author + ':' + theme + '\n')

                    # 这里来获取spider中定义的file实现持久化
                    spider.file.write(author + ':' + theme + '\n')

        return item

    def close_spider(self, spider):
        # self.file.close()
        pass


class ImageDownloadPipeline(ImagesPipeline):
    """
    dependency: Pillow
    图片爬取管道类
    """

    def get_media_requests(self, item, info):
        """
        重写请求类
        :param item: item对象
        :param info:
        :return:
        """
        if item.get('src'):
            for src, name in zip(item['src'], item['name']):
                # 利用请求传参，把图片名传递下去
                yield scrapy.Request(url='https:' + src, meta={'name': name})

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        重写该函数，返回图片文件名称
        否则将在项目根目录生成乱七八糟的文件名
        :param request: 请求对象
        :param response:
        :param info:
        :param item:
        :return:
        """

        return request.meta['name'] + '.jpg'

    def item_completed(self, results, item, info):
        """
        重写该函数，将item继续传递给后面的管道类
        :param results:
        :param item:
        :param info:
        :return:
        """
        # print(item['name'] + '爬取 ')
        # print(results[0][0])
        return item

