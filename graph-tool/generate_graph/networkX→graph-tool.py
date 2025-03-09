# networkxのノードをgraph-toolのノードに追加
node_map = {}  # networkxのノードとgraph-toolのノードの対応を保持する辞書
for node_nx in G.nodes():
    node_gt = g.add_vertex()
    node_map[node_nx] = node_gt

# networkxのエッジをgraph-toolのエッジに追加
for edge_nx in G.edges():
    node_u = node_map[edge_nx[0]]
    node_v = node_map[edge_nx[1]]
    g.add_edge(node_u, node_v)

#### 例 ####

import networkx as nx
import graph_tool.all as gt

# networkxのグラフを作成
G = nx.complete_graph(14)
# graph-toolのグラフオブジェクトを作成
g = gt.Graph(directed=False)

# networkxのノードをgraph-toolのノードに追加
node_map = {}  # networkxのノードとgraph-toolのノードの対応を保持する辞書
for node_nx in G.nodes():
    node_gt = g.add_vertex()
    node_map[node_nx] = node_gt

# networkxのエッジをgraph-toolのエッジに追加
for edge_nx in G.edges():
    node_u = node_map[edge_nx[0]]
    node_v = node_map[edge_nx[1]]
    g.add_edge(node_u, node_v)

# グラフを描画して確認
gt.graph_draw(g, output_size=(300, 300))
