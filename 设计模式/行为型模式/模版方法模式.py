'''
模版方法模式：定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模版方法使得子类可以不改变一个算法的结构即可重新定义该算法的某些特定步骤。
角色：
    - 抽象类(AbstractClass)：定义抽象的原子操作(钩子操作)；实现一个模版方法作为算法的骨架。
    - 具体类(ConcreteClass)：实现原子操作
适用场景：
    - 一次性实现一个算法的不变的部分
    - 各个子类中的公共行为应该被提取出来并集中到一个公共父类中以避免代码重复
    - 控制子类扩展
'''
import time
from abc import abstractmethod, ABCMeta


class Window(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def stop(self):  # 原子操作/钩子操作/钩子函数
        pass

    def run(self):  # 模版方法
        self.start()
        while True:
            try:
                self.refresh()
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                break


class MyWindow(Window):
    def __init__(self, msg):
        self.msg = msg

    def start(self):
        print("开启窗口")

    def stop(self):
        print("关闭窗口")

    def refresh(self):
        print(self.msg)


# client
my_window = MyWindow("刷牙啦")
my_window.run()
