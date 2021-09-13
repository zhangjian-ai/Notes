import math
from overloads.overloads import overloads


@overloads
def area(l: int, w: int):
    """计算长方形面积"""
    return l * w


@overloads
def area(r: int):
    """计算圆面积"""
    return math.pi * r * 2


@overloads
def area():
    """计算圆面积"""
    return 36


if __name__ == '__main__':
    # 根据不同的参数个数，执行不同的函数
    print(area(3, 4))
    print(area(5))
    print(area())
    # print(area(5, "aa"))
