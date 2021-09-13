# 守护进程：通常作为主进程的一个子进程而存在，主要作用就是监控主进程的一些状态。
# 生命周期：守护进程在主进程代码执行完毕之后立即结束，而不是主进程结束后结束。 原因：主进程要负责回收子进程的资源。

import time

from multiprocessing import Process


def son1():
    while True:
        time.sleep(1)
        print("son1")


def son2():
    for i in range(5):
        time.sleep(1)
        print("son2")


if __name__ == '__main__':
    p1 = Process(target=son1)
    # 设置p1 为守护进程
    p1.daemon = True
    # 异步开启子进程
    p1.start()

    p2 = Process(target=son2)
    p2.start()

    time.sleep(3)

'''
执行结果分析：
    son2  
    son1  
    son2
    son1  # 子进程一是守护进程，当主进程代码执行完，便立即结束循环
    son2
    son2
    son2  # 子进程二不是守护进程，故会一直执行完内部的循环
    
          # 待主进程回收完子进程的资源后，再由pycharm的进程来回收py文件的进程资源
'''

