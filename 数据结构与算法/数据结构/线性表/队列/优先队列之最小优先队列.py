'''
最小优先队列：
    和最大优先队列相反，把最小值放到索引1处，那么每次取到的值就是最小值了。
    最要的区别就在于上浮、下沉算法的不同。
API设计：
    类名：MinPriorityQueue
    构造方法：
        - __init__(self, capacity) 创建容量为 capacity 的 MinPriorityQueue 对象
    成员方法：
        - less(i, j) 判断索引 i 处的值是否小于索引 j 处的值，返回 bool。
        - exch(i, j) 交换索引 i 和索引 j 处的值。
        - del_max() 删除队列中最大的元素，并返回这个元素。
        - insert(item) 往队列中插入一个元素 item。
        - swim(k) 使用上浮算法，使索引 k 处的值能在队列中处于一个正确的位置。
        - sink(k) 使用下沉算法，使索引 k 处的值能在队列中处于一个正确的位置。
        - size() 获取队列中的元素个数
        - is_empty() 判断队列是否为空
    成员变量：
        - items 用来保存元素的数组，python中用列表代替
        - N 队列中元素的个数
'''


class MinPriorityQueue:
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

    def del_min(self):
        # 索引1处的值就是最大值
        max_value = self.items[1]
        self.exch(1, self.N)
        # 判断一下是否有值可删
        if self.N == 0:
            raise ValueError
        self.N -= 1
        # 使用下沉算法把交换后的 索引 1 处的值放到合适的位置
        self.sink(1)

        return max_value

    def insert(self, item):
        self.items[self.N + 1] = item
        self.N += 1

        # 使用上浮算法，使新增后 索引 N 处的值位于合适的位置
        self.swim(self.N)

    def swim(self, index):
        while index > 1:
            # 判断当前结点是否比父结点大，如果是就交换位置并继续循环
            if not self.less(int(index / 2), index):
                self.exch(index, int(index / 2))
                index = int(index / 2)
                continue
            break

    def sink(self, index):
        while 2 * index <= self.N:
            # 找出子结点中较大的结点索引
            if 2 * index + 1 <= self.N and self.less(2 * index + 1, 2 * index):
                min_index = 2 * index + 1
            else:
                min_index = 2 * index

            # 判断当前结点是否大于子结点的较小值，如果是就下沉
            if self.less(min_index, index):
                self.exch(index, min_index)
                index = min_index
                continue

            break

    @property
    def size(self):
        return self.N

    @property
    def is_empty(self):
        return self.N == 0


if __name__ == '__main__':
    q = MinPriorityQueue(10)
    q.insert("A")
    q.insert("B")
    q.insert("C")
    q.insert("D")
    q.insert("E")
    q.insert("F")
    q.insert("G")
    q.insert("H")

    while not q.is_empty:
        item = q.del_min()
        print(item, end=" ")

