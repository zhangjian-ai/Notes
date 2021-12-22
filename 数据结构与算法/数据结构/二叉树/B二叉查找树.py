"""
二叉树：
    - 就是度不超过2的树。(每个结点最多有两个子结点)
满二叉树：
    - 一个二叉树，如果每一层的结点树都达到最大值，这个二叉树就是满二叉树。
完全二叉树：
    - 叶结点只能出现在最下层和次下层，并且最下面一层的结点都集中在该层最左边的若干位置的二叉树。

二叉查找树API设计：
    - 类名：BinaryTree
    - 成员变量：
        - root：记录根结点
        - N：记录树中元素个数
    - 成员方法：
        - put(key, value)：向树中插入一个键值对
        - __put(node, key, value) -> node：向指定树node中添加一个键值对，并返回添加后的新树
        - get(key)：根据key从树中找出对应的值
        - __get(node, key)：从指定树node中，根据key找出对应的值
        - delete(key)：根据key从树中删除对应的键值对
        - __delete(node, key)：从指定树node中，根据key从树中删除对应的键值对
        - size()：获取树中元素的个数
    - 结点类：
        - 类名：Node
        - 构造方法：
            - __init__(key, value, left, right) 创建一个Node对象
        - 成员变量：
            - key：存储键
            - value：存储值
            - left：记录左子结点
            - right：记录右子结点
"""


class BinaryTree:
    class Node:
        def __init__(self, key, value, left, right):
            self.key = key
            self.value = value
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.N = 0

    @property
    def size(self):
        return self.N

    def put(self, key, value):
        # 直接调用重载方法
        self.root = self.__put(self.root, key, value)

    def __put(self, node, key, value):
        # 当前树node中还没有任何结点时，直接返回新结点即可
        if not node:
            # 结点数加1
            self.N += 1
            return self.Node(key, value, None, None)

        # 当前树中已经存在结点，按照下面的原则插入元素
        # 如果新结点的key小于当前结点的key，那么继续查找左子结点
        # 如果新结点的key大于当前结点的key，那么继续查找右子结点
        # 如果新结点的key等于当前结点的key，那么说明树中已经存在相同的key，那么替换当前结点的值
        if key < node.key:
            node.left = self.__put(node.left, key, value)
        elif key > node.key:
            node.right = self.__put(node.right, key, value)
        else:
            node.value = value

        return node

    def get(self, key):
        # 直接返回重载方法
        return self.__get(self.root, key)

    def __get(self, node, key):
        # 如果树node中还没有任何结点
        if not node:
            return None

        # 当前树中已经存在结点，按照下面的原则查找元素
        # 如果新结点的key小于当前结点的key，那么继续查找左子结点
        # 如果新结点的key大于当前结点的key，那么继续查找右子结点
        # 如果新结点的key等于当前结点的key，那么说明已经找到了对应的结点，返回当前结点的值即可
        if key < node.key:
            return self.__get(node.left, key)
        elif key > node.key:
            return self.__get(node.right, key)
        else:
            return node.value

    def delete(self, key):
        # 直接调用重载方法
        self.root = self.__delete(self.root, key)

    def __delete(self, node, key):
        # 如果树node中还没有任何结点
        if not node:
            return None

        # 当前树中已经存在结点，按照下面的原则查找元素
        # 如果新结点的key小于当前结点的key，那么继续查找左子结点
        # 如果新结点的key大于当前结点的key，那么继续查找右子结点
        # 如果新结点的key等于当前结点的key，那么说明已经找到了对应的结点，删除当前结点
        if key < node.key:
            node.left = self.__delete(node.left, key)
        elif key > node.key:
            node.right = self.__delete(node.right, key)
        else:
            # 结点数减一
            self.N -= 1

            # 找到当前结点，就删除当前结点。删除结点后，树结构就被拆成了三部分，所以需要找一个仍然存在的结点来替换愿结点
            # 找出当前结点 右子树 中键最小的结点作为替换结点
            # 特殊场景即当前结点没有左子树或者右子树，那么就直接返回相反的子树即可
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # 找出 右子树 中键最小的结点作为替换结点
            min_node = node.right
            while min_node.left:
                # 如果 min_node.left.left 是None，那么久找到了最小结点
                if min_node.left.left is None:
                    # 断开最小结点与其父结点的链接
                    temp = min_node.left
                    min_node.left = None

                    # 更新最小结点
                    min_node = temp

                # 如果 min_node.left.left 不是None，就下一个
                min_node = min_node.left

            # 把当前结点的左子树、右子树 都转移到最小结点身上
            min_node.left = node.left
            if min_node != node.right:
                min_node.right = node.right

            # 返回最小结点，在递归的上一层就会使其成为当前被替换结点的父结点的子结点
            node = min_node

        # 返回当前结点
        return node


if __name__ == '__main__':
    b = BinaryTree()

    b.put(3, '段誉')
    b.put(9, '杨过')
    b.put(8, '小龙女')
    b.put(7, '阿瑞斯')
    b.put(4, '万剑诀')
    b.put(10, '易筋经')
    b.put(11, '金刚经')

    print(b.size)
    print(b.get(9))
    b.delete(7)

    print(b.get(3))
    print(b.get(8))
    print(b.get(9))

    print(b.get(4))

    print(b.get(7))
    print(b.size)
    b.delete(4)
    print(b.size)
    print(b.get(4))
    print(b.get(8))
    print(b.size)






