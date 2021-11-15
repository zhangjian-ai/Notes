## Scrapy 入门

### 1. 五大核心组件

#### 引擎(Scrapy)

> 用来处理整个系统的数据流处理, 触发事务(框架核心)



#### 调度器(Scheduler)

> 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址



#### 下载器(Downloader)

> 用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)



#### 爬虫(Spiders)

> 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面



#### 项目管道(Pipeline)

> 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。



### 2. 常用中间件

#### 下载器中间件(Downloader Middlewares)：

> 位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
> 本中间件是使用最的中间件，主要是用来串改请求、代理、和响应数据等



#### 爬虫中间件(Spider Middlewares)：

> 介于Scrapy引擎和爬虫之间的框架，主要工作是处理spider的响应输入和请求输出。



#### 调度中间件(Scheduler Middlewares)：

> 介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。



### 3. 基础命令

安装scrapy库
``` python
pip3 install scrapy

# scrapy图片持久化时，需要安装 twisted 模块
pip3 install twisted
```

创建项目
```
scrapy startproject 项目名

# 查看当前项目已有的爬虫
cd 项目名
scrapy list
```

创建基础爬虫类
``` python3
# 进入项目目录后执行命令
cd 项目名
scrapy genspider 爬虫文件名 目标域名
scrapy genspider baidu www.baidu.com
```

创建全站爬取爬虫类
``` python
scrapy genspider -t crawl 爬虫文件名 目标域名
```

执行爬虫文件
``` python3
# -o : 表示终端命令的方式本地持久化文件。文件扩展名只支持指定格式
scrapy crawl 爬虫名 [ -o  filePath ]
```





## 分布式爬虫

### 安装scrapy-redis

```python
# 安装模块
pip3 install scrapy-redis
```

- Scrapy_redis在scrapy的基础上实现了更多，更强大的功能，具体体现在：reqeust去重，爬虫持久化，和轻松实现分布式
- Scrapy-redis提供了下面四种组件（components）：(四种组件意味着这四个模块都要做相应的修改)

> Scheduler
> Duplication Filter
> Item Pipeline
> Base Spider

- Scrapy_redis是工作流程:

  <img src="https:////upload-images.jianshu.io/upload_images/12983183-1489558044ed0d56.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp" alt="img" style="zoom:50%;" />具体操作：



### 配置settings文件

```php
# 1：设置去重组件，使用的是scrapy_redis的去重组件，而不是scrapy自己的去重组件了
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2：设置调度器，使用scrapy——redis重写的调度器，
# 而不再使用scrapy内部的调度器了
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 3：可以实现断点爬取=jondir，（请求的记录不会丢失，会存储在redis数据库中，
# 不会清楚 redis的队列，下次直接从redis的队列中爬取）
SCHEDULER_PERSIST = True
# 4：设置任务队列的模式（三选一）：
# SpiderPriorityQueue数据scrapy-redis默认使用的队列模式（
# 有自己的优先级）默认第一种
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 使用了队列的形式，任务先进先出。
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# 采用了栈的形式：任务先进后出
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
#5： 实现这个管道可以将爬虫端获取的item数据，统一保存在redis数据库中
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

# 6：指定要存储的redis数据库的主机IP
REDIS_HOST = '127.0.0.1'  # 远端的ip地址

# 指定redis数据库主机的端口
REDIS_PORT = 6379
```



### 使用scrapy-redis

- 代码执行之后redis自动生成以下内容：

  ```python
  "xcfCrawlSpider:requests"：存储的是请求的request对象
  "xcfCrawlSpider:items":存储的爬虫端获取的items数据
  "xcfCrawlSpider:dupefilter"：存储的指纹(为了实现去重)
  127.0.0.1:6379> type xcfCrawlSpider:requests
  zset
  127.0.0.1:6379> type xcfCrawlSpider:items
  list
  127.0.0.1:6379> type xcfCrawlSpider:dupefilter
  set
  ```

- 第一种情况：只设置settings文件，并没有实现分布式，只是实现了scrapy_redis的数据储存和去重功能（只实现了存，没有取）

  ```python
  import scrapy
  from xiachufang.items import XiachufangTagItem,XiachufangCaiPuItem,XiachufangUserInfoItem
  
  
  class XcfSpider(scrapy.Spider):
      name = 'xcf'
      allowed_domains = ['xiachufang.com']
      #start_urls = ['https://www.xiachufang.com/category/40076/?page=1']
      start_urls = ['http://www.xiachufang.com/category/']
  
      def start_requests(self):
          pass
  ```

- 第二种情况：通用爬虫

  ```python
  from scrapy_redis.spiders import RedisCrawlSpider
  # 继承自redis——crawlspider
  class MyCrawler(RedisCrawlSpider):
      """Spider that reads urls from redis queue (myspider:start_urls)."""
      name = 'mycrawler_redis'
      # 缺少了start_url,多了redis_key:根据redis_key从redis数据库中获取任务
      redis_key = 'mycrawler:start_urls'
  
  启动爬虫
  爬虫出现等待状态:我们需要在redis中设置起始任务:
  redis输入命令：lpush xcfCrawlSpider:start_urls http://www.xiachufang.com/category/
  ```

  **注意:在redis保存起始url的时候，windows系统写url的时候不加引号，ubuntu如果输入redis命令不生效，url需要加引号**

- 第三种情况：实现scrpy.spider爬虫的分布式爬虫

  ```python
    from scrapy_redis.spiders import RedisSpider
      #继承自：RedisSpider
      class MyCrawler(RedisSpider):
          """Spider that reads urls from redis queue (myspider:start_urls)."""
          name = 'mycrawler_redis'
          allowed_domains = ['dmoz.org']
          #缺少了start_url,多了redis_key:根据redis_key从redis
          #数据库中获取任务
          redis_key = 'mycrawler:start_urls'
  
          def start_requests(self):
              """
              重写这个方法的目的可以根据自己的需求发起请求
              :return:
              """
              for url in self.start_urls:
                  yield scrapy.Request(url, callback=self.parse, dont_filter=True)
          def parse(self, response):
               pass
      启动爬虫：scrapy crawl 爬虫名称
      现象:爬虫处于等待状态
      需要设置起始任务：
      lpush mycrawler:start_urls 目标url
  ```

  **注意：实现scrpy.spider爬虫的分布式爬虫第一个回调方法必须是parse，否则代码无法运行。第三种情况同样要注意redis的命令**
