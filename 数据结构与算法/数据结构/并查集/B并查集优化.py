"""
并查集时间复杂度分析:
    根据并查集的API设计，如果我们想将列表中所有的元素都合并到一个组，那么我们至少需要调用N-1次union方法；
    同时，我们在union方法内部遍历了列表。
    若以想要完成所有元素合并的时间复杂度是O(n^2)，这种情况下处理大量元素时，将带来巨大的开销。

优化思路：
    对eleToGroup列表进行重新设定：
        1、我们仍然让列表的索引作为结点的元素
        2、但是，列表索引对应保存的值，不再是当前结点的分组标识，而是该结点的父结点
        3、只有当结点没有父结点时，列表索引处的值才是分组标识

具体实现：
    重写并查集的find、union、connected方法

优化结果：
    按照如下代码优化后，union方法的时间复杂度变成了O(1)
    但是我们同时修改并掉了find方法，而find方法的时间复杂度是O(n)，所以整体合并的时间复杂度，仍然是O(n^2)
    所以我们继续优化，请见 并查集路径压缩
"""

from 数据结构与算法.数据结构.并查集.A并查集 import UF


class UF_Tree(UF):
    def find(self, p):
        while True:
            # 如果当前接的索引和保存的值相等，那么说明就找到了分组标识
            if p == self.eleToGroup[p]:
                return p

            # 如果不相等，就说明当前结点保存的是父元素。那么久用父元素继续向上查找分组标识
            p = self.eleToGroup[p]

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        # 找到p和q的分组标识
        p_g = self.find(p)
        q_g = self.find(q)

        # 判断二者是否相同，相同则不需要继续合并了
        if p_g == q_g:
            return

        # 如果不相同，则把p的分组标识编成q的分组标识
        # 提醒：分组标识所在的结点，索引和保存的分组标识是相等的
        self.eleToGroup[p_g] = q_g

        # 分组数量减1
        self.N -= 1


if __name__ == '__main__':
    uf = UF_Tree(20)
    print(uf.count)

    a = uf.connected(1, 2)
    print(a)
    uf.union(1, 2)
    print(uf.count)
    uf.union(1, 19)
    print(uf.count)

    print(uf.connected(1, 19))
