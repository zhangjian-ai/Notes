# 引入selenium UI自动化测试模块 pip3 install selenium
# 下载对应浏览器驱动：此处使用chromedriver  地址：http://npm.taobao.org/mirrors/chromedriver/
# 需求：爬取 百度首页热搜信息

from selenium import webdriver
from lxml import etree

# 实例化之前可以先做一些配置
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 后台运行模式

# 实例化驱动对象
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

# 打开网页
driver.get('https://www.baidu.com/')

# 获取网页页面源代码
page_text = driver.page_source

# 关闭当前窗口
driver.close()

# 关闭整个浏览器
driver.quit()

# 解析文本
tree = etree.HTML(page_text)
li_list = tree.xpath('//div[@id="s-hotsearch-wrapper"]/ul/li')
hot_text = list()
for li in li_list:
    text = li.xpath('./a/span[2]/text()')[0]
    hot_text.append(text)

print(hot_text)
