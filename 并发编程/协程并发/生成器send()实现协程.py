# yield本身就是一种在单线程下可以保存任务运行状态的方法
#   - 1、yiled可以保存状态，yield的状态保存与操作系统的保存线程状态很像，但是yield是代码级别控制的，更轻量级
#   - 2、send可以把一个函数的结果传给另外一个函数，以此实现单线程内程序之间的切换
import time


def decorator(func):
    """实现一个装饰器来开启协程"""

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res.__next__())
        # 而这完全等价
        # next(res)
        return res

    return wrapper


@decorator
def consumer(n):
    """
    生成器首次迭代不能直接使用send(value)
    必须使用next()或者send(None)
    这里借助装饰器完成第一次调用以开启协程模式
    """
    info = '初始值'
    while True:
        time.sleep(n)
        msg = yield info
        print(f"current consuming msg : {msg}")
        info = f"第 {msg} 次等待中 ..."


def producer(c1):
    """
    producer和consumer函数在一个线程内执行，通过调用send方法和yield互相切换，实现协程的功能。
    """
    n = 1
    while n < 5:
        print(f"current producing msg : {n}")
        print(c1.send(n))
        # print(c2.send(n))
        n += 1


if __name__ == '__main__':
    c1 = consumer(2)
    # c2 = consumer(3)

    producer(c1)
