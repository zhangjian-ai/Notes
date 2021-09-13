# 死锁现象：多个线程竞争多把锁的时，且多把锁存在交叉使用的情况，那么久极有可能出现死锁现象。即线程之间都在等待对方释放锁。
# 递归锁：递归锁可以多次acquire和release，只有第一次竞争到锁的线程才可以继续acquire，其他线程需要等到所有的acquire都被release才能竞争到。
#   - 优点：递归锁快捷可以实现多级锁，其次是在优化项目多个互斥锁的场景比较方便。
#   - 缺点：递归锁性能不如互斥锁，所以尽可能的使用互斥锁。
import time
from threading import Lock, RLock, Thread

# 死锁和是不是使用互斥锁没有关系，此处使用递归锁处理死锁的问题
# l1 = Lock()
# l2 = Lock()

l1 = l2 =RLock()


def lock1(l1, l2, name):
    l1.acquire()
    print(name, "拿到第一把锁")

    l2.acquire()
    print(name, "拿到第二把锁")

    time.sleep(2)
    print(name, "do something")

    l1.release()
    print(name, "释放第一把锁")

    l2.release()
    print(name, "释放第二把锁")


def lock2(l1, l2, name):
    l2.acquire()
    print(name, "拿到第二把锁")

    l1.acquire()
    print(name, "拿到第一把锁")

    time.sleep(2)
    print(name, "do something")

    l1.release()
    print(name, "释放第一把锁")

    l2.release()
    print(name, "释放第二把锁")


for i in range(10):
    Thread(target=lock1, args=(l1, l2, 'alex')).start()
    Thread(target=lock2, args=(l2, l2, 'fiona')).start()
