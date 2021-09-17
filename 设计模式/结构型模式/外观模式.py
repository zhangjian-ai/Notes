'''
外观模式：为子系统中的一组接口提供一个一致的界面，外观模式定义了一个高层接口，这个接口使得这一子系统更加容易使用
角色：
    - 外观(facade)
    - 子系统类(subsystem classes)
优点：
    - 减少系统相互依赖
    - 提高了灵活性
    - 提高了安全性
'''


class CPU:
    def run(self):
        print("CPU启动")

    def stop(self):
        print("CPU停止")


class Disk:
    def run(self):
        print("硬盘启动")

    def stop(self):
        print("硬盘停止")


class Memory:
    def run(self):
        print("内存启动")

    def stop(self):
        print("内存停止")


class Computer:  # 提供一个统一的高层接口，子系统之间没有依赖关系
    def __init__(self):
        self.cpu = CPU()
        self.disk = Disk()
        self.memory = Memory()

    def run(self):
        self.cpu.run()
        self.disk.run()
        self.memory.run()

    def stop(self):
        self.cpu.stop()
        self.disk.stop()
        self.memory.stop()


# client
computer = Computer()
computer.run()
computer.stop()
