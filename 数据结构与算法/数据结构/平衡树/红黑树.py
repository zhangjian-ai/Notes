'''
红黑树：
    - 用标准二叉树来实现的2-3二叉树，在树中用红连接来表示3-结点

红黑树是含有红黑连接并满足以下条件的二叉查找树：
    - 红连接均为左连接。
    - 没有任何一个结点同时和两条红连接相连。
    - 红黑树是完全黑色平衡的，即任意空连接到根结点的路径上的黑连接数量相同。
    - 根结点的color总是黑色的

红黑树的平衡化：
    左旋：当某个节点的左子结点为黑色，右子结点为红色，此时需要左旋。
    前提：当前结点为h，它的右子结点为x。
    左旋过程：
        1、让x的左子结点变为h的右子结点：h.right = x.left;
        2、让h称为x的左子结点：x.left = h;
        3、让h的color属性值变为x的color的属性值：x.color = h.color;
        4、让h的color属性变为RED：h.color = true;

    右旋：当某个节点的左子结点是红色，且左子结点的左子结点也是红色时，需要右旋。
    前提：当前结点为h，它的左子结点为x
    右旋过程：
        1、让x的右子结点称为h的左子结点：h.left = x.right;
        2、让h称为x的右子结点：x.right = h;
        3、让h的color属性值变为x的color的属性值：x.color = h.color;
        4、让h的color属性变为RED：h.color = true;

    颜色反转：
        当一个结点的左子结点、右子结点都是红色，那么就需要将当前结点的左子结点、右子结点有变为黑色，同时让当前结点变为红色。


API设计：
    类名：RedBlackTree
    构造方法：
        - __init__(self) 创建 RedBlackTree 对象
    成员方法：
        - is_red(Node h) 判断当前结点的父指向是否为red
        - rotate_left(Node h) 左旋调整
        - rotate_right(Node h) 右旋调整
        - flip_color(Node h) 颜色反转
        - put(key, value) 在整颗树上完成插入操作
        - __put(Node h, key, value) 在指定树中，完成插入操作，并返回添加新元素后的新树
        - get(key) 根据key，从树中找出对应的值
        - __get(Node h, key) 从指定的树 h中，根据 key 找出对应的值
        - size() 获取整个树中元素的个数
    成员变量：
        - root 记录根结点
        - N 记录树中的元素个数
    结点类：
        类名：Node
        构造方法：
            - __init__(self, key, value, left, right, color) 创建一个Node结点对象
        成员变量：
            - key 存储键
            - value 存储值
            - left 记录左子结点
            - right 记录右子结点
            - color 父结点指向当前结点的连接的颜色。bool值，true表示红色，false表示黑色
'''


class RedBlackTree:
    class Node:
        def __init__(self, key, value, left, right, color: bool):
            self.key = key
            self.value = value
            self.left = left
            self.right = right
            self.color = color

    def __init__(self):
        self.root = None
        self.N = 0

    @staticmethod
    def is_red(node):
        return node.color

    def rotate_left(self, h):
        #     前提：当前结点为h，它的右子结点为x。
        #     左旋过程：
        #         1、让x的左子结点变为h的右子结点：h.right = x.left;
        #         2、让h称为x的左子结点：x.left = h;
        #         3、让h的color属性值变为x的color的属性值：x.color = h.color;
        #         4、让h的color属性变为RED：h.color = true;
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = True

        return x

    def rotate_right(self, h):
        # 前提：当前结点为h，它的左子结点为x
        # 右旋过程：
        # 1、让x的右子结点称为h的左子结点：h.left = x.right;
        # 2、让h称为x的右子结点：x.right = h;
        # 3、让x的color属性值变为h的color的属性值：x.color = h.color;
        # 4、让h的color属性变为RED：h.color = true;
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = True

        return x

    def flip_color(self, h):
        h.color = True
        h.right.color = False
        h.left.color = False

    def put(self, key, value):
        self.root = self.__put(self.root, key, value)
        self.root.color = False

    def __put(self, h, key, value):
        # 如果h为None，则创建一个红色的新结点返回
        if not h:
            self.N += 1
            return self.Node(key, value, None, None, True)

        # 如果不是None，就比较要插入的key和当前结点key的大小
        if key < h.key:
            # 继续往左
            h.left = self.__put(h.left, key, value)
        elif key > h.key:
            # 继续往右
            h.right = self.__put(h.right, key, value)
        else:
            # 如果相等则发生值的替换
            h.value = value

        # 进行左旋：当某个节点的左子结点为黑色，右子结点为红色，此时需要左旋。
        if not h.left and h.right:
            h = self.rotate_left(h)

        # 进行右旋：当某个节点的左子结点是红色，且左子结点的左子结点也是红色时，需要右旋。
        if h.left and h.left.left:
            h = self.rotate_right(h)

        # 颜色反转：当一个结点的左子结点、右子结点都是红色，就进行颜色反转
        if h.left and h.right:
            self.flip_color(h)

        return h

    def get(self, key):
        return self.__get(self.root, key)

    def __get(self, h, key):
        # 如果h为None，则创建一个红色的新结点返回
        if not h:
            return None

        # 如果不是None，就比较要插入的key和当前结点key的大小
        if key < h.key:
            # 继续往左
            return self.__get(h.left, key)
        elif key > h.key:
            # 继续往右
            return self.__get(h.right, key)
        else:
            # 如果相等则发生值的替换
            return h.value

    def size(self):
        return self.N


if __name__ == '__main__':
    r = RedBlackTree()
    r.put(1, "张三")
    r.put(2, "赵四")
    r.put(3, "王五")

    print(r.get(1))
    print(r.get(2))
    print(r.get(4))
    print(r.size())
