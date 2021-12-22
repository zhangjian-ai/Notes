"""
符号表：
    符号表最主要的目的是将一个键和一个值联系起来，符号表能够将存储的数据元素是一个键和一个值共同组成的键值对数据，我们可以根据键来查找对应的值。
    符号表中，键具有唯一性。

API设计：
    类名：
        - SymbolTable
    构造方法：
        - __init__() 创建一个SymbolTable对象
    成员方法：
        - get(key) 根据键key，找到对应的值
        - put(key, value) 向符号表中插入一个键值对
        - delete(key) 删除键为key的键值对
        - size() 获取符号表的大小
    成员变量：
        - head 记录首结点
        - N 记录键值对的个数
    成员内部类：
        类名：
            - Node
        成员变量：
            - key 存储键
            - value 存储值
            - next 下一个结点
"""


class SymbolTable:
    class Node:
        def __init__(self, key, value, next):
            self.key = key
            self.value = value
            self.next = next

    def __init__(self):
        # 头结点不存放键值，仅存放 指向 第一个结点 的指针
        self.head = self.Node(None, None, None)
        self.N = 0

    @property
    def size(self):
        return self.N

    def get(self, key):
        # 遍历符号表插队对应的key，并返回值
        node = self.head
        while node.next:
            node = node.next
            if node.key == key:
                return node.value

        # 如果循环完也没找到，就返回None
        return None

    def put(self, key, value):
        # 如果符号表中已经有相同的key，则覆盖该 键值对 的值
        node = self.head
        while node.next:
            node = node.next
            if node.key == key:
                node.value = value
                return

        # 如果没有相同的key，那么就创建一个新的结点。让head.next指向新结点
        old_first = self.head.next
        new_first = self.Node(key, value, old_first)
        self.head.next = new_first

        # 结点数加1
        self.N += 1

    def delete(self, key):
        # 遍历符号表找到对应的key，并删除
        node = self.head
        while node.next:
            if node.next.key == key:
                # 删除对应的key时，只需要让其上一个结点指向下一个结点即可。成功删除返回True
                node.next = node.next.next
                self.N -= 1
                return True

            # 下一个结点
            node = node.next

        # 没有删除返回False
        return False


if __name__ == '__main__':
    s = SymbolTable()
    s.put(1, '乔峰')
    s.put(2, '虚竹')
    s.put(3, '段誉')
    s.put(4, '阿紫')

    print(s.size)
    print(s.get(3))

    s.put(3, '阿朱')
    print(s.get(3))

    print(s.delete(1))

    print(s.size)
    print(s.get(1))
