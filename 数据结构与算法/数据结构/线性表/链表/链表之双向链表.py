'''
双向链表：
    - 是链表的一种。它由多个结点组成，每个结点由一个数据域和两个指针域组成，数据域用来存储数据，其中一个指针指向其后继结点，另一个指针指向其前驱结点。
    - 链表的头结点的数据域不存储数据，指向前驱结点的指针域值为None，指向后继结点的指针域指向第一个真正存储数据的结点。

双向链表API设计：
    类名：
        - TwoWayList
    构造方法：
        - __init__(self): 创建TwoWayList对象，初始化成员变量
    成员方法：
        - clear(): 置空双向链表
        - isEmpty(): 判断双向链表是否为空，是返回true，否返回false
        - length(): 获取双向链表中的元素个数
        - get(i: int): 读取双向链表中第i个元素的值，如果没有第i个元素则返回-1
        - insert(i: int, value): 在双向链表的下标i处插入一个值为value的元素
        - add(value): 在双向链表的末尾添加一个元素
        - remove(i: int): 移除双向链表下标i处的元素并返回
        - indexOf(value): 返回双向链表中，首次出现value元素的下标，若不存在返回-1
        - getFirst(): 获取第一个元素
        - getLast(): 获取最后一个元素
    成员变量：
        - first: 首结点
        - last: 尾结点
        - N: 当前双向链表的长度
    成员内部类：
        - Node：结点类
            构造方法：
                - __init__(self, item, pre, next): 创建一个Node结点对象，初始化数据item， 下一个结点类next
            成员变量：
                - item：结点存储的数据
                - pre: 指向前驱结点
                - next: 指向后继结点
'''


class TwoWayList:
    class Node:
        def __init__(self, item, pre, next):
            self.item = item
            self.pre = pre
            self.next = next

    def __init__(self):
        self.N = 0
        self.first = self.Node(None, None, None)
        self.last = None

        # 迭代结点变量
        self.node = self.first

    def clear(self):
        self.N = 0
        self.first.next = None
        self.last = None

    @property
    def isEmpty(self):
        return self.N == 0

    @property
    def length(self):
        return self.N

    @property
    def getFirst(self):
        return self.first

    @property
    def getLast(self):
        return self.last

    def get(self, i: int):
        if not isinstance(i, int):
            raise TypeError
        if i >= self.N or i < 0:
            return -1

        node = self.first
        index = 0
        while node.next:
            if index == i:
                return node.next.item
            node = node.next
            index += 1

    def insert(self, i: int, value):
        if not isinstance(i, int):
            raise TypeError

        if i < 0 or i > self.N:
            raise IndexError

        # i索引的前一个结点
        pre = self.first
        index = 0
        while True:
            if index == i:
                # i索引的后一个结点
                next_node = pre.next
                # 创建当前结点
                cur = self.Node(value, pre, next_node)
                # 把前一个结点的next指向当前结点
                pre.next = cur
                # 把后一个结点的pre指向当前结点
                if next_node:  # 若插入到最后一个结点位置，那么next_node应该是None
                    next_node.pre = cur
                # 结点数量加1
                self.N += 1
                break

            pre = pre.next
            index += 1

    def add(self, value):
        # 如果结点的next为None，则表明该结点为最后一个结点
        node = self.first
        while node.next:
            node = node.next

        cur = self.Node(value, node, None)
        node.next = cur
        self.N += 1

    def remove(self, i: int):
        if not isinstance(i, int):
            raise TypeError
        if i < 0 or i > self.N - 1:
            raise IndexError
        
        # i索引的前一个结点
        pre = self.first
        index = 0
        while pre.next:
            if index == i:
                # 当前结点
                cur = pre.next
                next_node = cur.next
                # 把前一个结点的next指向下一个结点；把下一个结点的pre指向前一个结点
                pre.next = next_node
                if next_node:  # 若删除的是最后一个结点，那么next_node为None
                    next_node.pre = pre
                self.N -= 1
                return cur.item
            pre = pre.next
            index += 1

    def indexOf(self, value):
        node = self.first
        index = 0
        while node.next:
            if node.next.item == value:
                return index
            node = node.next
            index += 1

        return -1

    # 实现链表可迭代
    def __iter__(self):
        return self

    def __next__(self):
        if self.node.next:
            self.node = self.node.next
            return self.node.item

        raise StopIteration


if __name__ == '__main__':
    seq = TwoWayList()
    seq.add("姚明")
    seq.add("老张")
    seq.add("朱晓明")
    seq.add("好吧睡觉")
    # seq.add(1)
    # seq.add(2)

    # print(seq)
    # print(seq.get(1))
    # print(seq.isEmpty)
    #
    # seq.remove(3)
    # print(seq.get(3))
    #
    seq.insert(2, "悍匪")
    # print(seq.indexOf("姚明"))
    # print(seq.length)
    #
    # seq.clear()
    seq.add("调任新职")

    for i in seq:
        print(i)

    print(seq.getFirst)
    print(seq.getLast)
