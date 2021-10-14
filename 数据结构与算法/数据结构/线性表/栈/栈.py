'''
栈：
    栈是一种基于先进后出(FILO)的数据结构，是一种只能在一端进行插入和弹出操作的特殊线性表。
    按照先进后出的原则，先进入的元素压入栈底，最后的数据在栈顶，弹出数据时，从栈顶开始弹出。
    我们称数据进入栈的动作为 压栈， 数据从栈中出去的动作为 弹栈。

API设计：
    构造方法：
        - __init__() 创建Stack对象
    成员方法：
        - is_empty(): 判断栈是否为空，是返回True，否返回False
        - size(): 获取栈中的元素个数
        - pop(): 弹出栈顶元素
        - push(node: Node): 向栈中压入元素
    成员变量：
       - head：记录首结点
       - N：记录当前栈中元素个数
    成员内部类：
        - Node：
            构造方法：
                - __init__(self, item, next): 创建一个Node结点对象，初始化数据item， 下一个结点类next
            成员变量：
                - item: 结点存储的数据
                - next: 指向下一个结点
'''


class Stack:
    class Node:
        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self):
        self.head = self.Node(None, None)
        self.N = 0

        # 迭代结点变量
        self.node = self.head

    @property
    def is_empty(self):
        return self.N == 0

    @property
    def size(self):
        return self.N

    def push(self, item):
        # 拿到当前栈的第一个结点
        old_node = self.head.next

        # 创建一个新结点，并使其指向old_node
        new_node = self.Node(item, old_node)

        # 更新头结点的指向
        self.head.next = new_node

        # 栈中元素数量加一
        self.N += 1

    def pop(self):
        # 拿到当前栈的第一个结点
        old_node = self.head.next

        # 如果没有下一个结点直接返回None
        if not old_node:
            return None

        # 拿到当前栈的第二个结点
        new_node = old_node.next

        # 让头结点指向第二个结点，即弹出了第一个结点
        self.head.next = new_node

        # 栈中元素减一
        self.N -= 1

        # 返回被弹出的结点
        return old_node.item

    # 实现栈可迭代
    def __iter__(self):
        return self

    def __next__(self):
        if self.node.next:
            self.node = self.node.next
            return self.node.item

        self.node = self.head  # 重置迭代位置
        raise StopIteration


if __name__ == '__main__':
    s = Stack()
    s.push('a')
    s.push('b')
    s.push('c')
    s.push('d')

    for i in s:
        print(i)

    print('-------------')

    print(s.pop())
    print(s.size)

    print(s.pop())
    print(s.size)

    print(s.pop())
    print(s.is_empty)

    print(s.pop())
    print(s.is_empty)

    print(s.pop())
    print(s.is_empty)
