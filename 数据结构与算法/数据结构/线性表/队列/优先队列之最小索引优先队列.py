'''
背景：
    最大优先队列和最小优先队列，可以轻易的获取到队列中的最大值或者最小值。但是并不能获取到其中任意的元素。
    弊端就是，当我们想修改队列中的元素时，就没办法快速的找到对应的找到元素去修改。

最小优先队列实现思路：
    - 在向队列中插入元素时，为每个元素绑定一个索引，即insert(int k, ele t)，k也就是列表的索引，这样就可以通过索引轻松找到需要修改的元素
    - 引入第一个辅助列 s1，用来保存步骤一中每个元素关联的索引。当我们给步骤一种队列排序时，就修改我们这个辅助列表中索引的顺序，这样就可以保持原队列中元素和索引的对应关系
    - 如果我们修改了队列索引0处的元素，打乱了队列顺序，那么我们需要遍历步骤二的辅助列表，找出列表中保存0的位置，在列表中进行上浮处理
        但是如果遍历列表，时间复杂度立马就变成了O(n)，所以我们再引入第二个辅助列表 s2。
    - s2 用来保存 s1 的逆序（把 s1 的值当作 s2 的索引，把 s1 的索引 当作 s2 的值），
        那么此时 s2 的索引就和 原始队列，一一对应。例如：修改了原始队列 索引0处的值，那么我们直接获取在s2中的索引0处的值，这个值
        作为 s1 的索引，那么这个索引 对应的值 再作为原始队列的索引，我们就通过简单的两步，就找到了需要做上浮处理的元素。
        大大降低了时间复杂度，此时时间复杂度为O(1).

API设计：
    类名：IndexMinPriorityQueue
    构造方法：
        - __init__(capacity) 实例化一个长度为 capacity 的IndexMinPriorityQueue对象
    成员方法：
        - less(i, j) 判断队列中索引i处的值是否小于索引j处的值
        - exch(i, j) 交换队列中索引i处和索引j处的值
        - del_min() 删除队列中最小的元素，并返回该元素关联的索引
        - insert(i, t) 往队列中插入一个元素t，并将其关联到索引i
        - swim(k) 使用上浮算法，使索引k处的元素处于一个正确的位置
        - sink(k) 使用下沉算法，使索引k处的元素处于一个正确的位置
        - size() 获取队列中元素的个数
        - is_empty() 判断队列是否为空
        - contains(k) 判断索引k处的元素是否存在
        - change_item(i, t) 把索引i处关联的元素，修改为t
        - min_index() 最小元素关联的索引
        - delete(i) 删除索引i关联的元素
    成员变量：
        - items 用来存储元素的列表，即原始队列
        - s1 保存items列表中元素的索引，该列表需要堆有序
        - s2 保存 s1 的逆序
        - N 记录队列中元素的个数
'''


class IndexMinPriorityQueue:
    def __init__(self, capacity):
        self.items = [None] * (capacity + 1)
        self.s1 = [None] * (capacity + 1)
        self.s2 = [None] * (capacity + 1)
        self.N = 0

    @property
    def size(self):
        return self.N

    @property
    def is_empty(self):
        return self.N == 0

    def less(self, i, j):
        return self.items[self.s1[i]] < self.items[self.s1[j]]

    def exch(self, i, j):
        # 交换元素实际上就是调整s1中的元素顺序，和原始队列没啥关系
        self.s1[i], self.s1[j] = self.s1[j], self.s1[i]

        # 更新s2逆序列表
        self.s2[self.s1[i]] = i
        self.s2[self.s1[j]] = j

    def contains(self, k):
        # 判断索引k处是否有值，就是看s2中该索引处又没有s1的逆序值
        return self.items[k] is not None

    def min_index(self):
        # 获取最小元素的索引，那就是s1中索引1处对应的值
        return self.s1[1]

    def insert(self, i, t):
        # 在索引i处插入元素t，先判断索引i是否已经被占用
        if self.contains(i):
            return

        # 元素个数加1
        self.N += 1

        # 在原始队列插入元素
        self.items[i] = t

        # 同时更新s1，s2
        self.s1[self.N] = i
        self.s2[i] = self.N

        # 通过上浮算法使s1中新插入的元素处于正确的位置
        self.swim(self.N)

    def del_min(self):
        # 删除队列中的最小值，该值的索引就是s1中索引1处的值
        min_ind = self.min_index()

        # 要删除s1索引1处的值，用s1中最大值与之替换后，再删掉原来的最大值即可
        self.exch(1, self.N)
        # 删除s2中的逆序
        self.s2[self.s1[self.N]] = None
        # 删除items中对应的值
        min_value = self.items[min_ind]
        self.items[min_ind] = None
        # 删除s1中最大索引处的值，s1列表要最后删
        self.s1[self.N] = None

        # 元素个数减1
        self.N -= 1

        # 使用下沉算法使s1中索引1对应的值位于合适的位置
        self.sink(1)

        return min_value

    def delete(self, i):
        # 找到i在s1中的索引
        k = self.s2[i]

        # 交换s1中k和N处的元素
        self.exch(k, self.N)
        # 删除s2中的逆序
        self.s2[self.N] = None
        # 删除items中的元素
        value = self.items[i]
        self.items[i] = None

        # 元素个数减1
        self.N -= 1

        # 先上浮，在下沉
        self.swim(k)
        self.sink(k)

        return value

    def change_item(self, i, t):
        # 修改队列指定索引处的值
        self.items[i] = t
        # 找到s1中i的位置
        k = self.s2[i]
        # 上浮下沉处理
        self.swim(k)
        self.sink(k)

    def swim(self, k):
        while k > 1:
            if self.less(k, int(k / 2)):
                self.exch(k, int(k / 2))

            k = int(k / 2)

    def sink(self, k):
        while 2 * k <= self.N:
            if 2 * k + 1 <= self.N and self.less(2 * k + 1, 2 * k):
                min_index = 2 * k + 1
            else:
                min_index = 2 * k

            # 比较当前结点和子结点的大小
            if self.less(min_index, k):
                self.exch(min_index, k)
                k = min_index
                continue

            break


if __name__ == '__main__':
    q = IndexMinPriorityQueue(5)
    q.insert(0, "A")
    q.insert(1, "C")
    q.insert(2, "F")
    q.change_item(2, "B")

    while not q.is_empty:
        print(q.del_min(), end=" ")