"""
适配器模式：将一个类的接口转换成客户希望的另一个接口。适配器模式使得原本不兼容的接口可以一起工作。
两种实现方式：
    - 类适配器：使用多继承。适配单个接口比较方便，适配多个接口代码比较冗余。
    - 对象适配器：使用组合。把多个需要适配的接口组合到一个适配器中。
角色：
    - 目标接口(Target)
    - 待适配的类(Adaptee)
    - 适配器(Adapter)
"""

from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):
    """抽象三方支付类"""

    @abstractmethod
    def pay(self, money) -> None:
        """抽象目标接口"""
        pass


class AliPay(Payment):
    """具体支付类"""
    def pay(self, money) -> None:
        print(f"支付宝支付: {money} 元")


class WechatPay(Payment):
    """具体支付类"""
    def pay(self, money) -> None:
        print(f"微信支付: {money} 元")


class BankPay:
    """待适配的类"""
    def cost(self, money) -> None:
        print(f"银联支付: {money} 元")


class ApplePay:
    """待适配的类"""
    def spend(self, money) -> None:
        print(f"苹果支付: {money} 元")


# 类适配器
# 把银联支付适配过来，尤其适用与不同代码的合并，这样既不影响已有代码，又能统一新增代码的调用方式
class BankPayAdapter(Payment, BankPay):
    """适配器"""
    def pay(self, money) -> None:
        self.cost(money)


# 对象适配器
# 把多个实例的不同的接口适配到统一的类中
class PayAdapter(Payment):
    """适配器"""
    def __init__(self, payer: object):
        self.payer = payer

    def pay(self, money) -> None:
        if isinstance(self.payer, BankPay):
            self.payer.cost(money)
        elif isinstance(self.payer, ApplePay):
            self.payer.spend(money)
        elif isinstance(self.payer, (AliPay, WechatPay)):
            self.payer.pay(money)
        else:
            raise TypeError(f"不支持的支付类: {type(self.payer)}. 如需要支持该支付类，请扩展适配接口。")


if __name__ == '__main__':
    p = BankPayAdapter()
    p.pay(100)

    p2 = PayAdapter(AliPay())
    # p2 = PayAdapter(BankPay())
    p2.pay(20)
