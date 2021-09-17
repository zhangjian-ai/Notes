'''
桥模式：将一个事物的两个维度分离，使其都可以独立的变化
角色：
    - 抽象(Abstraction)
    - 细化抽象(RefinedAbstraction)
    - 实现者(Implementor)
    - 具体实现着(ConcreteImplementor)
应用场景：
    - 当事物有两个纬度上的表现，两个维度都需要扩展时。
优点：
    - 抽象和实现相分离
    - 优秀的扩展能力
'''

from abc import ABCMeta, abstractmethod


class Shape(metaclass=ABCMeta):  # 形状的纬度
    @abstractmethod
    def draw(self, color: object):
        pass


class Color(metaclass=ABCMeta):  # 颜色的纬度，通过传参的方式和形状弱关联，既不规定入参具体的形状和颜色
    @abstractmethod
    def paint(self, shape: object):
        pass


class Red(Color):
    def paint(self, shape: object):
        # 绘制红色的图案
        print("红色的 %s" % shape.name)


class Green(Color):
    def paint(self, shape: object):
        # 绘制红色的图案
        print("绿色的 %s" % shape.name)


class Rectangle(Shape):
    name = "矩形"

    def draw(self, color: object):
        color.paint(self)  # color的paint需要传入一个形状对象，把自己传进去


class Square(Shape):
    name = "正方形"

    def draw(self, color: object):
        color.paint(self)


# 在扩展时，不论是颜色还是形状都只需要新增一个具体类即可，非常方便
# client
# drawer = Rectangle()
# drawer.draw(Red())
drawer = Red()
drawer.paint(Rectangle())

