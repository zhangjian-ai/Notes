"""
有环：
    即在单向列表中，不是所有结点都依次指向下一个结点，存在结点指向了它前面的结点。
思路：
    定义快慢指针，遍历链表。如果快慢指针重合，那么就存在环。
"""

from D快慢指针之中间值问题 import MidValue


class CircleList(MidValue):
    def __init__(self):
        super(CircleList, self).__init__()

        # 产生环
        self.node9.next = self.node3

    def has_circle(self) -> bool:
        # 定义快慢指针，快指针步长为2，慢指针步长为1
        fast = self.node1
        slow = self.node1

        # 开始循环遍历
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

            # 快慢指针重合则说明有环
            if fast == slow:
                return True

        return False


if __name__ == '__main__':
    cl = CircleList()
    bl = cl.has_circle()
    print(bl)
