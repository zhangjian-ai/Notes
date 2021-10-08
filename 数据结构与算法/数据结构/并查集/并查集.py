'''
并查集是一种输形结构，并查集可以高效的进行如下操作；
    - 查询元素p 和元素 q是否属于同一组。
    - 合并元素p 和元素 q所在的组。

并查集也是一种属性结构，但这棵树和二叉树、红黑树、B树都不一样，这种树的要求比较简单：
    1、每个元素都唯一的对应一个结点；
    2、每一组数据中的多个元素都在同一棵树中；
    3、一个组中的数据对应的树和另一个组中的数据对应的树之间没有任何联系；
    4、元素在树中并没有子父级关系的硬性要求。

API结构设计：
    类名：UF
    构造方法：
        - __init__(self, N) 初始化并查集，以整数标识(0, N-1)个结点
    成员方法：
        - count() 获取当前并查集中数据有多少个分组
        - connected(p, q) 判断并查集中的元素p 、元素q 是否在同一个组中，返回 bool
        - find(p) 元素p 所在的分组标识
        - union(p, q) 把元素p 和 元素q所在的分组合并
    成员变量：
        - eleToGroup 记录结点元素和该元素所在的分组标识，是一个列表。列表的索引表示元素、而每个索引处的值标识分组标识
        - N 记录并查集中数据的分组个数
'''


class UF:
    def __init__(self, N):
        # 初始状态下，默认就是每个索引一个分组，所以初始状态的分组数就是N
        self.N = N
        # 创建初始化列表
        self.eleToGroup = [None] * self.N
        # 让列表每个索引称为其对应索引的值
        for i in range(self.N):
            self.eleToGroup[i] = i

    @property
    def count(self):
        return self.N

    def connected(self, p, q):
        return self.eleToGroup[p] == self.eleToGroup[q]

    def find(self, p):
        return self.eleToGroup[p]

    def union(self, p, q):
        # 判断当前两个元素是否在同一组中，如果在则可以直接结束
        if self.connected(p, q):
            return

        # 分别找出p, q 的分组标识
        p_g = self.eleToGroup[p]
        q_g = self.eleToGroup[q]

        # 循环遍历，把所有p_g分组下的元素分组都编成q_g
        for i in range(self.N):
            if self.eleToGroup[i] == p_g:
                self.eleToGroup[i] = q_g

        # 把分组数量减 1
        self.N -= 1


if __name__ == '__main__':
    uf = UF(20)
    print(uf.count)

    a = uf.connected(1, 2)
    print(a)
    uf.union(1, 2)
    print(uf.count)
    uf.union(1, 19)
    print(uf.count)

    print(uf.connected(1, 19))
