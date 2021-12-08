"""
桥模式：将一个事物的两个维度分离，使其都可以独立的变化
角色：
    - 抽象(Abstraction)
    - 细化抽象(RefinedAbstraction)
    - 实现者(Implementor)
    - 具体实现者(ConcreteImplementor)
应用场景：
    - 当事物有两个纬度上的表现，两个维度都需要扩展时。
优点：
    - 抽象和实现相分离
    - 优秀的扩展能力
"""

from abc import ABCMeta, abstractmethod


class Shape(metaclass=ABCMeta):
    """细化抽象类：形状"""

    @abstractmethod
    def draw(self, color) -> None:
        pass


class Color(metaclass=ABCMeta):
    """细化抽象类：颜色"""

    @abstractmethod
    def paint(self, shape) -> None:
        pass


class Red(Color):
    """具体实现者：颜色"""
    name = "红色"

    def paint(self, shape) -> None:
        print(f"绘制 {self.name} 的 {shape.name}")


class Green(Color):
    """具体实现者：颜色"""
    name = "绿色"

    def paint(self, shape) -> None:
        print(f"绘制 {self.name} 的 {shape.name}")


class Rectangle(Shape):
    """实现者：形状"""
    name = "长方形"

    def draw(self, color) -> None:
        color.paint(self)


class Square(Shape):
    """实现者：形状"""
    name = "正方形"

    def draw(self, color) -> None:
        color.paint(self)


# 在扩展时，不论是颜色还是形状都只需要新增一个具体类即可，非常方便
# -------client------
drawer = Rectangle()
drawer.draw(Red())
painter = Red()
painter.paint(Rectangle())
