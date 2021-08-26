# 需求：爬取千图网的作者及主题名称

import scrapy
from itemloaders import ItemLoader

from qiantu.items import QiantuItem


class ThousandpicSpider(scrapy.Spider):
    name = 'thousandPic'
    # allowed_domains = ['www.58pic.com']
    start_urls = ['http://www.58pic.com/c/']

    def parse(self, response):
        '''
        查看页面元素
            - /html/body/div[4]/div[3]/div[1]/a/p[2]/span/span[2]/text() 这是常规的页面元素的xpath路径
            - 因为页面中 有多张图，而图是以 /html/body/div[4]/div[3]/div[i]/a/p[2]/span/span[2]/text()中i为变量作为区分的
            - 所以为了获取当前页面所有的图这里不写 i 程序会遍历该路径下的所有图片。
            - /html/body/div[4]/div[3]/div/a/p[2]/span/span[2]/text()
        '''

        # # ----------------------传统解析方式--------------------
        # author = response.xpath('//div[@class="favls-wrap clearfix"]/div/a/p[2]/span/span[2]/text()').extract()
        # theme = response.xpath('/html/body/div[4]/div[3]/div/a/p[1]/span/text()').extract()
        #
        # # 使用框架自带的log输出器
        # # self.log(author)
        # # self.log(theme)
        #
        # # for key, value in zip(author, theme):
        # #     print(key.ljust(16, " ") + value)
        #
        # # 引入item
        # item = QiantuItem()
        # item['author'] = author
        # item['theme'] = theme
        #
        # return item
        # # ----------------------传统解析方式--------------------

        # -------------------引入itemLoader-------------------
        # 实例化loader
        loader = ItemLoader(item=QiantuItem(), selector=response)

        # 使用功能类itemLoader取代传统的解析方式
        loader.add_xpath('author', '//div[@class="favls-wrap clearfix"]/div/a/p[2]/span/span[2]/text()')
        loader.add_xpath('theme', '/html/body/div[4]/div[3]/div/a/p[1]/span/text()')

        # load_item()返回的是一个字典结构数据体的一个item类，{'author': [...], 'theme': [...]}
        return loader.load_item()
        # -------------------引入itemLoader-------------------

