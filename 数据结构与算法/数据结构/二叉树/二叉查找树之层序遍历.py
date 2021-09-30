'''
层序遍历：
    - 就是按层从上往下遍历，每一层从左往右遍历。

实现思路：
    - 创建一个初始结点队列，默认先放入根结点；在创建一个存放键的队列，初始为None
    - 从结点队列中弹出一个结点，并做判断：
        - 如果当前结点的左子结点不为None，那么就将其左子结点放入到结点队列中
        - 如果当前结点的右子结点不为None，那么就将其右子结点放入到结点队列中
        - 将当前结点的key，放入到键队列中

层序遍历是二叉树的高级遍历，采用广度优先原则
'''

from 二叉查找树之前序_中序_后序遍历 import ErgodicBinaryTree
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class LayerErgodic(ErgodicBinaryTree):
    def __init__(self):
        super(LayerErgodic, self).__init__()

    # 层序遍历
    @property
    def layer_ergodic(self):
        # 创建两个队列
        nodes = Queue()
        nodes.enqueue(self.root)
        keys = Queue()

        # 循环遍历
        while not nodes.is_empty:
            # 从结点队列弹出一个结点
            node = nodes.dequeue()

            # 如果当前结点的左子结点不为None，那么就将其左子结点放入到结点队列中
            if node.left:
                nodes.enqueue(node.left)

            # 如果当前结点的右子结点不为None，那么就将其右子结点放入到结点队列中
            if node.right:
                nodes.enqueue(node.right)

            # 将当前结点的key，放入到键队列中
            keys.enqueue(node.key)

        return keys


if __name__ == '__main__':
    e = LayerErgodic()
    e.put("E", 5)
    e.put("B", 2)
    e.put("G", 7)
    e.put("A", 1)
    e.put("D", 4)
    e.put("F", 6)
    e.put("H", 8)
    e.put("C", 3)

    for i in e.layer_ergodic:
        print(i, end=',')
