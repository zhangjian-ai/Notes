'''
API设计：
    类名：Graph
    构造方法：
        - __init__(capacity) 创建一个包含 capacity 个顶点，但不包含边的图
    成员方法：
        - vertex_count() 获取图中顶点的数量
        - edge_count() 获取图中边的数量
        - add_edge(v, w) 像图中添加一条连接顶点v和顶点w的边
        - get_adj(v) 获取和顶点v相邻的所有顶点
    成员变量：
        - V 记录顶点数量
        - E 记录边的数量
        - adj 邻接表
'''
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class Graph:
    def __init__(self, capacity):
        self.V = capacity
        self.E = 0
        self.adj = [None] * capacity

        # 初始化每个顶点的邻接表队列
        for i in range(len(self.adj)):
            self.adj[i] = Queue()

    def vertex_count(self):
        return self.V

    def edge_count(self):
        return self.E

    def add_edge(self, v, w):
        if v >= self.V or w >= self.V:
            raise IndexError

        # 无向图中，边 是没有方向的，所以要同时给两个顶点的邻接队列都加上对应的顶点
        self.adj[v].enqueue(w)
        self.adj[w].enqueue(v)

        # 边的数量加一
        self.E += 1

    def get_adj(self, v):
        # 获取顶点v的邻接顶点，返回该顶点的队列即可
        return self.adj[v]


if __name__ == '__main__':
    g = Graph(10)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(3, 4)

    print(g.edge_count())
    print(g.vertex_count())

    for i in g.get_adj(4):
        print(i)
