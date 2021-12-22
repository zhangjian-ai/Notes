"""
有向图：
    有向图是一幅具有方向的图，是由一组顶点和一组有方向的边组成的，每条有方向的边都连着一对有序的顶点。
出度：
    由某个顶点指出的边的个数称为该顶点的出度。
入库：
    指向某个顶点的边的个数称为该顶点的入度。
有向路径：
    有一系列的顶点组成，对于其中的每个顶点都存在一条有向边，从它指向序列中的下一个顶点。
有向环：
    一条至少包含一条边，且起点和终点是同一个定点的有向路径。

有向图中，两个顶点的四种关系：
    1、没有边相连；
    2、存在从A到B的一条边
    3、存在从B到A的一条边
    4、即存在从A到B的边，又存在从B到A的边

API设计：
    类名：Digraph
    构造方法：
        - __init__(capacity) 创建一个包含 capacity 个顶点，但不包含边的有向图
    成员方法：
        - vertex_count() 获取图中顶点的数量
        - edge_count() 获取图中边的数量
        - add_edge(v, w) 像图中添加一条由顶点v指向顶点w的边
        - get_adj(v) 获取和顶点v相邻的所有顶点
        - reverse() 该图的反向图
    成员变量：
        - V 记录顶点数量
        - E 记录边的数量
        - adj 邻接表。索引表示顶点，列表的值是一个队列，记录该顶点指向的所有邻接点。
"""

from 数据结构与算法.数据结构.线性表.队列.A队列 import Queue


class Digraph:
    def __init__(self, capacity):
        self.V = capacity
        self.E = 0
        self.adj = [None] * self.V

        # 初始状态时，每个顶点的邻接表都是一个空队列
        for i in range(self.V):
            self.adj[i] = Queue()

    @property
    def vertex_count(self):
        return self.V

    @property
    def edge_count(self):
        return self.E

    def add_edge(self, v, w):
        # 有向图中，只需将w顶点，放到v顶点的邻接队列中即可。表示从v顶点指向w顶点
        self.adj[v].enqueue(w)
        # 边的数量加一
        self.E += 1

    def get_adj(self, v):
        return self.adj[v]

    def reverse(self):
        # 创建一个新的图
        digraph = Digraph(self.V)

        # 遍历当前有向图，把每个顶点的反向边加到图中
        for v in range(self.V):
            # 遍历队列，把当前顶点加到邻接点的邻接队列中
            for w in self.adj[v]:
                digraph.adj[w].enqueue(v)
                # 边的数量加一
                digraph.E += 1

        # 返回反向图
        return digraph


if __name__ == '__main__':
    g = Digraph(10)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(3, 4)

    print(g.edge_count)
    print(g.vertex_count)

    for i in g.get_adj(0):
        print(i)

    print("---------")
    g2 = g.reverse()

    print(g2.edge_count)
    print(g2.vertex_count)

    for i in g2.get_adj(4):
        print(i)
