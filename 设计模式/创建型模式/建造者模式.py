'''
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
缺点：

'''

from abc import abstractmethod, ABCMeta


class Player:
    def __init__(self, face=None, body=None, leg=None):
        self.face = face
        self.body = body
        self.leg = leg

    def __str__(self):
        return "%s , %s , %s" % (self.face, self.body, self.leg)


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def build_face(self):
        pass

    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_leg(self):
        pass


class SexLadyBuilder(Builder):
    def __init__(self):
        self.player = Player()

    def build_face(self):
        self.player.face = "尊贵而优雅的脸蛋"

    def build_body(self):
        self.player.body = "窈窕且轻盈的身姿"

    def build_leg(self):
        self.player.leg = "雪白又纤长的大腿"


class MonsterBuilder(Builder):
    def __init__(self):
        self.player = Player()

    def build_face(self):
        self.player.face = "丑陋的脸蛋"

    def build_body(self):
        self.player.body = "肥胖的身躯"

    def build_leg(self):
        self.player.leg = "拐弯的大腿"


class PlayerDirector:  # 控制组装顺序
    def build_player(self, builder):
        builder.build_face()
        builder.build_body()
        builder.build_leg()

        return builder.player


# client
# builder = SexLadyBuilder()
builder = MonsterBuilder()
director = PlayerDirector()
p = director.build_player(builder)
print(p)
