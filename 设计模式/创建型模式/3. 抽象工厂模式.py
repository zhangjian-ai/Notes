"""
抽象工厂模式：
    - 定义一个工厂类接口，让工厂子类来创建一系列相关或相互依赖的对象。相比工厂方法模式，抽象工厂模式中的每个具体工厂都生产一套产品。
角色：
    - 抽象工厂角色(Creator)
    - 具体工厂角色(Concrete Creator)
    - 抽象产品角色(Product)
    - 具体产品角色(Concrete Product)
    - 客户端(Client)
优点：
    - 将客户端与类的具体实现相分离
    - 每个工厂创建了一个完整的产品系列，使得易于交换的产品系列
    - 有利于产品的一致性(即产品之间的约束关系)
缺点：
    - 难以支持新种类的(抽象)产品
"""

from abc import ABCMeta, abstractmethod


# ---------抽象产品类---------
class Shell(metaclass=ABCMeta):
    @abstractmethod
    def show_shell(self) -> None:
        pass


class CPU(metaclass=ABCMeta):
    @abstractmethod
    def show_cpu(self) -> None:
        pass


class OS(metaclass=ABCMeta):
    @abstractmethod
    def show_os(self) -> None:
        pass


# ---------抽象工厂类----------
class Factory(metaclass=ABCMeta):
    @abstractmethod
    def make_shell(self) -> Shell:
        pass

    @abstractmethod
    def make_cpu(self) -> CPU:
        pass

    @abstractmethod
    def make_os(self) -> OS:
        pass


# ----------具体产品类----------
class MiniShell(Shell):
    def show_shell(self) -> None:
        print("小手机壳")


class BigShell(Shell):
    def show_shell(self) -> None:
        print("大手机壳")


class SnapDragonCPU(CPU):
    def show_cpu(self) -> None:
        print("麒麟CPU")


class AppleCPU(CPU):
    def show_cpu(self) -> None:
        print("苹果CPU")


class AndroidOS(OS):
    def show_os(self) -> None:
        print("安卓系统")


class AppleOS(OS):
    def show_os(self) -> None:
        print("苹果系统")


# ---------具体工厂类---------
class XiaoMiFactory(Factory):
    def make_shell(self) -> Shell:
        return BigShell()

    def make_cpu(self) -> CPU:
        return SnapDragonCPU()

    def make_os(self) -> OS:
        return AndroidOS()


class AppleFactory(Factory):
    def make_shell(self) -> Shell:
        return MiniShell()

    def make_cpu(self) -> CPU:
        return AppleCPU()

    def make_os(self) -> OS:
        return AppleOS()


# ----------客户端----------
class Phone:
    def __init__(self, factory):
        self.shell = None
        self.cpu = None
        self.os = None
        self.make_phone(factory)

    def make_phone(self, factory):
        self.shell = factory.make_shell()
        self.cpu = factory.make_cpu()
        self.os = factory.make_os()

    def show_info(self):
        print("手机详情信息：")
        self.shell.show_shell()
        self.cpu.show_cpu()
        self.os.show_os()


if __name__ == '__main__':
    phone = Phone(AppleFactory())
    phone.show_info()
