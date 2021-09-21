import threading

# threading.local() 对象可以实现线程间的数据隔离，当前线程的属性只能当前线程操作
instance = threading.local()  # 返回一个实例对象


def put():
    instance.name = 'zhangjian'
    name = instance.name
    print(name)  # zhangjian


def get():
    name = instance.name
    print(name)  # 抛出异常：AttributeError: '_thread._local' object has no attribute 'name'


t1 = threading.Thread(target=put)
t2 = threading.Thread(target=get)

t1.start()
t1.join()
t2.start()
t2.join()
