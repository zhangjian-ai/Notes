import os

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from selenium import webdriver

from wangyi.items import NewsItem

# >>> 需求：抓取网易新闻中各板块的新闻标题及新闻内容
# >>> 小知识：get()/getall() 两个方法同 extract_first()/extract()
from wangyi.settings import BASE_DIR


class NewsSpider(CrawlSpider):
    name = 'news'
    # allowed_domains = ['https://news.163.com/']
    start_urls = ['https://news.163.com/']

    # 利用LinkExtractor提取出首页中各板块的url
    links = LinkExtractor(allow='https://news.163.com/[a-z]+/$')

    # rules 元组中，可以添加多个Rule()对象，传入不同的提取器对象以实现同一页面不同规则的url内容爬取
    rules = (
        # follow 取值说明
        # - True: 表示链接提取器，在所有请求的页面都会生效，去匹配满足正则的url
        # - False: 链接提取器仅在其实url页面提取链接，后续将不再提取
        Rule(links, callback='parse_item', follow=False),
    )

    # 实例化一个driver,给下载中间件来篡改响应用
    # 实例化之前可以先做一些配置
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 后台运行模式

    # 实例化驱动对象
    driver = webdriver.Chrome(executable_path=os.path.join(BASE_DIR.rsplit('/', 2)[0], 'chromedriver'), options=options)

    # 本地持久化保存
    file = open(os.path.join(BASE_DIR, 'wangyi', 'download', 'news.txt'), 'a', encoding='utf-8')

    def parse_item(self, response):
        # 网易新闻分类页面都是懒加载的，所以直接解析是解析不到新闻标题的
        # 此处在下载中间件中篡改response，解决该问题，实现方式见中间件文件
        url_list = response.xpath('//div[@class="ndi_main"]/div/div/div[1]/h3/a/@href').getall()
        cate = response.xpath('//div[@class="index_head"]/div[1]/span/span/text()').get()

        # 写入分类
        if url_list:
            self.file.write(cate + ': \n\n')

        for url in url_list:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_content, meta={'cate': cate})

    def parse_content(self, response):
        # 解析出分类页中的新闻标题
        loader = ItemLoader(item=NewsItem(), selector=response)

        # 网易新闻分类页面都是懒加载的，所以直接解析是解析不到新闻标题的
        # 此处在下载中间件中篡改response，解决该问题，实现方式见中间件文件
        loader.add_xpath('title', '//h1[@class="post_title"]/text()')
        loader.add_xpath('content', '//div[@class="post_body"]//text()')

        item = loader.load_item()

        item['cate'] = response.request.meta['cate']

        return item

    def close(spider, reason):
        # 关闭driver对象
        spider.driver.quit()
        # 关闭文件对象
        spider.file.close()
