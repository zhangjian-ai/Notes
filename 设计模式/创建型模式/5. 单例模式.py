"""
单例模式：保证一个类只有一个实例对象，并提供一个访问它的全局访问点。
角色：
    - 单例(Singleton)
优点：
    - 对唯一实例的受控访问
    - 单例相当于全局变量，防止了命名空间被污染
实现方式：有五种实现方式，常用的主要是基于__new__方法实现；基于metaclass实现
    - python中单个py文件其实就已经实现了单例。在模块代码执行之前，解释器会先将其编译成字节码保存在.pyc文件中(导入模块、run模块都会产生.pyc)
    - 在多次导入时，解释器会先检查.pyc文件的创建时间和py文件最近的修改时间，如果没有修改便会直接调用之前的.pyc文件，省去代码编译这一步操作。
"""

from threading import Lock


class Singleton:
    lock = Lock()

    def __new__(cls, *args, **kwargs):
        # 创建实例的过程需要加锁，否则可能出现两个线程都在创建实例的情况
        with cls.lock:
            if not hasattr(cls, '_singleton'):
                cls._singleton = super().__new__(cls)
        return cls._singleton


class MyClass(Singleton):
    def __init__(self, num):
        self.num = num


a = MyClass(10)
b = MyClass(20)

print(a.num)
print(b.num)

print(id(a), id(b))

'''
打印结果说明：
    20  # 因为单例的存在，变量a的引用，在b实例化时，返回给了b，即b变量的引用和a是同一个。在b执行__init__时，修改了该对象中的属性num值
    20  # 所以此时的a、b都指向同一个对象，所以打印的值是一样的
    4331680000 4331680000  # 通过打印对象的id，再次证明二者是同一个实例对象
'''

