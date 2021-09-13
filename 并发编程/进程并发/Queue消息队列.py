# Queue 队列是一个线性链表，遵守先进先出原则。如果链表为空，那么get()将会阻塞，直到put进去一个新的值。
# Queue 是可以保证进程数据安全的

import multiprocessing
import time
from multiprocessing import Queue, Process


def consumer(q):
    while True:
        time.sleep(1)
        product = q.get()
        if product != None:
            print("消费者消费了产品：【%s】" % product)
        else:
            break


def producer(i, q):
    for a in range(5):
        time.sleep(1)
        print("%s 生产了产品：【%s】" % (i, a))
        q.put(a)


if __name__ == '__main__':
    multiprocessing.set_start_method('fork')

    q = Queue()
    producers = []

    # 多个生产者
    for i in range(3):
        p = Process(target=producer, args=(i, q))
        p.start()
        producers.append(p)

    # 等到生产者都生产好了在消费
    # [x.join() for x in producers]

    # 一个消费者
    c = Process(target=consumer, args=(q,))
    c.start()

    # put一个结束表示
    time.sleep(15)
    q.put(None)
