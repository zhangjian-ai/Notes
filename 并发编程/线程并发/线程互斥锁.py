# 互斥锁存在的意义：解决线程之间的数据安全问题。多线程共享全局变量、静态变量，所以就存在数据安全隐患。
# 多线程数据不安全的操作：+=  -=  /=  %=  if语句  while语句  等。只要是先计算后赋值或者先判断后操作的场景，都有数据安全风险。
#   - 原因：线程之间的依赖GIL锁来完成切换，在上面描述场景中很可能没来得及赋值，线程就被切换了，当再次切回来赋值时，就有可能覆盖其他线程的执行结果。

# 线程互斥锁使用举例：单例模式，不论是基于__new__函数实现，还是基于元类实现，都把 判断并实例化的操作 放到锁里面。

import time

from threading import Thread, Lock


class Singleton:
    _instance = None
    lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls.lock:  # 这里不加锁，那么下面的多线程打印出来的就不是同一个对象了。
            if not cls._instance:
                # 加sleep是为了方便触发线程切换
                time.sleep(0.01)
                cls._instance = super().__new__(cls)

        return cls._instance


def single():
    a = Singleton()
    print(a)


for i in range(10):
    Thread(target=single).start()
