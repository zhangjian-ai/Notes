'''
在很对情况下，我们希望像遍历顺序表或者链表一样遍历树，但是由于树的结构，没办法从头到尾依次遍历。
目前主要的三种遍历树的方式：
    - 前序遍历：先访问根结点，再访问左子树，最后访问右子树
    - 中序遍历：先访问左子树，再访问根结点，最后访问右子树
    - 后序遍历：先访问左子树，再访问右子树，最后访问根结点

遍历方式 以根结点被访问的时机来命名。
中序遍历 是使用最广的一种遍历方式。
前序、中序、后序遍历被称之为基础遍历，采用深度优先的原则。
'''

from 二叉查找树之最大_最小值 import CustomBinaryTree
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class ErgodicBinaryTree(CustomBinaryTree):
    def __init__(self):
        super().__init__()

    # 前序遍历
    @property
    def pre_ergodic(self):
        queue = Queue()
        self.__pre_ergodic(self.root, queue)
        return queue

    def __pre_ergodic(self, node, queue):
        if not node:
            return

        # 前序遍历：先访问根结点，再访问左子树，最后访问右子树
        queue.enqueue(node.key)

        if node.left:
            self.__pre_ergodic(node.left, queue)

        if node.right:
            self.__pre_ergodic(node.right, queue)

    # 中序遍历
    @property
    def mid_ergodic(self):
        queue = Queue()
        self.__mid_ergodic(self.root, queue)
        return queue

    def __mid_ergodic(self, node, queue):
        if not node:
            return

        # 中序遍历：先访问左子树，再访问根结点，最后访问右子树
        if node.left:
            self.__mid_ergodic(node.left, queue)

        queue.enqueue(node.key)

        if node.right:
            self.__mid_ergodic(node.right, queue)

    # 后序遍历
    @property
    def after_ergodic(self):
        queue = Queue()
        self.__after_ergodic(self.root, queue)
        return queue

    def __after_ergodic(self, node, queue):
        if not node:
            return

        # 后序遍历：先访问左子树，再访问右子树，最后访问根结点
        if node.left:
            self.__after_ergodic(node.left, queue)

        if node.right:
            self.__after_ergodic(node.right, queue)

        queue.enqueue(node.key)


if __name__ == '__main__':
    e = ErgodicBinaryTree()
    e.put("E", 5)
    e.put("B", 2)
    e.put("G", 7)
    e.put("A", 1)
    e.put("D", 4)
    e.put("F", 6)
    e.put("H", 8)
    e.put("C", 3)

    for i in e.after_ergodic:
        print(i, end=',')
