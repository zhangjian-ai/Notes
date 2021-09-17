'''
简单工厂模式：
    - 不直接向客户暴露对象创建的实现细节，而是通过一个工厂类来负责创建产品类的实例。
角色：
    - 工厂角色(creator)
    - 抽象产品角色(Product)
    - 具体产品角色(Concrete Product)

优点：
    - 隐藏了对象创建的细节
    - 客户端不需要修改代码
缺点：
    - 违反了单一职责原则，将创建逻辑集中到一个工厂类里
    - 当添加新产品时，需要修改工厂类代码，违反了开放封闭原则
'''

from abc import abstractmethod, ABCMeta


class Payment(metaclass=ABCMeta):
    """抽象产品角色"""
    @abstractmethod
    def payment(self, money):
        pass


class AliPay(Payment):
    """具体产品角色"""
    def payment(self, money):
        print("支付宝支付：%s" % money)


class WechatPay(Payment):
    def payment(self, money):
        print("微信支付：%s" % money)


class PaymentFactory:
    def create_payment(self, method):
        if method == "alipay":
            return AliPay()
        elif method == "wechat":
            return WechatPay()
        else:
            raise TypeError("no such payment named %s" % method)


if __name__ == '__main__':
    # 工厂类的作用就是来创建不同的实例对象，对外隐藏对象创建的细节
    factory = PaymentFactory()
    p = factory.create_payment("alipay")
    p.payment(100)
