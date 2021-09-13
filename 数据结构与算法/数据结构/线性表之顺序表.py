'''
顺序表: 用一组连续的存储单元，依次存储线性表中的各个元素。使得线性表中在逻辑结构上相邻的两个元素存储在相邻的物理存储单元中，
       即通过数据元素物理存储的相邻关系来反映元素之间逻辑上的相邻关系。

顺序表API设计：
    类名：
        - SequenceList
    构造方法：
        - __init__(self): 创建SequenceList对象
    成员方法：
        - clear(): 置空线性表
        - isEmpty(): 判断线性表是否为空，是返回true，否返回false
        - length(): 获取线性表中的元素个数
        - get(i: int): 读取线性表中第i个元素的值，如果没有第i个元素则返回-1
        - insert(i: int, value): 在线性表的下标i处插入一个值为value的元素
        - add(value): 在线性表的末尾添加一个元素
        - remove(i: int): 移除线性表下标i处的元素并返回
        - indexOf(value): 返回线性表中，首次出现value元素的下标，若不存在返回-1
    成员变量：
        - eles: 存储元素的列表
        - N: 当前线性表的长度
'''


class SequenceList:

    def __init__(self):
        self.N = 0
        self.eles = []

        # 迭代计数器
        self.count = 0

    def __str__(self) -> str:
        return self.eles.__str__()

    def clear(self):
        self.N = 0
        self.eles = []

    @property
    def isEmpty(self):
        return self.N == 0

    @property
    def length(self):
        return self.N

    def get(self, i: int):
        if not isinstance(i, int):
            raise TypeError

        return -1 if i >= self.N or i < 0 else self.eles[i]

    def insert(self, i: int, value):
        if not isinstance(i, int):
            raise TypeError

        if i < 0 or i >= self.N:
            raise IndexError

        self.eles += [None]
        for j in range(self.N, i, -1):
            self.eles[j] = self.eles[j - 1]

        self.eles[i] = value

        self.N += 1

    def add(self, value):
        try:
            self.eles[self.N]
        except IndexError:
            self.eles += [None]
        finally:
            self.eles[self.N] = value

        self.N += 1

    def remove(self, i: int):
        if not isinstance(i, int):
            raise TypeError
        if i < 0 or i >= self.N:
            raise IndexError

        value = self.eles[i]

        if i == self.N - 1:
            pass
        else:
            for j in range(i, self.N):
                self.eles[j] = self.eles[j + 1]

        self.N -= 1

        temp = [None] * self.N
        for i in range(self.N):
            temp[i] = self.eles[i]

        self.eles = temp

        return value

    def indexOf(self, value):
        for i in range(self.N):
            if self.eles[i] == value:
                return i
        return -1

    # 实现顺序表可迭代
    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count <= self.N:
            return self.eles[self.count - 1]
        self.count = 0
        raise StopIteration


if __name__ == '__main__':
    seq = SequenceList()
    seq.add("姚明")
    seq.add("老张")
    seq.add("朱晓明")
    seq.add("好吧睡觉")
    seq.add(1)
    seq.add(2)

    # print(seq)
    # print(seq.get(1))
    # print(seq.isEmpty)
    # print(seq.items)
    #
    # seq.remove(3)
    # print(seq.get(3))
    # print(seq.items)
    #
    seq.insert(1, "悍匪")
    # print(seq.items)
    # print(seq.indexOf("姚明"))
    # print(seq.length)

    seq.clear()
    seq.add("调任新职")

    for i in seq:
        print(i)
