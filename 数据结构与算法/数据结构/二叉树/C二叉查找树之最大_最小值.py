"""
获取二叉查找树中，值最大的键、值最小的键。
在二叉查找树基础上新增以下两个成员方法：
    - min()：从树中找出值最小的key
    - __min(node)：从指定树node中，找出值最小的key
    - max()：从树中找出值最大的key
    - __max(node)：从指定树node中，找出值最大的key
"""

from B二叉查找树 import BinaryTree


class CustomBinaryTree(BinaryTree):
    @property
    def min(self):
        # root结点代表整棵树
        return self.__min(self.root).key

    def __min(self, node):
        # 判断当前结点是否有左子结点，如果有就继续往后找，如果没有则说明当前结点就是key最小的结点
        if node.left:
            return self.__min(node.left)
        return node

    @property
    def max(self):
        return self.__max(self.root).key

    def __max(self, node):
        # 判断当前结点是否有右子结点，如果有就继续往后找，如果没有则说明当前结点就是key最大的结点
        if node.right:
            return self.__max(node.right)
        return node


if __name__ == '__main__':
    b = CustomBinaryTree()
    b.put(3, '段誉')
    b.put(9, '杨过')
    b.put(8, '小龙女')
    b.put(7, '阿瑞斯')
    b.put(4, '万剑诀')
    b.put(10, '易筋经')
    b.put(11, '金刚经')
    b.put(1, '四相神功')
    b.put(20, '八卦掌')

    print(b.min)
    print(b.max)
