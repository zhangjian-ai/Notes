'''
Prim算法：
    1、把图中一个顶点看作一个集合A，剩余的所有顶点看作一个集合B；
    2、找到两个集合之间的权重最小的边，以及该边连接的另一个顶点；
    3、把权重最小边和它连接的顶点加入到集合A，B中剩余顶点组成新的集合B；
    4、重复2～3步骤，直到找出图的最小生成树

API设计：
    类名：PrimMST
    构造方法：
        - __init__(G) 根据加权无向图G，创建最小生成树计算对象
    成员方法：
        - visit(G, v) 将顶点v添加到最小生成树中，并更新数据
        - edges() 获取最小生成树的所有边
    成员变量：
        - edge_to 一个列表。索引代表顶点，值表示当前顶点和最小生成树之间的最短边
        - dist_to 一个列表。索引代表顶点，值表示当前顶点和最小生成树之间的最短边的权重
        - marks 一个列表。索引代表顶点，值表示当前顶点是否在最小生成树中
        - queue 一个最小索引优先队列。存放树中顶点与非树中顶点之间的有效横切边的权重
'''
import sys

from 数据结构与算法.数据结构.图.加权无向图 import EdgeWeightedGraph, Edge
from 数据结构与算法.数据结构.线性表.队列.优先队列之最小索引优先队列 import IndexMinPriorityQueue
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class PrimMST:
    def __init__(self, G):
        self.edge_to = [None] * G.vertex_count
        self.dist_to = [None] * G.vertex_count
        self.marks = [False] * G.vertex_count
        self.queue = IndexMinPriorityQueue(G.vertex_count)

        # 由于需要找出权重最小的边，先默认让dist_to中的权重保存为最大值
        for i in range(G.vertex_count):
            self.dist_to[i] = sys.maxsize

        # 默认让dist_to中0索引处的值为0.0，因为从顶点0开始遍历（默认把索引0作为初始树），所以自己到自己的距离就是0
        self.dist_to[0] = 0.0
        # 把索引0添加到队列，作为初始遍历的起点
        self.queue.insert(0, 0.0)

        # 遍历索引最小优先队列
        while not self.queue.is_empty:
            # 拿到索引最小的顶点，将其添加到树中
            self.visit(G, self.queue.del_min())

    def visit(self, G, v):
        # 把当前顶点添加到树中
        self.marks[v] = True
        # 遍历当前顶点v与非树中顶点连接的所有横切边
        for edge in G.adj[v]:
            # 找到横切边的另一个顶点
            w = edge.other(v)

            # 判断顶点w是否已经在树中，如果在就不进行任何操作
            if self.marks[w]:
                continue

            # 如果不在则更新数据，前提是当前边edge的权重要小于dist_to中对应顶点保存的最小边的权重值
            if edge.get_weight < self.dist_to[w]:
                self.edge_to[w] = edge
                self.dist_to[w] = edge.get_weight

                # 将当前边添加到索引最小优先队列
                if self.queue.contains(w):
                    self.queue.change_item(w, edge.get_weight)
                else:
                    self.queue.insert(w, edge.get_weight)

    @property
    def edges(self):
        """获取最小生成树的所有边，返回一个队列"""
        all_edges = Queue()
        # 遍历edge_to列表，其中所有的边就是最小生成树的边
        for edge in self.edge_to:
            if edge:
                all_edges.enqueue(edge)

        return all_edges


if __name__ == '__main__':
    g = EdgeWeightedGraph(8)
    g.add_edge(Edge(4, 5, 0.35))
    g.add_edge(Edge(4, 7, 0.37))
    g.add_edge(Edge(5, 7, 0.28))
    g.add_edge(Edge(0, 7, 0.16))
    g.add_edge(Edge(1, 5, 0.32))
    g.add_edge(Edge(0, 4, 0.38))
    g.add_edge(Edge(2, 3, 0.17))
    g.add_edge(Edge(1, 7, 0.19))
    g.add_edge(Edge(0, 2, 0.26))
    g.add_edge(Edge(1, 2, 0.36))
    g.add_edge(Edge(1, 3, 0.29))
    g.add_edge(Edge(2, 7, 0.34))
    g.add_edge(Edge(6, 2, 0.40))
    g.add_edge(Edge(3, 6, 0.52))
    g.add_edge(Edge(6, 0, 0.58))
    g.add_edge(Edge(6, 4, 0.93))

    p = PrimMST(g)

    for e in p.edges:
        print(e.v, e.w, '=>', e.weight)
