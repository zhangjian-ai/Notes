import os

import scrapy
from itemloaders import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from qiantu.items import ThousandPicPages

from qiantu.settings import BASE_DIR


class ThousandpicpagesSpider(CrawlSpider):
    name = 'thousandPicPages'
    # allowed_domains = ['www.58pic.com']
    # start_urls = ['http://www.58pic.com/c/']
    # 通常首页的url和其他翻页后的地址是不一样的，但是往往也可以通过翻页，获取到首页的翻页地址，这样就可以不用重写parse_start_url
    start_urls = ['https://www.58pic.com/c/1-0-0-1.html']

    # 网站非首页地址：https://www.58pic.com/c/1-0-0-3.html
    # 根据翻页后的地址，写出能匹配翻页后url的正则表达式：https://www.58pic.com/c/\d+-\d+-\d+-\d+.html
    # LinkExtractor()返回一个 包含符合正则匹配的规则的列表 的LxmlLinkExtractor对象，会自动去重
    page_links = LinkExtractor(allow='/c/\d+-\d+-\d+-\d+.html', allow_domains='www.58pic.com')

    rules = (
        # 执行规则会遍历links中的地址，依次发起请求并调用回调函数处理response
        Rule(page_links, callback='parse_item', follow=True),
    )

    # 把持久化的前置操作放到spider中，这样不同的spider提交到管道后，管道就可以根据不同的item对象分别持久化
    # 总结:
    #   - 通过在items.py文件中，编写不同的类，为同一工程下不同的spider提供item类
    #   - 在pipelines.py文件中不进行前后置操作，前后置操作放到spider文件中，通过spider对象进行传递，
    #     这样就可以实现不同spider使用不同的pipeline类，降低耦合度
    #   - 在spider类中定义属性实现前置，重写close方法实现后置

    file_path = os.path.join(BASE_DIR, 'download', '千图网作者即作品名.txt')
    file = open(file_path, 'a')

    # def parse_start_url(self, response, **kwargs):
    #     """
    #     重写该方法，完成对网站首页的数据解析
    #     原因：因为上面的正则只能匹配到翻页后的url，首页url无法匹配
    #     :param response:
    #     :param kwargs:
    #     :return:
    #     """
    #     # 实例化loader
    #     loader = ItemLoader(item=ThousandPicPages(), selector=response)
    #
    #     # 使用功能类itemLoader取代传统的解析方式
    #     loader.add_xpath('author', '//div[@class="favls-wrap clearfix"]/div/a/p[2]/span/span[2]/text()')
    #     loader.add_xpath('theme', '/html/body/div[4]/div[3]/div/a/p[1]/span/text()')
    #
    #     # 解析函数会重复执行，这里使用yield
    #     yield loader.load_item()

    def parse_item(self, response):
        """
        回调函数
        :param response:
        :return:
        """
        # 实例化loader
        loader = ItemLoader(item=ThousandPicPages(), selector=response)

        # 使用功能类itemLoader取代传统的解析方式
        loader.add_xpath('author', '//div[@class="favls-wrap clearfix"]/div/a/p[2]/span/span[2]/text()')
        loader.add_xpath('theme', '//div[@class="favls-wrap clearfix"]/div/a/p[1]/span/text()')

        # 解析函数会重复执行，这里使用yield
        yield loader.load_item()

    def close(spider, reason):
        # 后置，关闭file对象
        print("最后调用")
        spider.file.close()
