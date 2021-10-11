'''
由图的概念可知：
    路径 是由边顺序连接的一系列的顶点组成

路径查找：
    判断从s顶点到v顶点是否存在一条路径，如果存在，就找出这条路径

API设计：
    类名：DepthFirstPaths
    构造方法：
        - __init__(G, s) 构造DepthFirstPaths对象，使用深度优先算法，找出图G中以s为起点的所有路径
    成员方法：
        - dfs(G, v) 使用深度优先算法找出G图中v顶点可搜索到的顶点，并记录到该顶点路径上的最后一个顶点
        - has_path(v) 判断v顶点与s顶点是否存在路径
        - path(v) 返回一个栈，找出从s顶点到v顶点的路径
    成员变量：
        - marks 一个列表，保存bool。索引代表顶点，值表示当前顶点是否已经被搜索，已经被搜索的话，表示和顶点s相通
        - s 起点
        - edge_to 一个列表，索引代表顶点，值代表从起点s到该顶点路径上的最后一个顶点
'''
from 数据结构与算法.数据结构.图.无向图 import Graph
from 数据结构与算法.数据结构.线性表.栈.栈 import Stack


class DepthFirstPaths:
    def __init__(self, G, s):
        self.s = s
        self.marks = [False] * G.V
        self.edge_to = [None] * G.V

        self.dfs(G, s)

    def dfs(self, G, v):
        # 把当前顶点标记为已搜索
        self.marks[v] = True

        # 找到当前结点的临界点进行遍历
        for i in G.get_adj(v):
            if not self.marks[i]:
                # 记录到达结点i的路径上的最后一个顶点，就是当前的v顶点
                self.edge_to[i] = v
                # 递归调用深度算法
                self.dfs(G, i)

    def has_path(self, v):
        # 判断是否存在相通的路径，就是看顶点v是否被搜索过，被搜索过就代表一定由路径
        return self.marks[v]

    def path(self, v):
        # 先判断顶点v是否可达，如果可达则一定有路径，如果不可达则直接返回
        if not self.has_path(v):
            return

        # 要找出从顶点s到顶点v的路径，那么就从顶点v开始找循环往后找路径上的顶点即可
        # 将路径上的顶点存入栈中
        s = Stack()
        # 先把自己放进去
        s.push(v)

        # 只要还没找到起始顶点就一直找
        while v != self.s:
            # 把顶点v路径上最后一个顶点放入栈中
            s.push(self.edge_to[v])

            # 迭代v
            v = self.edge_to[v]

        return s


if __name__ == '__main__':
    G = Graph(12)
    G.add_edge(0, 1)
    G.add_edge(0, 6)
    G.add_edge(0, 2)
    G.add_edge(0, 5)
    G.add_edge(5, 8)
    G.add_edge(10, 11)
    G.add_edge(5, 7)
    G.add_edge(7, 8)
    G.add_edge(8, 10)

    dfp = DepthFirstPaths(G, 0)
    s = dfp.path(11)
    while not s.is_empty:
        print(s.pop())
