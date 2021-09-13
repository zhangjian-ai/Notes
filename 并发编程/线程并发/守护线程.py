import time
from threading import Thread


def son1():
    while True:
        time.sleep(1)
        print("son-1")


def son2():
    for i in range(5):
        time.sleep(1)
        print("son-2")


t1 = Thread(target=son1)
t2 = Thread(target=son2)

t1.daemon = True
t1.start()

t2.start()

# 守护线程在当前进程中所有非守护线程结束后才结束，包括主线程，不随主线程代码执行完毕而结束。
# 守护线程结束后，进程也随之结束。

# 守护进程和守护线程的区别：
#   - 守护进程，作为主进程的子进程，需要由主进程来回收其资源，故要先于主进程关闭，时间点选在主进程代码执行完毕的时刻。
#   - 守护线程，作为主线程的子线程，他们都是运行同一进程中，互相共享进程资源，故无需在主线程之前结束。
