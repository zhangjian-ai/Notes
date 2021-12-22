"""
深度优先搜索：
    在对图进行搜索的过程中，如果一个结点既有兄弟结点，又有子结点。那么优先对子结点进行搜索。

API设计：
    类名：DepthFirstSearch
    构造方法：
        - __init__(G, s) 构造深度优先搜索对象，使用深度优先搜索出G图中与s顶点的所有相同的顶点
    成员方法：
        - dfs(G, v) 使用深度优先搜索出G图中与v顶点的所有相同的顶点
        - marked(w) 判断顶点w是否与顶点s相通
        - size() 获取与顶点s相通的所有顶点的总数
    成员变量：
        - marks 一个列表，保存bool。索引代表顶点，值表示当前顶点是否已经被搜索，已经被搜索的话，表示和顶点s相通
        - count 记录有多少个顶点与s顶点相通
"""

from 无向图 import Graph


class DepthFirstSearch:
    def __init__(self, G, s):
        # marks的长度和图G相同，初始状态未连通
        self.marks = [False] * G.V
        self.count = 0

        self.dfs(G, s)

    def dfs(self, G, v):
        # 把顶点v标记为已搜索
        self.marks[v] = True

        # 找到顶点v的相邻顶点，并递归搜索
        for i in G.get_adj(v):
            # 判断顶点i是否被搜索过，如果没有被搜索，就递归
            if not self.marks[i]:
                self.dfs(G, i)

        # 连通顶点数加一
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

    dfs = DepthFirstSearch(G, 0)
    print(dfs.size)
    print(dfs.marked(3))
    print(dfs.marked(11))










