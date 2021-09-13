# Queue 先进先出队列
# LifoQueue 后进先出队列
# PriorityQueue 优先级队列
# 以上队列均能保证数据安全

import time
import threading
from queue import Queue, LifoQueue, PriorityQueue


def producer(q):
    # for i in range(3):
    #     time.sleep(1)
    #     q.put(i)
    #     print(f"生产：{i}")

    # 优先级队列，根据优先级取值，按ascii码顺序，越靠前的越大
    q.put((3, "哩个"))
    q.put((1, "诸天"))
    q.put((0, "莫邪"))


def consumer(q):
    for i in range(3):
        time.sleep(1)
        a = q.get()
        print(f"消费：{a}")


# 入参表示队列最大长度，当队列满了之后，继续put会阻塞。除非get出去
# q = Queue(4)
# q = LifoQueue(3)
q = PriorityQueue(3)


p = threading.Thread(target=producer, args=(q,))
p.start()
p.join()

threading.Thread(target=consumer, args=(q,)).start()
