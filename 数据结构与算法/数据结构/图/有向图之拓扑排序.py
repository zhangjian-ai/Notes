'''
前提：
    有向图中无环

拓扑排序：
    给定一幅有向图，将所有的顶点排序，使得所有的有向边均从排在前面的顶点指向排在后面的顶点，此时就可以明确的表示出每个顶点的优先级。

API设计：
    类名：Topological
    构造方法：
        - __init__(G) 创建一个拓扑排序对象
    成员方法：
        - has_cycle() 判断图G是否有环
        - get_order() 获取拓扑排序的所有顶点
    成员变量：
        - order 顶点的拓扑排序序列
'''
from 数据结构与算法.数据结构.图.有向图 import Digraph
from 有向图之检测有环 import DirectedCycle
from 有向图之顶点排序 import DepthFirstOrder


class Topological:
    def __init__(self, G):
        self.G = G
        self.order = None

        # 如果当前图没有环，就对其顶点排序
        if not self.has_cycle():
            depth_first_order = DepthFirstOrder(self.G)
            self.order = depth_first_order.get_stack()

    def has_cycle(self):
        # 判断图G是否有环
        directed_cycle = DirectedCycle(self.G)
        return directed_cycle.has_cycle

    @property
    def get_order(self):
        return self.order


if __name__ == '__main__':
    g = Digraph(10)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(3, 4)
    g.add_edge(4, 7)
    g.add_edge(6, 7)
    # g.add_edge(7, 0)

    topo = Topological(g)

    print(topo.get_order)

    for i in topo.get_order:
        print(i)
