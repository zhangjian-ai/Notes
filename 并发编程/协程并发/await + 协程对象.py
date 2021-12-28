# await: 等待。 直到获得了等待对象的返回值之后，再执行后面的代码
# await可等待的对象: 协程对象， task对象，future对象

import asyncio


async def func(name):
    print(name + " start")
    await asyncio.sleep(2)
    print(name + " end")
    return '返回值'


# 示例一: await 协程对象
async def func1(name):
    # 遇到IO操作时，await会挂起当前操作。如果是在事件循环中，那么就会切换到其他协程对象继续执行
    response1 = await func(name)
    print('第一次：', response1)


asyncio.run(asyncio.wait([func1("zhangjian"), func1("zhangjie")]))
