'''
最大深度：
    就是找出二叉树的最大层数。
'''

from 二叉查找树之前序_中序_后序遍历 import ErgodicBinaryTree


class DeepBinaryTree(ErgodicBinaryTree):
    def __init__(self):
        super().__init__()

    @property
    def max_deep(self):
        """找出整棵树的对大深度"""
        return self.__max_deep(self.root)

    def __max_deep(self, node):
        """找出当前结点的深度"""
        if not node:
            return 0

        # 当前结点左子树深度
        max_l = 0
        # 当前结点右子树深度
        max_r = 0

        # 找出左子树最大深度
        if node.left:
            max_l = self.__max_deep(node.left)

        # 找出右子树最大深度
        if node.right:
            max_r = self.__max_deep(node.right)

        # 当前结点深度为左右子结点深度较大值加一
        max_cur = max(max_l, max_r) + 1

        return max_cur


if __name__ == '__main__':
    e = DeepBinaryTree()
    e.put("E", 5)
    e.put("B", 2)
    e.put("G", 7)
    e.put("A", 1)
    e.put("D", 4)
    e.put("F", 6)
    e.put("H", 8)
    e.put("C", 3)

    print(e.max_deep)
