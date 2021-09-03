'''
归并排序（MERGE-SORT）是利用归并的思想实现的排序方法。
该算法采用经典的分治（divide-and-conquer）策略。
分治法将问题分(divide)成一些小的问题然后递归求解，而治(conquer)的阶段则将分的阶段得到的各答案"修补"在一起，即分而治之。
'''

a = [6, 4, 2, 1, 7, 5, 10, 22, 17, 23, 14, 3, 9, 16, 27, 33, 31, 22, 13, 6, 7]

min = 0
max = len(a) - 1


# 分解递归
def divide(seq, min, max):
    # 递归终止条件
    if max <= min:
        return

    mid = int((min + max) / 2)

    # 递归调用
    divide(seq, min, mid)
    divide(seq, mid + 1, max)

    merge(seq, min, mid, max)


def merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m

    # 创建临时数组
    L = list()
    R = list()

    # 拷贝数据到临时数组 arrays L[] 和 R[]
    for i in range(0, n1):
        L.append(arr[l + i])

    for j in range(0, n2):
        R.append(arr[m + 1 + j])

    # 归并临时数组到 arr[l..r]
    i = 0  # 初始化第一个子数组的索引
    j = 0  # 初始化第二个子数组的索引
    k = l  # 初始归并子数组的索引

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # 拷贝 L[] 的保留元素
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # 拷贝 R[] 的保留元素
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


if __name__ == '__main__':
    divide(a, min, max)
    print(a)


'''
时间复杂度: O(nlogn)
归递排序在排序过程中需要开辟中转空间，所以空间复杂度是大于希尔排序的
'''