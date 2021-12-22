"""
堆排序：
    - 利用堆的特性，完成对一个无序列表从小到大的排序。
API设计：
    类名：HeapSort
    构造方法：
        - __init__(self, source:list) 创建一个HeapSort对象，传入原始无序列表
    成员方法：
        - sort(source) 对数组进行从小到大的排序
        - create_heap(source) 根据原始数组source创建出堆heap
        - less(source, i, j) 判断索引i处的值是否小于索引j处的值
        - exch(source, i, j) 交换索引i 和 索引j 处的值
        - sink(source, target, scope) 对target索引处的值做下沉处理，下沉范围是 scope
"""


class HeapSort:
    def __init__(self, source):
        # 直接创建堆heap
        self.heap = self.create_heap(source)

    def create_heap(self, source):
        # 堆中的第一个索引不保存值
        temp_heap = [None]
        temp_heap.extend(source)  # 该方法无返回值，就地扩展列表

        # 对临时堆中的元素从 len(temp_heap)/2 处开始向索引1 处遍历，依次做下沉处理
        # 根据堆的特性，len(temp_heap)/2 后面的结点，都是叶子结点，不需要做下沉处理。需要做下沉处理的只是非叶子结点。
        for index in range(int(len(source) / 2), 0, -1):
            self.sink(temp_heap, index, len(source) - 1)

        # 返回一个从大到小的列表
        return temp_heap

    def sink(self, source, index, scope):
        # 判断是否有叶子结点，有则继续循环
        while 2 * index <= scope:
            # 找出叶子结点中的较大值
            if 2 * index + 1 <= scope and self.less(source, 2 * index, 2 * index + 1):
                max = 2 * index + 1
            else:
                max = 2 * index

            # 再判断当前结点和较大子结点的大小，如果当前结点小就交换位置
            if self.less(source, index, max):
                self.exch(source, index, max)
                index = max
                continue

            # 如果当前结点已经比子结点大了，那么就直接结束循环
            break

    def less(self, source: list, i, j):
        return source[i] < source[j]

    def exch(self, source: list, i, j):
        source[i], source[j] = source[j], source[i]

    def sort(self):
        # 将heap从小到大排序
        for index in range(len(self.heap) - 1, 1, -1):  # 当索引是1时，则没必要在做后续操作
            # 先交换index索引和索引1处的值，把最大值放到最后一个索引
            self.exch(self.heap, 1, index)
            # 对索引1处的值做下沉处理，下沉处理要排除最后一位，如此循环
            self.sink(self.heap, 1, index - 1)

        return self.heap


if __name__ == '__main__':
    source = ['S', 'O', 'R', 'T', 'E', 'X', 'A', 'M', 'P', 'L', 'E']
    heap = HeapSort(source)
    source = heap.sort()

    print(source)
