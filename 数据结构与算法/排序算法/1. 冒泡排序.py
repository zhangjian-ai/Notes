"""
冒泡排序(从小到大):
    - 依次比较相邻的两个元素，每一次外层的循环，都把最大的值放到序列的最后
"""

a = [6, 4, 2, 1, 7, 5, 11, 22, 17, 23, 14, 3, 9]
num = len(a)

for i in range(num - 1):
    for k in range(num - 1 - i):
        if a[k] > a[k + 1]:
            a[k], a[k + 1] = a[k + 1], a[k]

print(a)

'''
时间复杂度分析:
    - 交换次数: (n-1) + (n-2) + (n-3) .... + 1 = (n-1)*((n-1) + 1)/2 = (n^2 - n)/2
    - 时间复杂度: O(n^2)
'''


