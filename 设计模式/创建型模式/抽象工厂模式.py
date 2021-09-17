'''
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
    - 每个工厂创建了一个完成的产品系列，使得易于交换的产品系列
    - 有利于产品的一致性(即产品之间的约束关系)
缺点：
    - 难以支持新种类的(抽象)产品
'''

from abc import abstractmethod, ABCMeta


# ------------抽象产品------------
class PhoneShell(metaclass=ABCMeta):
    @abstractmethod
    def show_shell(self):
        pass


class CPU(metaclass=ABCMeta):
    @abstractmethod
    def show_cpu(self):
        pass


class OS(metaclass=ABCMeta):
    @abstractmethod
    def show_os(self):
        pass


# ------------抽象工厂------------
class Factory(metaclass=ABCMeta):
    @abstractmethod
    def make_shell(self):
        pass

    @abstractmethod
    def make_cpu(self):
        pass

    @abstractmethod
    def make_os(self):
        pass


# ------------具体产品------------
class BigShell(PhoneShell):
    def show_shell(self):
        print("一个大手机壳")


class MiniShell(PhoneShell):
    def show_shell(self):
        print("一个小手机壳")


class SnapDragonCPU(CPU):
    def show_cpu(self):
        print("骁龙CPU")


class KirinCPU(CPU):
    def show_cpu(self):
        print("麒麟CPU")


class AppleCPU(CPU):
    def show_cpu(self):
        print("苹果CPU")


class Android(OS):
    def show_os(self):
        print("安卓系统")


class IOS(OS):
    def show_os(self):
        print("IOS")


# ------------具体工厂------------
class MiFactory(Factory):
    def make_shell(self):
        return MiniShell()

    def make_os(self):
        return Android()

    def make_cpu(self):
        return SnapDragonCPU()


class HuaweiFactory(Factory):
    def make_shell(self):
        return BigShell()

    def make_os(self):
        return Android()

    def make_cpu(self):
        return KirinCPU()


class IphoneFactory(Factory):
    def make_shell(self):
        return BigShell()

    def make_os(self):
        return IOS()

    def make_cpu(self):
        return AppleCPU()


# ------------客户端------------
class Phone:
    def __init__(self, shell, os, cpu):
        self.cpu = cpu
        self.shell = shell
        self.os = os

    def show_info(self):
        print("手机信息：")
        self.cpu.show_cpu()
        self.os.show_os()
        self.shell.show_shell()


def make_phone(factory):
    shell = factory.make_shell()
    os = factory.make_os()
    cpu = factory.make_cpu()

    return Phone(shell, os, cpu)


if __name__ == '__main__':
    phone = make_phone(IphoneFactory())
    phone.show_info()
