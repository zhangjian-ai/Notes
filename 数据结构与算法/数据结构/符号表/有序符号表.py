"""
有序符号表：
    - 就是按照符号表保存的键来排序。保证在新增元素过程中，符号表始终是有序的。
思路：
    - 继承符号表，重写其put()方法即可。
"""

from 符号表 import SymbolTable


class OrderSymbolTable(SymbolTable):

    def put(self, key, value):
        # 为保证符号表（从小到大）有序，那么在插入元素时，找到 符号表 中 第一个结点的key 比 新增键值对的key 大的结点，在该结点前插入新结点即可。
        # 仍然需要考虑key已存在的情况

        # 定义中间变量初值
        cur = self.head.next
        pre = self.head

        # 找出key的临界值
        while cur and key > cur.key:
            pre = cur
            cur = cur.next

        # 如果存在相同的key，那么新值覆盖旧值
        if cur and key == cur.key:
            cur.value = value
            return

        # 不存在相同的key就在临界点添加新结点
        new_node = self.Node(key, value, cur)
        pre.next = new_node

        self.N += 1


if __name__ == '__main__':
    s = OrderSymbolTable()
    s.put(1, '乔峰')
    s.put(7, '虚竹')
    s.put(5, '段誉')
    s.put(4, '阿紫')

    print(s.size)
    print(s.get(3))

    s.put(3, '阿朱')
    print(s.get(3))

    print(s.delete(1))

    print(s.size)
    print(s.get(1))
