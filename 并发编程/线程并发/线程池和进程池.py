# 进程池：主要在高计算场景使用，使用场景较少
# 线程池：主要在高阻塞场景使用，包括 文件读写、网络请求、数据库操作等

# 使用池的优点：
#   - 事先开启线程/进程，当需要时直接使用，不用单独在开启
#   - 池中的线程/进程数量是固定的，有助于CPU调度资源，避免无限开启过多的线程/进程
#   - 池中的线程/进程不会因为调用结束而关闭，是可以被多路任务复用的，极大的减少了线程/进程开启和关闭的资源开销
import random
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

'''
只介绍线程池的使用，进程池的使用方法和线程几乎一样
'''


# def func(a, b):
#     print(f"开始干活{a}")
#     time.sleep(1)
#     return a + b


# def parse(res):
#     print(res.result())


def func(a):
    # print(f"开始干活{a}")
    b = a[1]
    a = a[0]
    time.sleep(random.randint(1, 3))
    return a + b


def parse(res_set):
    print(res_set)
    for res in res_set:
        print(res)


# 创建一个线程池对象，参数是池中线程的数量
'''
进程池进程数量：介于 CPU核数 的1~2倍之间
线程池线程数量：小于 CPU核数 的5倍
'''
pool = ThreadPoolExecutor(4)

# for i in range(20):
#     # submit提交任务到线程池，只要线程池中有空闲线程就会立即 异步非阻塞 的方式执行任务
#     res = pool.submit(func, i, i + 1)  # submit传参直接传入就好，返回一个Future对象
#
#     # Future对象可以添加回调函数来处理执行结果，将Future对象本身作为参数传入函数
#     res.add_done_callback(parse)  # 回调函数的执行是 异步阻塞 的，因为添加回调之后并不会阻塞主线程，但每个线程的回调都需要等Future内部执行完成才拿得到结果。


# 线程池的map函数使用，入参是一个可迭代对象
# 优点：不用手动逐个提交任务到线程池，会自动完成迭代
# 缺点：函数传参只能传一个值或者对象，不能是多个。如下展示多个值放到一个元组传进去
res_set = pool.map(func, [(i, i + 1) for i in range(20)])  # map的返回值是生成器，可迭代出任务的返回值，长度就是任务数
parse(res_set)
