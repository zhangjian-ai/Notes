# Manager 进程间数据共享方式使用较少，因为Manager共享原理是开辟一块所有进程都能访问的独立空间。
# 在进程修改数据时，需要将数据取回到进程内部，修改好了之后再放回去。就在这个一取一放的过程中，其他进程也可能同时对其进行了修改，故数据安全性比较低。
# 配合进程锁可解决以上问题，但是不是很必要。
import multiprocessing
import time
from multiprocessing import Process, Manager, Lock


def consumer(data):
    time.sleep(0.2)
    data['count'] += 1


def action(data, lock):
    with lock:
        consumer(data)


if __name__ == '__main__':
    multiprocessing.set_start_method('fork')

    lock = Lock()

    m = Manager()
    data = m.dict({'count': 0})
    lines = m.list([])

    for i in range(50):
        p = Process(target=action, args=(data, lock,))
        p.start()

    time.sleep(12)

    print(data)
