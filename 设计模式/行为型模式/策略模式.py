'''
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
'''

from abc import abstractmethod, ABCMeta


class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, command):
        pass


class FastStrategy(Strategy):
    def execute(self, command):
        print("快速执行命令-> %s" % command)


class SlowStrategy(Strategy):
    def execute(self, command):
        print("缓慢执行命令-> %s" % command)


class Context:
    def __init__(self, strategy: Strategy, command):
        self.strategy = strategy
        self.command = command

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def do_strategy(self):
        self.strategy.execute(self.command)


# client
cmd = "喝啤酒🍺🍺"
s1 = FastStrategy()
s2 = SlowStrategy()
context = Context(s2, cmd)
context.do_strategy()
context.set_strategy(s1)
context.do_strategy()
