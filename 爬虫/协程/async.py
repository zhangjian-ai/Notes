# 协程是一种用户态的轻量级线程，协程的调度完全由用户控制，而不是交给计算机。
# 协程是可以暂停等待、然后又恢复的生成器函数。
#   - 协程拥有自己的寄存器上下文和栈。
#   - 协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的寄存器上下文和栈，
#   - 直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量，所以上下文的切换非常快。
# 协程函数定义: async def 函数名
# 协程对象: 执行协程函数 函数名() 得到协程对象
# 注意: 执行协程函数 获得协程对象，内部函数是不会执行的
# 如果想要执行协程对象内部代码，必须将协程对象交给 事件循环 来处理, 或者 await 协程对象
# 协程并发：由事件循环来执行task任务列表，当协程阻塞时，完成自动切换

import asyncio

# uvloop 第三方库，其效率比asyncio自身的循环事件效率更高，通常将其替代asyncio的事件循环对象，操作如下
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # 在文件开头替换掉循环事件策略即可，其他asyncio操作不变


async def func():
    """async 关键字实现协程"""
    print("来了老弟！")


if __name__ == '__main__':
    # 获得协程对象，内部函数不执行
    res = func()

    # 循环事件 调用协程对象

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(res)

    # python 3.7 后的简单写法，等价于上面两行代码
    asyncio.run(res)
