'''
适配器模式：将一个类的接口转换成客户希望的另一个接口。适配器模式使得原本不兼容的接口可以一起工作。
两种实现方式：
    - 类适配器：使用多继承。适配单个接口比较方便，适配多个接口代码比较冗余。
    - 对象适配器：使用组合。把多个需要适配的接口组合到一个适配器中。
角色：
    - 目标接口(Target)
    - 待适配的类(Adaptee)
    - 适配器(Adapter)
'''

from abc import abstractmethod, ABCMeta


class Payment(metaclass=ABCMeta):
    @abstractmethod
    def payment(self, money):
        pass


class AliPay(Payment):
    def payment(self, money):
        print("支付宝支付：%s" % money)


class WechatPay(Payment):
    def payment(self, money):
        print("微信支付：%s" % money)


class BankPay:
    def cost(self, money):  # 目标接口
        print("银联支付：%s" % money)


class ApplePay:
    def spend(self, money):
        print("苹果支付：%s" % money)


# 类适配器
# 把银联支付适配过来，尤其适用与不同代码的合并，这样既不影响已有代码，又能统一新增代码的调用方式
class PaymentAdapter(Payment, BankPay):
    def payment(self, money):
        return self.cost(money)


# 对象适配器
# 把多个不同的接口适配到统一的类中
class PaymentAdapter2(Payment):
    def __init__(self, pay: object):  # 构造函数需要传入一个支付实例
        self.pay = pay

    def payment(self, money):
        # 增加校验逻辑，根据不同实例的类型来调用不同的方法
        if isinstance(self.pay, BankPay):
            self.pay.cost(money)
        if isinstance(self.pay, ApplePay):
            self.pay.spend(money)


if __name__ == '__main__':
    p = PaymentAdapter()
    p.payment(100)

    # p2 = PaymentAdapter2(ApplePay())
    p2 = PaymentAdapter2(BankPay())
    p2.payment(20)
