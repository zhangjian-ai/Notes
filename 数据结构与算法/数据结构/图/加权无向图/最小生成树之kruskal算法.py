'''
kruskal算法：
    是计算一幅加权无向图的最小生成树的另一种算法。
    主要思想是按边的权重（从小到大处理他们），根据条件（加入的边不会与最小生成树中已有的边构成环）将边加入到最小生成树中，直到树中含有v-1条边为止。

API设计：
    类名：KruskalMST
    构造方法：
        - __init__(G) 根据加权无向图，创建最小生成树的计算对象
    成员方法：
        - edges() 返回一个队列。保存最小生成树所有的边
    成员变量：
        - mst 一个队列，保存最小生成树所有的边
        - uf 一个并查集。索引代表顶点，值与表示不同的树
        - mfq 一个最小优先队列。存储图中所有的边，按权重进行排序
'''
from 数据结构与算法.数据结构.图.加权无向图.加权无向图 import EdgeWeightedGraph, Edge
from 数据结构与算法.数据结构.并查集.并查集路径压缩 import UF_Tree_Weighted
from 数据结构与算法.数据结构.线性表.队列.优先队列之最小优先队列 import MinPriorityQueue
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class KruskalMST:
    def __init__(self, G):
        self.mst = Queue()
        self.uf = UF_Tree_Weighted(G.vertex_count)
        self.mfq = MinPriorityQueue(G.edge_count)

        # 将图G中的边都放入到最小优先队列中
        for e in G.edges():
            self.mfq.insert(e)

        # 遍历最小优先队列，拿到最小权重的边进行处理
        while not self.mfq.is_empty and self.mst.size < G.vertex_count - 1:
            # 找到权重最小的边
            e = self.mfq.del_min()
            # 找到两个顶点
            v = e.either
            w = e.other(v)
            # 判断两个顶点是否在同一棵树中，如果在则不做处理
            # 如果不在，则让这两个顶点所在的两棵树合并成一棵树
            if self.uf.connected(v, w):
                continue

            self.uf.union(v, w)
            # 合并成一棵树之后，将边e加入到最小生成树的队列中
            self.mst.enqueue(e)

    @property
    def edges(self):
        return self.mst


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

    p = KruskalMST(g)

    for e in p.edges:
        print(e.v, e.w, '=>', e.weight)
