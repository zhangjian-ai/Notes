"""
约瑟夫问题：
    约瑟夫和他的朋友加上39个犹太人一起玩自杀游戏，但是约瑟夫和他的朋友不想死。
规则：
    一共41个人围城一个圈，从一开始报数，当报数为三时，那个人就去自杀。然后下一个人继续从一开始数，如此循环。
    聪明的约瑟夫把自己和朋友的位置依次选在了16和31。
思路：
    利用循环链表验证 约瑟夫 是否正确
"""

from H循环链表 import LoopLinkList


class Joseph(LoopLinkList):
    def __init__(self):
        super().__init__(41)

        # 定义一个计数器
        self.count = 0
        # 定义当前报数的结点以及他的前一个结点
        self.pre = None
        self.now = self.first

    # 开始自杀游戏
    def kill_self(self):
        # 循环报数，按照此规则，当只剩最后一个人的时候，结束循环
        # 就是说当前结点的下一个结点是自己
        while self.now.next != self.now:
            # 计数器开始计数
            self.count += 1

            # 如果count等于3，就删除当前结点并重置count
            if self.count == 3:
                # 打印一下删除的结点
                print(self.now.item, end=',')

                self.pre.next = self.now.next
                self.now = self.now.next
                self.count = 0
            else:
                # 把上一个结点变为当前结点，当前结点变为下一个结点
                self.pre = self.now
                self.now = self.now.next

        # 打印最后一个剩下的结点
        print(self.now.item, end='')


if __name__ == '__main__':
    joseph = Joseph()
    joseph.kill_self()  # 约瑟夫很机智，逃过一劫。
