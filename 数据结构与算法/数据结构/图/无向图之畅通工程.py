"""
畅通工程：
    某省调查城镇（共20个城镇）之间的交通状况，并列出了每条道路直接连接的两个城市编号。
    已经建好道路的城镇：(0,1),(6,9),(3,8),(5,11),(2,12),(6,10),(4,8)
    畅通工程的目标是使城镇之间都可以实现交通（不一定要直达，间接到达也可以）
    问：10号城市是否和9号城市相通；8号城市是否和9号城市相通

解决思路：
    1、创建一个Graph对象，为已经创建好的城市之间添加一条边
    2、创建一个深度优先搜索对象，把顶点9作为初始化顶点传入
    3、调用marked就可以得到城市之间的连通情况
"""

from 无向图 import Graph
from 无向图之深度优先搜索 import DepthFirstSearch

G = Graph(20)
G.add_edge(0, 1)
G.add_edge(6, 9)
G.add_edge(3, 8)
G.add_edge(5, 11)
G.add_edge(2, 12)
G.add_edge(6, 10)
G.add_edge(4, 8)

dfs = DepthFirstSearch(G, 9)

print("10号城市是否和9号城市相通:", dfs.marked(10))
print("8号城市是否和9号城市相通:", dfs.marked(8))
