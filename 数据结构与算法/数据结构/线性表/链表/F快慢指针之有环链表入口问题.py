"""
有环链表入口：
    即有环链表中，被逆向指向的那个结点即是环的入口。

思路：
    当快慢指针重合时，说明链表有环，与此同时定义一个步长为1的虚拟指针指向头结点。
    随后继续遍历链表，当虚拟指针和慢指针重合时，那么此时虚拟指针指向的就是环的入口。
"""

from E快慢指针之单向链表是否有环 import CircleList


class CircleExtendList(CircleList):

    def __init__(self):
        super(CircleExtendList, self).__init__()

    def get_entrance(self):
        # 定义快慢指针，快指针步长为2，慢指针步长为1
        # 定义虚拟指针为None
        fast = self.node1
        slow = self.node1
        virtual = None

        # 开始循环遍历
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            # 快慢指针重合则说明有环
            # 如果此时虚拟指针为 None，那就给虚拟指针赋初值
            if fast == slow and virtual is None:
                virtual = self.node1

            # 如果虚拟指针不为空，那么虚拟指针也跟随遍历，步长同慢指针
            if virtual:
                # 当虚拟指针和慢指针重合时的结点就是环的入口，结束循环
                if slow == virtual:
                    break

                virtual = virtual.next

        return virtual


if __name__ == '__main__':
    cxl = CircleExtendList()
    node = cxl.get_entrance()
    print(node.item)
