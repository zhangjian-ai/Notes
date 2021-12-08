"""
建造者模式：
    - 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。
    - 建造者模式与抽象工厂模式相似，都用来创建复杂对象。主要区别是建造者模式着重一步步构造复杂对象，而抽象工厂模式着重于多个系列的产品对象。
角色：
    - 抽象建造者(Builder)
    - 具体建造者(Concrete Builder)
    - 指挥者(Director)
    - 产品(Product)

优点：
    - 隐藏了一个产品的内部结构和装配过程。
    - 将构造代码与表示代码分开。
    - 可以对构造过程进行更精细的控制。
"""

from abc import ABCMeta, abstractmethod


class Human:
    """产品类"""

    def __init__(self):
        self.face = None
        self.body = None
        self.legs = None

    def show(self):
        print(f"这是一位拥有 {self.face}、{self.body}、{self.legs} 的高质量人类。")


class Builder(metaclass=ABCMeta):
    """抽象建造者"""

    @abstractmethod
    def build_face(self):
        pass

    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_legs(self):
        pass


class LadyBuilder(Builder):
    """具体建造者"""

    def __init__(self):
        self.human = Human()

    def build_face(self):
        self.human.face = "尊贵而优雅的脸蛋"

    def build_body(self):
        self.human.body = "轻盈且多姿的身段"

    def build_legs(self):
        self.human.legs = "雪白又细长的大腿"


class KillerBuilder(Builder):
    """具体建造者"""

    def __init__(self):
        self.human = Human()

    def build_face(self):
        self.human.face = "肃杀且阴沉的面孔"

    def build_body(self):
        self.human.body = "紧绷且健硕的躯体"

    def build_legs(self):
        self.human.legs = "敏捷且持久的脚力"


class Director:
    """抽象指挥者"""

    def create(self, builder: Builder) -> Human:
        """具体的创建过程，由具体指挥者决定"""
        pass


class CreateDirector(Director):
    """具体指挥者"""

    def create(self, builder: Builder) -> Human:
        builder.build_face()
        builder.build_body()
        builder.build_legs()

        return builder.human


if __name__ == '__main__':
    director = CreateDirector()

    lady = director.create(LadyBuilder())
    lady.show()

    killer = director.create(KillerBuilder())
    killer.show()
