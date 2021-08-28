import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader

from redis import Redis

from movie.items import A4567kpItem, A4567Detail


class A4567kpSpider(CrawlSpider):
    name = 'a4567kp'
    # allowed_domains = ['www.4567kp.com']
    start_urls = ['http://www.4567kp.com/frim/index1.html']

    links = LinkExtractor(allow=r'/frim/(index1|index1-\d+)\.html')

    rules = (
        Rule(links, callback='parse_item', follow=True),
    )

    # 实例化redis
    redis = Redis(host='121.4.47.229', password='meiduo123', db=15)

    def parse_item(self, response):
        # 解析出当前页面的电影详情链接
        loader = ItemLoader(item=A4567kpItem(), selector=response)

        loader.add_xpath('href', '//ul[@class="stui-vodlist clearfix"]/li/div/a/@href')
        item = loader.load_item()

        # 获取电影详情
        if item.get('href'):
            for url in item.get('href'):
                # 保存url到redis
                res = self.redis.sadd('a4567kp', url)

                # 保存成功则说明还未爬取过
                if res:
                    yield scrapy.Request(url='http://www.4567kp.com' + url, callback=self.parse_detail)
                else:
                    print('当前电影已被爬取...')

    def parse_detail(self, response):
        # 解析电影详情
        title = response.xpath('//div[@class="stui-content__detail"]/h1/text()').get()
        detail = response.xpath('//div[@class="stui-content__detail"]/p[@class="desc detail hidden-xs"]/span[@class="detail-content"]/text()').get()

        item = A4567Detail()
        item['title'] = title
        item['detail'] = detail

        return item

    def close(spider, reason):
        # 断开redis链接
        spider.redis.close()
