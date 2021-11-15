import scrapy

from itemloaders import ItemLoader

from qiantu.items import ImageDownload


class GetHomePictureSpider(scrapy.Spider):
    name = 'get_home_picture'
    # allowed_domains = ['www.58pic.com']
    start_urls = ['http://www.58pic.com/c/']

    def parse(self, response, **kwargs):

        # 解析图片名称及图片地址
        loader = ItemLoader(item=ImageDownload(), selector=response)
        loader.add_xpath('src', '//div[@class="favls-wrap clearfix"]/div/a/div/img/@src')
        loader.add_xpath('name', '//div[@class="favls-wrap clearfix"]/div/a/p[1]/span/text()')

        return loader.load_item()
