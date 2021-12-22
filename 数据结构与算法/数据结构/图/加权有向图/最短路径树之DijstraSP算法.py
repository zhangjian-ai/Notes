"""
最短路径：
    定义：
        在一幅加权有向图中，从顶点s到顶点v的最短路径，是指从顶点s到顶点v的路径中权重最小的那条路径。
    性质：
        1、路径具有方向性；
        2、权重不一定等价于距离。权重可以是距离、时间、花费等各种成本指标。
        3、只考虑连通图。为了简化问题，非连通图暂不考虑。
        4、最短路径不一定是唯一的。从一个顶点到另一个顶点的权重最小路径可能会有很多条，这里只需找出其中一条即可。

最短路径树：
    给定一幅加权有向图和一个顶点s，以顶点s为起点的最短路径树是该图的一幅子图，它包含顶点s以及从s可达的所有顶点。
    这棵树的根结点为s，树的每条路径都是有向图中的一条最短路径。

松弛技术：
    边的松弛：
        松弛边v->w意味着检查从s到w的最短路径是否先从s到v，然后再从v到w？
        如果是，则v->w这条边需要加入到最短路径中，更新edge_to和dist_to中的内容：edge_to[w] = v->w边对象；dist_to[w] = dist_to[v] + v->w边的权重
        如果不是，则忽略这条边

    顶点的松弛：
        顶点的松弛是基于边的松弛完成的，只需要把该顶点指出的所有边松弛完成，那么该顶点就松弛完毕。
        例如：要松弛顶点v，只需要遍历v的邻接表，把每一条边都松弛，那么顶点v就松弛了。

API设计：
    类名：DijkstraSP(迪杰斯特拉最短路径 Dijkstra Short Path)
    构造方法：
        - __init__(G, s) 根据加权有向图G和顶点s，创建一个以顶点s为起点的最短路径树的计算对象
    成员方法：
        - relax(G, v) 松弛图G中的顶点v
        - has_path(v) 判断从顶点s到顶点v是否可达
        - get_paths(v) 查询从起点s到顶点v的最短路径的所有边
    成员变量：
        - marks 一个列表。索引代表顶点，保存布尔值。表示该顶点是否已经被松弛
        - edge_to 一个列表。索引代表顶点，值表示从顶点s到当前顶点的最短路径上的最后一条边
        - dist_to 一个列表。索引代表顶点，值表示从顶点s到当前顶点的最短路径的总权重
        - queue 一个最小优先队列。记录树中顶点与非树中顶点之间的有效横切边
"""

import sys

from 数据结构与算法.数据结构.图.加权有向图.加权有向图 import EdgeWeightedDiGraph, DirectedEdge
from 数据结构与算法.数据结构.线性表.队列.优先队列之最小优先队列 import MinPriorityQueue

from 数据结构与算法.数据结构.线性表.队列.A队列 import Queue


class DijkstraSP:
    def __init__(self, G, s):
        self.marks = [False] * G.vertex_count
        self.edge_to = [None] * G.vertex_count
        self.dist_to = [None] * G.vertex_count
        self.queue = MinPriorityQueue(G.edge_count)

        # 初始化dist_to列表，让其默认保存最大浮点数
        for i in range(len(self.dist_to)):
            self.dist_to[i] = sys.float_info.max

        # 初始状态下，默认最短路径树中只有顶点s，且自己到自己的边的权重值为0.0
        self.dist_to[s] = 0.0
        self.queue.insert(s)

        # 遍历最小索引优先队列的中的顶点，对其进行松弛
        while not self.queue.is_empty:
            v = self.queue.del_min()
            self.relax(G, v)

    def relax(self, G, v):
        """松弛顶点v"""
        # 遍历顶点v指出的所有边
        for e in G.adj[v]:
            # 获取该边的目标顶点
            w = e.target
            # 检查从s到w的最短路径是否先从s到v，然后再从v到w?
            if self.dist_to[v] + e.get_weight < self.dist_to[w]:
                # 如果小于表示要先到v再到w，那么需要更新数据
                self.dist_to[w] = self.dist_to[v] + e.get_weight
                self.edge_to[w] = e

                # 将目标顶点w添加到最小索引优先队列，以完成对其松弛
                if not self.marks[w] and not self.queue.contains(w):
                    self.queue.insert(w)

        # 遍历完当前顶点指出的所有边，则修改当前顶点已经被松弛
        self.marks[v] = True

    def has_path(self, v):
        """判断从顶点s到顶点v是否可达"""
        # 只需要判断dist_to对应索引处的值是否是最大浮点数，如果不是，则说明在松弛的过程中找到了到该边的最短路径
        if self.dist_to[v] == sys.float_info.max:
            return False
        return True

    def get_paths(self, v):
        """查询从起点s到顶点v的最短路径的所有边，返回一个队列"""
        # 先判断顶点是否可达，不可达则直接返回
        if not self.has_path(v):
            return

        # 创建一个对
        all_edges = Queue()

        # 如果可达，则从当前顶点往回找。如果edge_to中，当前顶点索引处未保存边，则说明找到了起始顶点则结束循环
        while self.edge_to[v]:
            # 获取从顶点s到当前顶点的最短路径中的最后一条边
            e = self.edge_to[v]
            # 保存边到队列
            all_edges.enqueue(e)
            # 更新当前结点
            v = e.origin

        return all_edges


if __name__ == '__main__':
    g = EdgeWeightedDiGraph(8)
    g.add_edge(DirectedEdge(4, 5, 0.35))
    g.add_edge(DirectedEdge(5, 4, 0.35))
    g.add_edge(DirectedEdge(4, 7, 0.37))
    g.add_edge(DirectedEdge(5, 7, 0.28))
    g.add_edge(DirectedEdge(7, 5, 0.28))
    g.add_edge(DirectedEdge(5, 1, 0.32))
    g.add_edge(DirectedEdge(0, 4, 0.38))
    g.add_edge(DirectedEdge(0, 2, 0.26))
    g.add_edge(DirectedEdge(7, 3, 0.39))
    g.add_edge(DirectedEdge(1, 3, 0.29))
    g.add_edge(DirectedEdge(2, 7, 0.34))
    g.add_edge(DirectedEdge(6, 2, 0.40))
    g.add_edge(DirectedEdge(3, 6, 0.52))
    g.add_edge(DirectedEdge(6, 0, 0.58))
    g.add_edge(DirectedEdge(6, 4, 0.94))

    di = DijkstraSP(g, 0)
    for e in di.get_paths(6):
        print(e.v, e.w, '=>', e.weight)
