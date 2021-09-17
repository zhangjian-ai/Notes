'''
快速排序和归并排序类似，均采用分治思想。但是并不是左右均分，也不需要归并左右子序列。
快速排序重点在于分离序列：
    - 将序列第一个值作为标准值，并创建两个指针，分别是标准值的下标 lo 和序列的最大下标 hi
    - 先从 hi 处开始向下遍历，如果某个值小于 标准值则停止
    - 再从 lo 处开始向上遍历，如果某个值大于 标准值则停止
    - 如果 hi > lo， 交换 hi 和 lo 的值，再继续上面两步
    - 如果 hi == lo，停止遍历，如果标准值大于 hi 处的值，就交换 此时 hi 和 标准值的位置
    - 将 交换后的标准值作为节点，把 标准值前后两部分分裂成 两个序列 再完成以上步骤。分裂的两个序列都不包含标准值
'''


def quicksort(a, min, max):
    if min >= max:
        return

    key = a[min]
    p1 = min
    p2 = max

    while True:

        while key <= a[p2] and p1 < p2:
            p2 -= 1

        while key >= a[p1] and p1 < p2:
            p1 += 1

        if p1 == p2:
            if key > a[p2]:
                a[min], a[p2] = a[p2], a[min]
            break
        else:
            a[p1], a[p2] = a[p2], a[p1]

    return p2


def divide(a, min, max):
    position = quicksort(a, min, max)

    # 递归调用
    if position:
        divide(a, min, position - 1)
        divide(a, position + 1, max)


if __name__ == '__main__':
    a = [3, 4, 2, 1, 7, 5, 10, 22, 17, 23, 14, 6, 9, 16, 27, 33, 31, 1, 13, 6, 7]

    min = 0
    max = len(a) - 1

    divide(a, min, max)

    print(a)
