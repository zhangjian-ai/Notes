"""
广度优先搜索：
    在对图进行搜索的过程中，如果一个结点既有兄弟结点，又有子结点。那么优先对兄弟结点进行搜索。

API设计：
    类名：BreathFirstSearch
    构造方法：
        - __init__(G, s) 构造广度优先搜索对象，使用深度优先搜索出G图中与s顶点的所有相通的顶点
    成员方法：
        - bfs(G, v) 使用广度优先搜索出G图中与v顶点的所有相通的顶点
        - marked(w) 判断顶点w是否与顶点s相通
        - size() 获取与顶点s相通的所有顶点的总数
    成员变量：
        - marks 一个列表，保存bool。索引代表顶点，值表示当前顶点是否已经被搜索，已经被搜索的话，表示和顶点s相通
        - count 记录有多少个顶点与s顶点相通
        - wait_search 队列，临时存放待搜索的队列
"""

from 无向图 import Graph
from 数据结构与算法.数据结构.线性表.队列.A队列 import Queue


class BreathFirstSearch:
    def __init__(self, G, s):
        self.marks = [False] * G.V
        self.count = 0
        self.wait_search = Queue()

        self.bfs(G, s)

    def bfs(self, G, v):
        # 标记当前结点已被搜索
        self.marks[v] = True
        self.count += 1

        # 向临时队列中添加结点
        self.wait_search.enqueue(v)

        # 当临时队列有值是就循环遍历
        while not self.wait_search.is_empty:
            # 遍历搜索当前结点的相邻结点
            for i in G.adj[self.wait_search.dequeue()]:
                if not self.marks[i]:
                    self.marks[i] = True
                    # 向队列中添加当前结点
                    self.wait_search.enqueue(i)
                    # 连通数量加一
                    self.count += 1

    def marked(self, w):
        return self.marks[w]

    @property
    def size(self):
        return self.count


if __name__ == '__main__':
    G = Graph(12)
    G.add_edge(0, 1)
    G.add_edge(0, 6)
    G.add_edge(0, 2)
    G.add_edge(0, 5)
    G.add_edge(5, 10)
    G.add_edge(10, 11)
    G.add_edge(5, 7)
    G.add_edge(8, 9)
    G.add_edge(9, 3)

    dfs = BreathFirstSearch(G, 0)
    print(dfs.size)
    print(dfs.marked(3))
    print(dfs.marked(11))
