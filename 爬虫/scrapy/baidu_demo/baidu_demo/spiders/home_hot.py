import scrapy

from baidu_demo.items import BaiduDemoItem


class HomeHotSpider(scrapy.Spider):
    # name: 爬虫类的唯一标识
    name = 'home_hot'
    # allowed_domains = ['www.baidu.com']
    # start_urls: 执行爬虫文件时，将自动对列表中的url发起请求
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        """
        解析响应结果
            - 框架内的response对象，自带xpath方法，使用方式与etree对象的xpath方法基本一致
            - 框架的xpath方法，返回值同样是一个列表，但列表项不是解析到的数据，而是Selector对象
            - Selector对象/Selector对象所在的列表均可以调用extract()/extract_first()方法，将返回字符串/列表格式的解析结果
        :param response: 自动发起请求后的响应对象
        :return:
        """

        hot_list = response.xpath('//div[@id="s-hotsearch-wrapper"]/ul/li/a/span[2]/text()').extract()

        # 实例化item
        item = BaiduDemoItem()

        # 将数据保复制给item中对应的属性
        item['hot_point'] = hot_list

        # 将item提交给pipeline进行持久化操作。多次返回结果时，使用yield即可
        return item

