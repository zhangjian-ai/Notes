import time
from threading import Thread

loop = int(1E7)


def put(loop: int = 1):
    global num
    for _ in range(loop):
        num.append(0)


def get(loop: int = 1):
    global num
    # while not num:
    #     time.sleep(1E-8)
    for _ in range(loop):
        print(num.pop())


num = []

t1 = Thread(target=put, args=(loop,))
t2 = Thread(target=get, args=(loop,))

# 数据安全：因为是同步执行，因为弹出的操作一定是在全部append之后
t1.start()
t1.join()

t2.start()
t2.join()

# 数据不安全：连续start()存在短暂的异步，这个过程中就可能pop到空列表
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()


