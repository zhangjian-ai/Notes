import scrapy
import requests


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    # allowed_domains = ['www.XXX.com']
    start_urls = ['https://download.csdn.net/api/source/detail/v1/previewInfos?sourceId=13743198&pageBeginNum=1&pageSize=1']

    def parse(self, response):

        response = requests.get(self.start_urls[0])
        print(response.status_code)
        print(response.text.encode().decode())
        txt = response.text.xpath('//div[@class="c x1 y1 w2 h2"]//text()')
        print(txt)
