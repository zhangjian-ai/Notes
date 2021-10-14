'''
加权有向图：
    是一种为每条边关联一个权重值或是成本的有向图模型，在该模型中，用一个对象来描述一条边。

加权边API设计：
    类名：DirectedEdge
    构造方法：
        - __init__(v, w, weight) 通过顶点v、顶点w 和权重值weight 构造一个边对象
    成员方法：
        - get_weight() 获取边的权重值
        - origin() 获取有向边的起点
        - target() 获取有向边的终点
    成员变量：
        - v 起点
        - w 终点
        - weight 当前边的权重

加权无向图API设计：
    类名：EdgeWeightedDiGraph
    构造方法：
        - __init__(capacity) 创建一个包含capacity个顶点的加权有向图
    成员方法：
        - vertex_count() 获取图中顶点的数量
        - edge_count() 获取图中边的数量
        - add_edge(edge) 往图中添加一条边
        - edges() 获取加权有向图的所有边，返回一个队列
    成员变量：
        - v 记录顶点的数量
        - e 记录边的数量
        - adj 一个列表，索引表示顶点，值是一个队列，记录由该顶点指出的所有的边
'''
from 数据结构与算法.数据结构.线性表.队列.队列 import Queue


class DirectedEdge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    @property
    def get_weight(self):
        return self.weight

    @property
    def origin(self):
        return self.v

    @property
    def target(self):
        return self.w

    # 实现魔法方法__lt__，以便后续在做比较运算时使用
    def __lt__(self, other):
        if self.weight < other.weight:
            return True
        else:
            return False


class EdgeWeightedDiGraph:
    def __init__(self, capacity):
        self.v = capacity
        self.e = 0
        self.adj = [None] * self.v

        # 初始化adj
        for i in range(self.v):
            self.adj[i] = Queue()

    @property
    def vertex_count(self):
        return self.v

    @property
    def edge_count(self):
        return self.e

    def add_edge(self, e):
        """向图中添加一条边"""
        # 找到边的起点
        v = e.origin
        # 向adj中添加边
        self.adj[v].enqueue(e)

        # 边数量加一
        self.e += 1

    def edges(self):
        """返回一个队列，包含图中所有的边"""
        q = Queue()

        # 遍历顶点，将其指出的边放到队列中
        for i in range(self.v):
            for e in self.adj[i]:
                q.enqueue(e)

        return q
