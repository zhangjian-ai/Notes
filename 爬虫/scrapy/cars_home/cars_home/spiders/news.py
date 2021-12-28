"""
需求：
    爬取汽车之家的新闻信息。
        标题
        简介
        标题链接
        图片链接
        标签
"""
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from cars_home.items import NewsItem

from database import DBPool


class NewsSpider(CrawlSpider):
    name = 'news'
    # allowed_domains = ['https://www.autohome.com.cn/']
    start_urls = ['https://www.autohome.com.cn/all/']

    # 解析tag首页链接
    tag_links = LinkExtractor(
        allow="https://www.autohome.com.cn/(all|news|advice|drive|use|culture|travels|tech|tuning|ev)/$")

    # 解析新闻列表页
    news_links = LinkExtractor(allow="https://www.autohome.com.cn/\w+/\d{1,3}/#liststart$")

    rules = (
        # tag标签只需要在首页匹配tag链接即可
        Rule(tag_links, callback='parse', follow=True),

        # 新闻列表页需要在所有页面去匹配满足条件的链接以爬取数据
        Rule(news_links, callback="parse", follow=True)
    )

    # 初始化数据库连接池
    db_pool = DBPool(
        host="101.43.61.175",
        port=3300,
        user="root",
        password="zm_123456",
        db="chatroom",
        mincached=10
    )

    # 计数
    count = 0

    def parse(self, response, **kwargs):
        # 获取页面中所有的li标签
        li_list = response.xpath('//*[@class="article"]/li')

        # 遍历标签列表，获取数据
        for li in li_list:
            title = li.xpath('a/h3/text()').get()
            if title:
                # 实例化item对象
                item = NewsItem()

                detail_url = "https:" + li.xpath('a/@href').get().strip()
                img_url = li.xpath('a/div/img/@src').get().strip()

                if "https" not in img_url:
                    img_url = "https:" + img_url

                item['title'] = title.strip()
                item['summary'] = li.xpath('a/p/text()').get().strip()
                item['detail_url'] = detail_url
                item['img_url'] = img_url
                item['tag'] = item['detail_url'].split('/', 4)[3]

                yield item
