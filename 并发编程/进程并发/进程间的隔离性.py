import time
from multiprocessing import Process

n = 100


def func():
    time.sleep(2)
    global n
    n = n + 100
    print(n)


if __name__ == '__main__':
    p = Process(target=func)
    p.start()
    # p.join()

    print(n)  # 从 入门.py 中可知，子进程是拥有自己的一套数据的，所以子进程修改的 全局变量 n 是子进程中的，和主进程中的没有关系

    # 异步结束子进程
    p.terminate()
    # 查看进程状态，因为是异步结束，所以这里立即打印子进程肯定是激活的状态，只需要小睡一下
    time.sleep(0.01)
    print(p.is_alive())

    # 进程名
    print(p.name)

    # 释放进程资源，前提是必须是执行完的进程或者调用terminate()
    p.close()
