"""
折纸问题：
    把一张纸放在桌上，向上对折依次，产生一条折痕，展开后这一条折痕向下，标记为 down；
    在此基础上再对折一次，共有3条折痕，展开后，折痕依次：向下、向下、向上，标记为 down down up

需求：
    给定一个对折次数 N，求出每一个折痕的方向标记

解决思路：
    - 将折痕倒置，看成一棵树。
    - 对折一次的 下折痕 为根结点
    - 每个结点的左子结点是下折痕
    - 每个节点的右子结点是上折痕
    - 对着次数 理解为 树的层数
"""

from 数据结构与算法.数据结构.线性表.队列.A队列 import Queue


class PaperFolding:
    # 定义结点类
    class Node:
        def __init__(self, item, left, right):
            self.item = item
            self.left = left
            self.right = right

    def __init__(self, N):
        self.N = N
        self.root = None

    def create_tree(self):
        """创建 折纸树 """
        # 安全性校验
        if self.N == 0:
            return None

        # 根据对着次数开始循环产生树
        for i in range(self.N):
            # 当没有根结点时，优先创建根结点
            if not self.root:
                self.root = self.Node("down", None, None)  # 根结点是下折痕
                continue

            # 有根结点需要找出当前结点的尾结点来添加新的子树
            # 这里采用 层序遍历 的思想来解决问题，默认放入根结点，因为要从根结点开始找
            queue = Queue()
            queue.enqueue(self.root)

            while not queue.is_empty:
                # 弹出队列中的一个结点
                node = queue.dequeue()

                # 如果当前结点有左子或者右子结点，那么就将其添加到队列
                if node.left:
                    queue.enqueue(node.left)
                if node.right:
                    queue.enqueue(node.right)

                # 如果当前结点既没有左子结点又没有右子结点，那么就为其创建新的子结点
                if not node.left and not node.right:
                    node.left = self.Node("down", None, None)
                    node.right = self.Node("up", None, None)

    def ergodic_tree(self, node=None):
        # 采用 中序遍历 思想遍历当前树
        # 安全性校验
        if not self.root:
            return None

        # 没有传入 node 时使用根结点
        if not node:
            node = self.root

        # 中序遍历
        if node.left:
            self.ergodic_tree(node.left)

        print(node.item, end=" ")

        if node.right:
            self.ergodic_tree(node.right)


if __name__ == '__main__':
    t = PaperFolding(3)
    t.create_tree()
    t.ergodic_tree()
