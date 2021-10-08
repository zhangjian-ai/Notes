'''
单向链表：
    - 是链表的一种。它由多个结点组成，每个结点由一个数据域和一个指针域组成，数据域用来存储数据，指针域用来指向其后继结点。
    - 链表的头结点的数据域不存储数据，指针域指向第一个真正存储数据的结点。

单向链表API设计：
    类名：
        - LinkList
    构造方法：
        - __init__(self): 创建LinkList对象，初始化成员变量
    成员方法：
        - clear(): 置空单向链表
        - isEmpty(): 判断单向链表是否为空，是返回true，否返回false
        - length(): 获取单向链表中的元素个数
        - get(i: int): 读取单向链表中第i个元素的值，如果没有第i个元素则返回-1
        - insert(i: int, value): 在单向链表的下标i处插入一个值为value的元素
        - add(value): 在单向链表的末尾添加一个元素
        - remove(i: int): 移除单向链表下标i处的元素并返回
        - indexOf(value): 返回单向链表中，首次出现value元素的下标，若不存在返回-1
    成员变量：
        - head: 首结点
        - N: 当前单向链表的长度
    成员内部类：
        - Node：结点类
            构造方法：
                - __init__(self, item, next): 创建一个Node结点对象，初始化数据item， 下一个结点类next
            成员变量：
                - item：结点存储的数据
                - next: 指向下一个结点
'''


class LinkList:
    class Node:
        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self):
        self.N = 0
        self.head = self.Node(None, None)

        # 迭代结点变量
        self.node = self.head

    def clear(self):
        self.N = 0
        self.head.next = None

    @property
    def isEmpty(self):
        return self.N == 0

    @property
    def length(self):
        return self.N

    def get(self, i: int):
        if not isinstance(i, int):
            raise TypeError
        if i >= self.N or i < 0:
            return -1

        node = self.head
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

        node = self.head
        index = 0
        while True:
            if index == i:
                # next_node即为当前i索引处的结点，插入时将其放到下一个结点去
                next_node = node.next
                cur = self.Node(value, next_node)
                node.next = cur
                self.N += 1
                break
            node = node.next
            index += 1

    def add(self, value):
        node = self.head
        while node.next:
            node = node.next

        cur = self.Node(value, None)
        node.next = cur
        self.N += 1

    def remove(self, i: int):
        if not isinstance(i, int):
            raise TypeError
        if i < 0 or i > self.N - 1:
            raise IndexError

        pre = self.head
        index = 0
        while pre.next:
            if index == i:
                cur = pre.next
                next = cur.next
                pre.next = next
                self.N -= 1
                return cur.item
            pre = pre.next
            index += 1

    def indexOf(self, value):
        node = self.head
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

        self.node = self.head  # 重置迭代位置
        raise StopIteration


if __name__ == '__main__':
    seq = LinkList()
    seq.add("姚明")
    seq.add("老张")
    seq.add("朱晓明")
    seq.add("好吧睡觉")
    # seq.add(1)
    # seq.add(2)

    # print(seq)
    # print(seq.get(0))
    # print(seq.isEmpty)
    #
    # seq.remove(3)
    # print(seq.get(3))
    print(seq.head.item)
    #
    seq.insert(0, "悍匪")
    # # print(seq.items)
    print(seq.indexOf("姚明"))
    print(seq.length)
    #
    # seq.clear()
    seq.add("调任新职")

    for i in seq:
        print(i)
