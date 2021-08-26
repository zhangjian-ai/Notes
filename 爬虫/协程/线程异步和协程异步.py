# 需求：爬取梨视频的视频数据
# 原则：线程池处理的是阻塞且耗时的操作
import re
from multiprocessing.dummy import Pool

import asyncio
import requests
from lxml import etree

# UA伪装
headers = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}
url = 'https://www.pearvideo.com/category_5'

# 获取响应文本
page_text = requests.get(url=url, headers=headers).text

# 解析出热门生活视频地址和视频名称
tree = etree.HTML(page_text)
li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')
video_list = list()
for li in li_list:
    video_id = li.xpath('./div/a/@href')[0].split("_")[1]
    detail_url = f'https://www.pearvideo.com/videoStatus.jsp?contId={video_id}&mrd=0.3589928467076693'
    video_name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'

    # 获取详情页信息，解析出视频地址
    headers['Referer'] = f'https://www.pearvideo.com/video_{video_id}'

    response = requests.get(url=detail_url, headers=headers).json()
    video_url = re.sub("/[0-9]{13}-", f"/cont-{video_id}-", response['videoInfo']['videos']['srcUrl'])

    video_list.append({
        'name': video_name,
        'url': video_url,
    })


def get_video_content(data: dict):
    url = data.get('url')

    print(f"开始爬取视频: {data.get('name')}")
    # 爬取视频二进制数据
    response = requests.get(url=url)
    content = response.content

    # 本地持久化视频
    with open(f"./{data.get('name')}", 'wb') as fp:
        fp.write(content)

    print(f"本地持久化完成: {data.get('name')}")


import aiohttp
import aiofiles


async def get_video_content_(data: dict):
    # 引入aiohttp 模块 pip3 install aiohttp  实现网络请求异步
    # 引入aiofiles 模块 pip3 install aiofiles   实现本地IO异步
    print("开始爬取：", data.get('name'))
    async with aiohttp.ClientSession() as session:
        async with session.get(data.get('url')) as response:
            content = await response.read()

            # 本地持久化视频
            async with aiofiles.open(f"./{data.get('name')}", 'wb') as fp:
                await fp.write(content)


if __name__ == '__main__':
    # # 创建有4个线程的线程池对象并执行
    # pool = Pool(4)
    # pool.map(get_video_content, video_list)
    #
    # # 关闭线程池
    # pool.close()
    # pool.join()

    tasks = [get_video_content_(data) for data in video_list]
    asyncio.run(asyncio.wait(tasks))
