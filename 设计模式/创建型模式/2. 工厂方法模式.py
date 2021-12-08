"""
工厂方法模式：
    - 定义一个用于创建对象的接口(工厂接口)，让子类决定实例化哪一个产品类。
角色：
    - 抽象工厂角色(Creator)
    - 具体工厂角色(Concrete Creator)
    - 抽象产品角色(Product)
    - 具体产品角色(Concrete Product)

优点：
    - 每个具体产品都对应一个具体工厂类，不需要修改工厂类代码
    - 隐藏了对象创建的实现细节
缺点：
    - 每增加一个具体产品类，就必须增加一个对应的具体工厂类
"""

from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):
    """抽象产品类"""

    @abstractmethod
    def pay(self, money) -> None:
        pass


class Factory(metaclass=ABCMeta):
    """抽象工厂类"""

    @abstractmethod
    def create(self) -> object:
        pass


class AliPay(Payment):
    """具体产品类"""

    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def pay(self, money) -> None:
        if self.use_huabei:
            print(f"花呗支付：{money}")
        else:
            print(f"支付宝支付：{money}")


class WechatPay(Payment):
    """具体产品类"""

    def pay(self, money) -> None:
        print(f"微信支付：{money}")


class AliFactory(Factory):
    """具体工厂类"""

    def create(self) -> AliPay:
        return AliPay()


class HuaBeiFactory(Factory):
    """具体工厂类"""

    def create(self) -> AliPay:
        return AliPay(use_huabei=True)


class WechatFactory(Factory):
    """具体工厂类"""

    def create(self) -> WechatPay:
        return WechatPay()


if __name__ == '__main__':
    # 工厂方法模式 相比于 简单工厂模式 ，就是把工厂类拆分，遵循 单一职责原则。每个工厂只实例化一种实例
    # 缺点也很明显，就是每新增一种 具体的产品类，就需要 同时新增一个 具体工厂类
    factory = AliFactory()
    pay = factory.create()

    pay.pay(100)
