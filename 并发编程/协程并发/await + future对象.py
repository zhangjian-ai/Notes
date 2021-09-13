# task 继承 future，task内部 await结果的处理基于future

import asyncio


# 示例一：
async def main():
    # 获取当前循环事件，即asyncio.run() 创建的循环事件
    loop = asyncio.get_running_loop()

    # 创建一个future对象，该对象内部什么都不干
    fut = loop.create_future()

    # 等待任务最终结果，此处没有结果则会一直等下去
    await fut


# asyncio.run(main())


# 示例二
async def set_after(fut):
    await asyncio.sleep(2)
    fut.set_result("666")


async def main1():
    loop = asyncio.get_running_loop()
    fut = loop.create_future()

    # 创建一个task，await 关键字等待这个task，那么这个task任务内部代码将被执行，2s后会给fut对象手动设置返回值
    # 当前await 等到就是一个 set_after 的协程对象
    await loop.create_task(set_after(fut))

    data = await fut
    print(data)


asyncio.run(main1())

# ---------------------------------
# 扩展: concurrent.futures.Future 对象

import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor


def func(value):
    time.sleep(1)
    print(value)


def func1():
    time.sleep(2)
    return "SB"


# 创建线程池
# pool = ThreadPoolExecutor(max_workers=5)
#
# # 创建进程池
# # pool = ProcessPoolExecutor(max_workers=5)
#
# for i in range(10):
#     # pool.submit() 返回一个Future对象
#     fut = pool.submit(func, i)
#     # print(fut)


async def main2():
    loop = asyncio.get_running_loop()

    # 第一步：内部先调用 ThreadPoolExecutor 自动创建一个线程池，再调用 submit 方法去线程池中申请一个线程去执行func1，并返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.warp_future装饰器，将第一步的Future对象包装成 asyncio.future 对象
    # concurrent.futures.Future对象 是不支持 await 语法，只有asyncio.future支持

    fut = loop.run_in_executor(None, func1)  # 默认使用 ThreadPoolExecutor, 也可以主动传入线程池/进程池对象
    result = await fut

    print(result)

    # with ThreadPoolExecutor(max_workers=5) as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #
    #     print(result)

    # with ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #
    #     print(result)

if __name__ == '__main__':
    asyncio.run(main2())
