"""
策略模式：定义一系列的算法，把他们一个个的封装起来，并使他们可相互替换。本模式使得算法可独立于使用它的客户而变化。
角色：
    - 抽象策略(Strategy)
    - 具体策略(ConcreteStrategy)
    - 上下文(Context)
优点：
    - 定义了一些列可复用的算法和行为
    - 消除了一些条件语句
    - 可以提供相同行为的不同实现
缺点：
    - 客户必须了解不同的策略
"""

from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):
    """抽象策略"""

    @abstractmethod
    def execute(self, cmd) -> None:
        pass


class FastStrategy(Strategy):
    """具体策略"""

    def execute(self, cmd) -> None:
        print("快速执行命令：%s" % cmd)


class SlowStrategy(Strategy):
    """具体策略"""

    def execute(self, cmd) -> None:
        print("墨迹执行命令：%s" % cmd)


class Context:
    """上下文"""

    def __init__(self, strategy: Strategy, cmd: str):
        self.__strategy = strategy
        self.cmd = cmd

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, st: Strategy):
        self.__strategy = st

    def execute(self):
        self.__strategy.execute(self.cmd)


if __name__ == '__main__':
    cmd = "喝啤酒🍺"

    context = Context(FastStrategy(), cmd)
    context.execute()

    context.strategy = SlowStrategy()
    context.execute()
