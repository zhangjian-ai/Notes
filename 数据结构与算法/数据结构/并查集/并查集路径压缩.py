'''
路径分析：
    在并查集优化中，我们在合并时，总是直接把当前分组直接编成要合并的分组。
    这样的结果就是在合并过程中，很容易就出现线性树，致使树的深度很深，这样就增加了查询的次数

路径压缩：
    就是尽量降低树的深度，以减少查询次数

实现思路：
    引入另一个列表，来记录每个分组的元素个数。此时列表的索引表示分组标识，而结点记录的值标识分组中元素的个数
'''

from 并查集优化 import UF_Tree


class UF_Tree_Weighted(UF_Tree):
    def __init__(self, N):
        super().__init__(N)

        # 引入一个记录分组中元素个数的列表
        self.sz = [None] * self.N
        # 初始状态下，每个分组中的元素个数为 1
        for i in range(self.N):
            self.sz[i] = 1

    def union(self, p, q):
        '''优化合并方法'''

        # 找到p和q的分组标识
        p_g = self.find(p)
        q_g = self.find(q)

        # 判断而这是否相同，相同则不需要继续合并了
        if p_g == q_g:
            return

        # 根据分组中的元素个数来决定怎么合并
        if self.sz[p_g] < self.sz[q_g]:
            # p_g中的元素少，就把p_g的分组标识编成q_g
            self.eleToGroup[p_g] = q_g
            # 修改分组的元素个数
            self.sz[q_g] += self.sz[p_g]
        else:
            self.eleToGroup[q_g] = p_g
            self.sz[p_g] += self.sz[q_g]

        # 分组数量减1
        self.N -= 1


if __name__ == '__main__':
    uf = UF_Tree_Weighted(20)
    print(uf.count)

    a = uf.connected(1, 2)
    print(a)
    uf.union(1, 2)
    print(uf.count)
    uf.union(1, 19)
    print(uf.count)

    print(uf.connected(1, 19))
