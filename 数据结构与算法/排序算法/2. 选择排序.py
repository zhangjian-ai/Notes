"""
选择排序:
    - 默认待排序序列首位是最小值，下标为 minimum
    - 通过一次内层循环，依次拿首位根后面的值做比较，把真正的最小值放到首位去
"""

a = [6, 4, 2, 1, 7, 5, 11, 22, 17, 23, 14, 3, 9]

for i in range(len(a) - 1):
    minimum = i
    for k in range(i + 1, len(a)):
        if a[minimum] > a[k]:
            minimum = k
    if minimum != i:
        a[minimum], a[i] = a[i], a[minimum]

print(a)

'''
时间复杂度分析:
    - 比较次数: (n-1) + (n-2) + (n-3) .... + 1 = (n-1)*((n-1) + 1)/2 = (n^2 - n)/2
    - 交换次数: n-1
    _ 时间复杂度: O(n^2)
'''