'''
队列：
    - 队列是一种基于先进先出(FIFO)的数据结构，是一种只能在一端进行插入，在另一端进行删除操作的特殊线性表。
    - 先进先出就是指，先存储的数据，在读取数据时先被读出来。

API设计：
    构造方法：
        - __init__() 创建Queue对象
    成员方法：
        - is_empty(): 判断栈是否为空，是返回True，否返回False
        - size(): 获取队列中的元素个数
        - dequeue(): 取出一个队列中的元素
        - enqueue(node: Node): 向队列中插入一个元素
    成员变量：
       - head：记录首结点
       - last：记录尾结点
       - N：记录当前栈中元素个数
    成员内部类：
        - Node：
            构造方法：
                - __init__(self, item, next): 创建一个Node结点对象，初始化数据item， 下一个结点类next
            成员变量：
                - item: 结点存储的数据
                - next: 指向下一个结点
'''


class Queue:
    class Node:
        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self):
        self.head = self.Node(None, None)
        self.last = None
        self.N = 0

        # 迭代结点变量
        self.node = self.head

    @property
    def is_empty(self):
        return self.N == 0

    @property
    def size(self):
        return self.N

    def enqueue(self, item):
        # 如果队列是空
        if self.N == 0:
            # 直接head结点指向一个新结点，并把其作为last结点
            self.head.next = self.Node(item, None)
            self.last = self.head.next
        else:
            # 队列不为空时，直接让last结点指向一个新结点，并更新last为新结点
            self.last.next = self.Node(item, None)
            self.last = self.last.next

        self.N += 1

    def dequeue(self):
        # 如果队列为空直接返回None
        if self.N == 0:
            return None

        # 不为空时，就返回当前head.next，并更新head.next
        old_first = self.head.next
        self.head.next = old_first.next

        # 数量减1
        self.N -= 1

        # 如果数量为0，那么重置last结点为None
        if self.N == 0:
            self.last = None

        return old_first.item

    # 实现队列可迭代
    def __iter__(self):
        return self

    def __next__(self):
        if self.node.next:
            self.node = self.node.next
            return self.node.item

        self.node = self.head  # 重置迭代位置
        raise StopIteration


if __name__ == '__main__':
    q = Queue()
    q.enqueue('a')
    q.enqueue('b')
    q.enqueue('c')
    q.enqueue('d')

    for i in q:
        print(i)

    print('---------')

    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())

    print(q.is_empty)
    print(q.size)
