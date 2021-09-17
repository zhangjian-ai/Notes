'''
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
    - 每增加一个具体产品类，就必须增加一个响应的具体工厂类
'''

from abc import abstractmethod, ABCMeta


class Payment(metaclass=ABCMeta):
    """抽象产品角色"""

    @abstractmethod
    def payment(self, money):
        pass


class AliPay(Payment):
    """具体产品角色"""

    def __init__(self, use_huabei=False):
        self.use_huabei = use_huabei

    def payment(self, money):
        if self.use_huabei:
            print("花呗宝支付：%s" % money)
        else:
            print("支付宝支付：%s" % money)


class WechatPay(Payment):
    def payment(self, money):
        print("微信支付：%s" % money)


class Factory(metaclass=ABCMeta):
    """工厂接口"""

    @abstractmethod
    def create_payment(self):
        pass


class AlipayFactory(Factory):
    def create_payment(self):
        return AliPay()


class HuabeiFactory(Factory):
    def create_payment(self):
        return AliPay(use_huabei=True)


class WechatFactory(Factory):
    def create_payment(self):
        return WechatPay()


if __name__ == '__main__':
    factory = HuabeiFactory()
    p = factory.create_payment()
    p.payment(20)
