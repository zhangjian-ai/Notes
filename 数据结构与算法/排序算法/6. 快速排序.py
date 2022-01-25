"""
快速排序和归并排序类似，均采用分治思想。但是并不是左右均分，也不需要归并左右子序列。
快速排序重点在于分离序列：
    - 将序列第一个值作为标准值，并创建两个指针，分别是标准值的下标 lo 和序列的最大下标 hi
    - 先从 hi 处开始向下遍历，如果某个值小于 标准值则停止
    - 再从 lo 处开始向上遍历，如果某个值大于 标准值则停止
    - 如果 hi > lo， 交换 hi 和 lo 的值，再继续上面两步
    - 如果 hi == lo，停止遍历，如果标准值大于 hi 处的值，就交换 此时 hi 和 标准值 的位置
    - 将 交换后的标准值作为节点（没交换，就把 hi == lo 处的值作为分隔结点），把 标准值前后两部分分裂成 两个序列 再完成以上步骤。分裂的两个序列都不包含标准值
"""


def divide(a, l, m):
    # 执行一次快排，得到一个分隔节点
    position = quicksort(a, l, m)

    # 根据分隔节点，递归拆解序列
    # 前提是 position 有值，可以继续拆解
    if position:
        divide(a, l, position - 1)
        divide(a, position + 1, m)


def quicksort(a, l, m):
    """
    :param a:
    :param l:
    :param m:
    :return: 返回当前 排序序列的 分隔节点 的索引
    """

    # 执行快排的前提是最小下标小于最大下标
    # 否则直接返回
    if l >= m:
        return

    # 准备标准值即初始指针
    key = a[l]
    p1 = l
    p2 = m

    # 开始循环排序，把所有小于 标准值 的都放到 分隔结点前面，大于 标准值 的都放到 分隔结点后面
    while True:
        # 从序列末端依次往前找大于标准值的结点，找到就停止
        while key <= a[p2] and p1 < p2:
            p2 -= 1

        # 从序列前端依次往后找小于标准值的结点，找到就停止
        while key >= a[p1] and p1 < p2:
            p1 += 1

        # 当 p1、p2 都指向合适的值之后
        #   1、先判断 p1/p2 是否指向同一个值，如果是则表明 本次 交换即将结束。需要 把当前结点 跟 标准值 做比较。如果 标准值 大，
        #   就交换 标准值 和 指针指向的值，这样一来 就以 分隔结点 为界限，把 小于分隔结点都到其前面，大于 分隔结点的都放到其后面去了
        if p1 == p2:
            if key > a[p2]:
                a[l], a[p2] = a[p2], a[l]
            break
        else:
            #   2、p1/p2 不相等时，就交换两个指针处的值
            a[p1], a[p2] = a[p2], a[p1]

    return p2


class Solution:
    def merge(self, intervals: list) -> list:
        self.dfs(intervals, 0, len(intervals) - 1)
        return intervals

    def dfs(self, intervals: list, start: int, end: int):
        if start >= end:
            return

        p1 = start
        p2 = end
        s = intervals[start]

        while p1 < p2:
            while p1 < p2 and intervals[p1] <= s:
                p1 += 1

            while p1 < p2 and intervals[p2] >= s:
                p2 -= 1

            if p1 != p2:
                intervals[p1], intervals[p2] = intervals[p2], intervals[p1]

            elif intervals[p1] < s:
                intervals[start], intervals[p1] = intervals[p1], intervals[start]

        self.dfs(intervals, start, p1 - 1)
        self.dfs(intervals, p1, end)


if __name__ == '__main__':
    a = [3, 4, 2, 1, 7, 5, 10, 22, 17, 23, 14, 6, 9, 16, 27, 33, 31, 1, 13, 6, 7]
    b = [10, 7, 9, 11, 23, 15, 7, 2, 12, 17, 14, 13, 22, 6, 20, 1, 5, 8, 0, 3, 3, 2, 19, 4]

    divide(b, 0, len(b) - 1)
    s = Solution()

    print(s.merge(a))
    print(b)
