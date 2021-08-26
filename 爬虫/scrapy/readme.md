#### 一、五大核心组件
引擎(Scrapy)
> 用来处理整个系统的数据流处理, 触发事务(框架核心)

调度器(Scheduler)
> 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址

下载器(Downloader)
> 用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)

爬虫(Spiders)
> 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面

项目管道(Pipeline)
> 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。


#### 二、常用中间件
下载器中间件(Downloader Middlewares)：
> 位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
> 本中间件是使用最的中间件，主要是用来串改请求、代理、和响应数据等

爬虫中间件(Spider Middlewares)：
> 介于Scrapy引擎和爬虫之间的框架，主要工作是处理spider的响应输入和请求输出。

调度中间件(Scheduler Middlewares)：
> 介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。


#### 三、基础命令
安装scrapy库
``` python
pip3 install scrapy
```

创建项目
```
scrapy startproject 项目名
```

创建基础爬虫类
``` python3
# 进入项目目录后执行命令
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
scrapy crawl 爬虫文件名 [ -o  filePath ]
```
