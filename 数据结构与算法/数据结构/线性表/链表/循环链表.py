'''
循环链表：
    在单向链表的基础上，让尾结点指向首结点，便构成了循环链表。
'''


class LoopLinkList:
    class Node:
        """结点类"""

        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self, n):
        """
        :param n: 链表结点数量
        """
        # 定义属性：首结点、当前结点
        self.first = None
        self.cur = None

        # 生成循环链表
        for i in range(1, n + 1):
            # 如果是第一个结点，将其赋值给 first 和 cur
            if i == 1:
                self.first = self.Node(i, None)
                self.cur = self.first
                continue

            # 如果不是首结点，那么就让当前结点指向新结点，然后更新当前结点
            new_node = self.Node(i, None)
            self.cur.next = new_node
            self.cur = new_node

            # 如果是尾结点，就让其指向首结点
            if i == n:
                self.cur.next = self.first
