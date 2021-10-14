'''
环：
    即在有向图中，顶点和有向边一起构成了一个圈，这条路径始终可以找到下一个顶点。

检测有环的API设计：
    类名：DirectedCycle
    构造方法：
        - __init__(G)  创建一个检测环对象，检测图G中是否有环
    成员方法：
        - dfs(G, v) 基于深度优先搜索，检测G图中是否有环
        - has_cycle() 判断图中是否有环
    成员变量：
        - marks 一个列表。索引代表顶点，值表示当前顶点是否已经被搜索
        - cycle bool值，表示当前图中是否有环
        - stack 一个列表。索引代表顶点，使用栈的思想，记录当前顶点是否正处于正在搜索的路径上
'''
from 数据结构与算法.数据结构.图.有向图 import Digraph


class DirectedCycle:
    def __init__(self, G):
        self.marks = [False] * G.vertex_count
        self.cycle = False
        self.stack = [False] * G.vertex_count

        # 由于检测的有向图，所以需要遍历每一个顶点作为起点时，图中是否有环
        for v in range(len(self.marks)):
            # 如果当前顶点没被搜索过，就调用深度搜索
            if not self.marks[v]:
                self.dfs(G, v)

    def dfs(self, G, v):
        # 把当前顶点标记为已搜索
        self.marks[v] = True

        # 把当前顶点入栈
        self.stack[v] = True

        # 遍历搜索当前顶点的邻接点
        for w in G.adj[v]:
            # 如果顶点没有被搜索，就递归调用深度搜索
            if not self.marks[w]:
                self.dfs(G, w)
                continue

            # 如果当前结点已经被搜索，就看当前顶点是否已经在当前搜索的路径栈中，如果在，则说明找到了环
            if self.stack[w]:
                self.cycle = True
                break

        # 如果没找到环就让当前顶点出栈
        self.stack[v] = False

    @property
    def has_cycle(self):
        return self.cycle


if __name__ == '__main__':
    g = Digraph(10)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(3, 4)
    g.add_edge(4, 7)
    g.add_edge(6, 7)
    g.add_edge(7, 0)

    d = DirectedCycle(g)
    print(d.has_cycle)
