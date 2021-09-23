'''
中缀表达式：
    - 中缀表达式就是我们常用的表达式。例如：3+4-(2*3)，特点就是二元运算符总是置于两个操作数之间。

逆波兰表达式(后缀表达式)：
    运算符总是放在跟它相关的操作数之后。例如：abc-+ => a+(b-c)，abc+*d+ => a*(b+c)+d

需求，用栈实现对逆波兰表达式求值
'''

from 栈 import Stack


def calculate(expression):
    s = Stack()

    # 遍历表达式
    for item in expression:
        if item in ['+', '-', '*', '/']:
            # 如果是运算符，那么就从栈中弹出最后入栈的两个元素来进行运算
            # 运算时，根据栈的特性，需要把最后入栈的元素放在运算符后面
            n1 = int(s.pop())
            n2 = int(s.pop())

            # 开始运算
            if item == '+':
                res = n2 + n1
            if item == '-':
                res = n2 - n1
            if item == '*':
                res = n2 * n1
            if item == '/':
                res = n2 / n1

            # 把计算结果放回到栈中
            s.push(res)
        else:
            # 如果不是运算符，就将其入栈即可
            s.push(item)

    # 运算完之后，栈里面就只剩下最后被计算出来的值
    return s.pop()


if __name__ == '__main__':
    exp = '345+*72+-'
    print(calculate(exp))
