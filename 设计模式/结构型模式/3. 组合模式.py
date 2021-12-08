"""
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
"""

from abc import ABCMeta, abstractmethod


class Graphic(metaclass=ABCMeta):
    """抽象组件"""

    @abstractmethod
    def draw(self) -> None:
        pass


class Point(Graphic):
    """叶子组件"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self) -> None:
        print("专业画家描绘了一个点，坐标是(%s, %s)" % (self.x, self.y))


class Line(Graphic):
    """叶子组件"""

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self) -> None:
        print("专业画家描绘了一条线，端点坐标分别是(%s, %s)、(%s, %s)" % (self.p1.x, self.p1.y, self.p2.x, self.p2.y))


class Shape(Graphic):
    """复合组件"""

    def __init__(self, p: Point, l: Line):
        self.p = p
        self.l = l

    def draw(self) -> None:
        print("专业画家描绘了一条线和一个点，线段端点坐标分别是(%s, %s)、(%s, %s)；点的坐标是(%s, %s)" % (
            self.l.p1.x, self.l.p1.y, self.l.p2.x, self.l.p2.y, self.p.x, self.p.y))


if __name__ == '__main__':
    """客户端"""
    p = Point(1, 3)
    l = Line(Point(2, 4), Point(5, 7))
    s = Shape(p, l)

    p.draw()
    l.draw()
    s.draw()
