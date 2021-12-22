"""
顶点排序：
    当进行深度搜索时，每搜索完一个顶点就将其放入栈中，那么最后栈中的顶点，就是排序好的顶点的集合。

API设计：
    类名：DepthFirstOrder
    构造方法：
        - __init__(G) 创建一个顶点排序对象，将G图中的顶点进行排序，返回一个顶点的线性栈
    成员方法：
        - dfs(G, v) 基于深度优先搜索，生成线性序列
        - get_stack() 获取顶点线性序列
    成员变量：
        - marks 一个列表。索引代表顶点，值表示当前顶点是否已经被搜索
        - stack 一个栈，存储顶点线性序列
"""

from 数据结构与算法.数据结构.图.有向图 import Digraph
from 数据结构与算法.数据结构.线性表.栈.栈 import Stack


class DepthFirstOrder:
    def __init__(self, G):
        self.marks = [False] * G.vertex_count
        self.stack = Stack()

        # 以图中每个顶点为入口做一次深度搜索
        for v in range(G.vertex_count):
            if not self.marks[v]:
                self.dfs(G, v)

    def dfs(self, G, v):
        # 把当前顶点标记为已搜索
        self.marks[v] = True

        # 遍历搜索当前结点的邻接点
        for w in G.adj[v]:
            if not self.marks[w]:
                self.dfs(G, w)

        # 当前结点搜索完毕后，将其入栈
        self.stack.push(v)

    def get_stack(self):
        return self.stack


if __name__ == '__main__':
    g = Digraph(10)
    g.add_edge(0, 1)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(3, 4)
    g.add_edge(4, 7)
    g.add_edge(6, 7)
    g.add_edge(7, 0)

    d = DepthFirstOrder(g)

    for i in d.get_stack():
        print(i, end=" ")
