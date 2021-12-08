"""
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
"""

from abc import ABCMeta, abstractmethod


class Observer(metaclass=ABCMeta):
    """抽象观察者"""

    @abstractmethod
    def listen(self, message) -> None:
        pass


class Subject(metaclass=ABCMeta):
    """抽象主题"""

    OBSERVER = []

    @classmethod
    def register(cls, observer: Observer) -> list:
        cls.OBSERVER.append(observer)
        return cls.OBSERVER

    @classmethod
    def remove(cls, observer: Observer) -> Observer:
        cls.OBSERVER.remove(observer)
        return observer

    @abstractmethod
    def publish(self, message) -> None:
        pass


class ConcreteSubject(Subject):
    """具体主题发布者"""

    def publish(self, message) -> None:
        """发布消息给订阅者"""
        for observer in self.OBSERVER:
            observer.listen(message)


class ConcreteObserver1(Observer):
    """具体订阅者"""

    def __init__(self):
        self.message = None

    def __str__(self):
        return f"订阅者一号：收到消息 {self.message}"

    def listen(self, message) -> None:
        self.message = message


class ConcreteObserver2(Observer):
    """具体订阅者"""

    def __init__(self):
        self.message = None

    def __str__(self):
        return f"订阅者二号：收到消息 {self.message}"

    def listen(self, message) -> None:
        self.message = message


if __name__ == '__main__':
    observer_01 = ConcreteObserver1()
    observer_02 = ConcreteObserver2()

    ConcreteSubject.register(observer_01)
    ConcreteSubject.register(observer_02)

    subject = ConcreteSubject()
    subject.publish("欢迎你，我的勇士！")

    print(observer_01)
    print(observer_02)
