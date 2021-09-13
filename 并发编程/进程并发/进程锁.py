import json
import os
import multiprocessing
import time
from multiprocessing import Lock, Process


def query_ticket(i):
    # path = os.path.join(os.path.abspath(__file__).rsplit('/', 1)[0], 'tickets.json')
    with open('tickets.json', 'r') as fp:
        tickets = json.load(fp)

    print("%s:查询到剩余票数：[%s]" % (i, tickets['count']))


def buy_ticket(i):
    with open('tickets.json', 'r') as fp:
        tickets = json.load(fp)

    if tickets['count'] > 0:
        time.sleep(1)
        tickets['count'] -= 1

        with open('tickets.json', 'w') as fp:
            json.dump(tickets, fp)

            print("%s: 我成功购到票啦！！" % i)
    else:
        print("%s: 很遗憾，没买到呢！！" % i)


def action(i, lock):
    query_ticket(i)

    # # 给进程加锁，购票时只能一个一个买
    # lock.acquire()
    # buy_ticket(i)
    # lock.release()
    with lock:
        buy_ticket(i)


if __name__ == '__main__':
    # 这是一个小坑。
    '''
    mac系统
    python3.4更新后，默认用“spawn”，开启进程，我们要主动指定为“fork”
    spawn：使用此方式启动的进程，只会执行和 target 参数或者 run() 方法相关的代码。
        Windows 平台只能使用此方法，事实上该平台默认使用的也是该启动方式。相比其他两种方式，此方式启动进程的效率最低。
    fork：使用此方式启动的进程，基本等同于主进程（即主进程拥有的资源，该子进程全都有）。
        因此，该子进程会从创建位置起，和主进程一样执行程序中的代码。
        注意，此启动方式仅适用于 UNIX 平台，os.fork() 创建的进程就是采用此方式启动的。
    forserver：使用此方式，程序将会启动一个服务器进程。
        即当程序每次请求启动新进程时，父进程都会连接到该服务器进程，请求由服务器进程来创建新进程。
        通过这种方式启动的进程不需要从父进程继承资源。注意，此启动方式只在 UNIX 平台上有效。
    '''
    multiprocessing.set_start_method('fork')

    # 实例化一个锁
    lock = Lock()

    for i in range(10):
        Process(target=action, args=(i, lock)).start()
