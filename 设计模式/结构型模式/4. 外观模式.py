"""
外观模式：为子系统中的一组接口提供一个一致的界面，外观模式定义了一个高层接口，这个接口使得这一子系统更加容易使用
角色：
    - 外观(facade)
    - 子系统类(subsystem classes)
优点：
    - 减少系统相互依赖
    - 提高了灵活性
    - 提高了安全性
"""


from abc import ABCMeta, abstractmethod


class Standard(metaclass=ABCMeta):
    """抽象外观"""

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


class CPU(Standard):
    """子系统类"""

    def run(self) -> None:
        print("CPU启动")

    def stop(self) -> None:
        print("CPU停止")


class Memory(Standard):
    """子系统类"""

    def run(self) -> None:
        print("内存启动")

    def stop(self) -> None:
        print("内存停止")


class FacadeComputer(Standard):
    """统一外观"""

    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()

    def run(self) -> None:
        self.cpu.run()
        self.memory.run()

    def stop(self) -> None:
        self.cpu.stop()
        self.memory.stop()


if __name__ == '__main__':
    """客户端"""
    computer = FacadeComputer()
    computer.run()
    computer.stop()
