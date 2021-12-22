"""
堆的特性：
    - 堆本身是一个完全二叉树。除了最后最后一层的结点不是满的，其他每一层结点都是满的。如果最后一层不满，那么要求左满右不满。
    - 堆通常用数组来实现(二叉查找树使用的链表来实现的)。具体方法就是将二叉树的结点按照层级顺序放入数组中。
        - 根结点放在位置 1 (位置 0 不使用，方便后序操作)
        - 它的左右子结点放在 2、3
        - 子结点的子结点则放在 4、5、6、7 以此类推
        * 如果一个结点的位置是 k，那么它的父结点的位置就是 [k/2]，而它的两个子结点位置分别为 2k,2k+1。
    - 每个节点的值 都大于等于它的两个子结点。这里规定父结点一定大于等于左右两个子结点，但两个子结点的位置并不作限制，区别于二叉查找树。
API设计：
    类名：Heap
    构造方法：
        - __init__(self, capacity) 创建容量为 capacity 的Heap对象
    成员方法：
        - less(i, j) 判断索引 i 处的值是否小于索引 j 处的值，返回 bool。
        - exch(i, j) 交换索引 i 和索引 j 处的值。
        - del_max() 删除堆中最大的元素，并返回这个元素。
        - insert(item) 往堆中插入一个元素 item。
        - swim(k) 使用上浮算法，使索引 k 处的值能在堆中处于一个正确的位置。
        - sink(k) 使用下沉算法，使索引 k 处的值能在堆中处于一个正确的位置。
    成员变量：
        - items 用来保存元素的数组，python中用列表代替
        - N 堆中元素的个数
"""


class Heap:
    def __init__(self, capacity):
        self.items = [None] * (capacity + 1)
        self.N = 0

    def less(self, i, j):
        if i > self.N or j > self.N:
            raise IndexError
        return self.items[i] < self.items[j]

    def exch(self, i, j):
        if i > self.N or j > self.N:
            raise IndexError
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def del_max(self):
        # 按照元素插入规则，堆中的最大值就是索引 1 处的值
        # 先用堆中最后一个值替换最大值，然后将最后一个值设置为空，就完成了元素的删除
        temp = self.items[1]
        self.items[1] = self.items[self.N]
        self.items[self.N] = None
        self.N -= 1

        # 使用下沉算法，将堆中首个元素放到合适的位置
        self.sink(1)

        return temp

    def insert(self, item):
        # 插入元素时，直接一次插入即可
        self.items[self.N + 1] = item
        self.N += 1

        # 使用上浮算法，将堆中最后一个元素放到合适的位置
        self.swim(self.N)

    def swim(self, k):
        # 使用上浮算法，使索引 k 处的值能在堆中处于一个正确的位置。
        while k > 1:  # 这里的条件需要大于1，因为0处没有保存值
            # 找出当前结点与其父结点的元素做比较，如果 当前元素 比父结点的元素大，那么久交换二者的位置
            if self.less(int(k / 2), k):
                # 交换值
                self.exch(k, int(k / 2))
                # 迭代k值
                k = int(k / 2)
                continue

            # 按照插入逻辑，子结点都是小于等于父结点的，所以 如果当前 父结点时大于当前结点的，那么就可以直接结束循环
            break

    def sink(self, k):
        # 使用下沉算法，使索引 k 处的值能在堆中处于一个正确的位置。
        while 2 * k <= self.N:  # 至少得有一个子结点有值才有循环的必要
            # 判断 2*K + 1是否有值
            # 找到当前结点 子结点中的 较大值
            if 2 * k + 1 <= self.N and self.less(2 * k, 2 * k + 1):
                m = 2 * k + 1
            else:
                m = 2 * k

            # 再判断当前结点和较大子结点的大小，如果当前结点小就交换位置
            if self.less(k, m):
                # 交换值
                self.exch(k, m)
                # 迭代k
                k = m
                continue

            # 如果当前结点已经比子结点大了，那么就直接结束循环
            break


if __name__ == '__main__':
    h = Heap(10)
    h.insert("A")
    h.insert("B")
    h.insert("E")
    h.insert("Q")
    h.insert("G")
    h.insert("Z")
    h.insert("C")
    h.insert("D")

    while h.N > 0:
        print(h.del_max(), end=" ")
