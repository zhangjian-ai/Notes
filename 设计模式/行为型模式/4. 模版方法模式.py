"""
模版方法模式：定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模版方法使得子类可以不改变一个算法的结构即可重新定义该算法的某些特定步骤。
角色：
    - 抽象类(AbstractClass)：定义抽象的原子操作(钩子操作)；实现一个模版方法作为算法的骨架。
    - 具体类(ConcreteClass)：实现原子操作
适用场景：
    - 一次性实现一个算法的不变的部分
    - 各个子类中的公共行为应该被提取出来并集中到一个公共父类中以避免代码重复
    - 控制子类扩展
"""
import time
from abc import ABCMeta, abstractmethod


class AbstractClass(metaclass=ABCMeta):
    """抽象类"""

    @abstractmethod
    def start(self) -> None:
        """原子操作/钩子"""
        pass

    @abstractmethod
    def operate(self) -> None:
        """原子操作/钩子"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """原子操作/钩子"""
        pass

    def run(self):
        """模板方法"""
        self.start()
        try:
            while True:
                self.operate()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


class BrowserWeb(AbstractClass):
    """具体类"""

    def start(self) -> None:
        print("打开浏览器...")

    def operate(self) -> None:
        print("浏览网页中...")

    def stop(self) -> None:
        print("关闭浏览器...")


if __name__ == '__main__':
    browser = BrowserWeb()
    browser.run()
