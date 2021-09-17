'''
观察者模式：定义对象间的一种一对多的依赖关系，当一个对象的状态发生变化时，所有依赖它的对象都得到通知并被自动更新。观察者模式又被称为"发布-订阅"模式。
角色：
    - 抽象主题(Subject)
    - 具体主题(ConcreteSubject)  --发布者
    - 抽象观察者(Observer)
    - 具体观察者(ConcreteObserver)  --订阅者
使用场景：
    - 当一个抽象模型有两方面，当其中一个方面依赖另一方面。将这两者封装在独立的对象中使他们可以各自独立的改变和复用。
    - 当对一个对象改变时需要同时改变其他对象，而不知道具体要改变几个对象。
    - 当一个对象必须通知其他对象，但又不知道其他对象具体是谁。换言之，你不希望这些对象是紧密耦合的。
优点：
    - 目标和观察者之间耦合度最小
    - 支持广播通信
'''

from abc import abstractmethod, ABCMeta


class Notice(metaclass=ABCMeta):  # 抽象主题
    def __init__(self):
        self.observers = []

    def attach(self, observer: object):
        self.observers.append(observer)

    def detach(self, observer: object):
        self.observers.remove(observer)

    def publish(self):
        for observer in self.observers:
            observer.update(self)


class Observer(metaclass=ABCMeta):  # 抽象观察者
    @abstractmethod
    def update(self, notice: object):
        pass


class InfoNotice(Notice):
    def __init__(self):
        super().__init__()
        self.__notification = None

    @property
    def notification(self):
        return self.__notification

    @notification.setter
    def notification(self, info):
        self.__notification = info
        self.publish()


class Staff(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, notice: object):
        self.message = notice.notification
        print(self.name, self.message)

    def __del__(self):
        print("deleted")


# client
s1 = Staff("小张")
s2 = Staff("小李")
p = InfoNotice()
p.attach(s1)
p.attach(s2)

p.notification = "中秋快乐！"
# p.detach(s1)
p.notification = "你好，勇士！"

