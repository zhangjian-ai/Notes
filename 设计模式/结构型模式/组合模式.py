'''
组合模式：将对象组合成树形结构以表示"部分-整体"的层次结构，组合模式使得用户对单个对象和组合对象的使用具有一致性。
角色：
    - 抽象组件(Component)
    - 叶子组件(Leaf)
    - 复合组件(Composite)
    - 客户端(Client)
适用场景：
    - 表示对象的"部分-整体"层次结构(特别是结构是递归的)
    - 希望客户忽略组合对象和单个对象的不同，用户统一地使用组合结构中的所有对象
优点：
    - 定义了基本对象和组合对象的类层次结构
    - 简化客户端代码，客户端可以以相同方式使用单个对象和组合对象
    - 更容易增加新类型的组件
'''

from abc import abstractmethod, ABCMeta


# 抽象组件
class Graphic(metaclass=ABCMeta):  # 图形、图表抽象类
    @abstractmethod
    def draw(self):
        pass


# 叶子组件
class Point(Graphic):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return "点(%s, %s)" % (self.x, self.y)

    def draw(self):
        print("点(%s, %s)" % (self.x, self.y))


# 叶子组件
class Line(Graphic):
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return "线[%s, %s]" % (self.p1, self.p2)

    def draw(self):
        print("线[%s, %s]" % (self.p1, self.p2))


# 复合组件
class Picture(Graphic):
    def __init__(self, leaf: list):
        self.leaf = leaf

    def draw(self):
        for g in self.leaf:
            g.draw()


# client
p1 = Point(1, 2)
l2 = Line(Point(3, 4), Point(5, 6))
pic = Picture([p1, l2])
pic.draw()
