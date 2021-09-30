'''
快慢指针：
    定义两个指针，这两个指针的移动速度一快一慢，以此来制造出自己想要的差值，这个差值帮我们找出链表上相应的结点。
    一般情况下，快指针的移动步长是慢指针的两倍。

中间值问题：
    即找出链表的中间值

思路：
    定义快慢指针，初始值都是头结点。当快指针移动到最后一个结点时，慢指针指向的值就是中间值。
'''

from 链表之单向链表 import LinkList


class MidValue(LinkList):
    def __init__(self):
        super(MidValue, self).__init__()

        # 生产结点
        self.node1 = self.Node('aa', None)
        self.node2 = self.Node('bb', None)
        self.node3 = self.Node('cc', None)
        self.node4 = self.Node('dd', None)
        self.node5 = self.Node('ee', None)
        self.node6 = self.Node('ff', None)
        self.node7 = self.Node('gg', None)
        self.node8 = self.Node('hh', None)
        self.node9 = self.Node('ii', None)

        # 完成结点指向
        self.head.next = self.node1
        self.node1.next = self.node2
        self.node2.next = self.node3
        self.node3.next = self.node4
        self.node4.next = self.node5
        self.node5.next = self.node6
        self.node6.next = self.node7
        self.node7.next = self.node8
        self.node8.next = self.node9

    def get_mid(self):
        # 定义快慢指针，快指针步长为2，慢指针步长为1
        fast = self.node1
        slow = self.node1

        # 开始循环遍历，当快指针走到尾结点时，慢指针停留的位置就是中间值
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next

        return slow


if __name__ == '__main__':
    mv = MidValue()
    node = mv.get_mid()
    print(node.item)
