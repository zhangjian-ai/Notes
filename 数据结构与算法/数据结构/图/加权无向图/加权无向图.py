"""
加权无向图：
    是一种为每条边关联一个权重值或是成本的无向图模型，在该模型中，用一个对象来描述一条边。

加权边API设计：
    类名：Edge
    构造方法：
        - __init__(v, w, weight) 通过顶点v、顶点w 和权重值weight 构造一个边对象
    成员方法：
        - get_weight() 获取边的权重值
        - either() 获取边上的一个点
        - other(v) 获取边上不是顶点v的另一个顶点
        - __lt__(edge: Edge) 判断当前边的权重是否比edge的权重小，如果是则返回 true；否则返回 false。__lt__是魔法方法，'<' 运算时自动调用
    成员变量：
        - v 顶点一
        - w 顶点二
        - weight 当前边的权重

加权无向图API设计：
    类名：EdgeWeightedGraph
    构造方法：
        - __init__(capacity) 创建一个包含capacity个顶点的加权无向图
    成员方法：
        - vertex_count() 获取图中顶点的数量
        - edge_count() 获取图中边的数量
        - add_edge(edge) 往图中添加一条边
        - edges() 获取加权无向图的所有边，返回一个队列
    成员变量：
        - v 记录顶点的数量
        - e 记录边的数量
        - adj 一个列表，索引表示顶点，值是一个队列，记录与该顶点相连的边
"""

from 数据结构与算法.数据结构.线性表.队列.A队列 import Queue


class Edge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    @property
    def get_weight(self):
        return self.weight

    @property
    def either(self):
        return self.v

    def other(self, v):
        if self.v != v:
            return self.v
        else:
            return self.w

    # 实现魔法方法__lt__，以便后续在做比较运算时使用
    def __lt__(self, other):
        if self.weight < other.weight:
            return True
        else:
            return False


class EdgeWeightedGraph:
    def __init__(self, capacity):
        self.v = capacity
        self.e = 0
        self.adj = [None] * self.v

        # 初始化每个顶点的邻接表
        for i in range(self.v):
            self.adj[i] = Queue()

    @property
    def vertex_count(self):
        return self.v

    @property
    def edge_count(self):
        return self.e

    def add_edge(self, edge):
        # 获取edge的两个顶点
        v = edge.either
        w = edge.other(v)

        # 分别向两个顶点邻接表中存入一条边
        self.adj[v].enqueue(edge)
        self.adj[w].enqueue(edge)

        # 边数量加一
        self.e += 1

    def edges(self):
        edge_queue = Queue()

        # 获取加权无向图中的所有的边，需要遍历每个顶点的邻接队列
        # 但由于是无向图，同一个边都会被保存两次，因此需要去重
        # 解决思路：每一条边都有两个顶点，我们都默认保存较小顶点的邻接队列中的边
        for v in range(self.v):
            for edge in self.adj[v]:
                if v == min(edge.v, edge.w):
                    edge_queue.enqueue(edge)
        return edge_queue
