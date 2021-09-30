from functools import reduce


def func(a, b):
    return a + b


# reduce(function, sequence, initial=_initial_missing)
# initial 表示 初次回调时 的第一个入参。如果没有，就在sequence中取第一个。
# reduce 累积函数，要求回调函数入参是两个，并把执行逻辑后的返回值作为，下一次调用的第一个入参
# 直到 可迭代对象 被迭代完。 最后返回 累积的结果。
cc = reduce(func, range(10))
dd = reduce(func, range(10), 5)

print(cc)  # 45
print(dd)  # 50
