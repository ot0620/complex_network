from graph_tool.all import *
import graph_tool.all as gt
import numpy as np
import random

def create_network(n, m, beta, seed=None):
    if seed is not None:
        np.random.seed(seed=seed)

    initial_nodes = m + 1
    g = gt.complete_graph(initial_nodes, directed=False)
    node_list = list(range(initial_nodes))
    node_id_property = g.new_vertex_property("int")

    for i in range(initial_nodes):
        node_id_property[g.vertex(i)] = i

    node_id = initial_nodes - 1

    # 初期ネットワークの次数リストを作成
    K_array_before = [v.out_degree() for v in g.vertices()]

    for i in range(initial_nodes, n):

        if beta == 0 or beta >= 1:
            K_array = np.array(K_array_before) ** beta
        elif beta == 1 / 2:
            K_array = np.sqrt(np.array(K_array_before))
        else:
            ipa = abs(beta)
            K_array = 1 / np.power(np.array(K_array_before), ipa, dtype=np.float64)

        g.add_vertex()
        K_array_before.append(0)  # 新しく追加したノードの次数を0で初期化

        for _ in range(m):
            # 次数に比例した確率ベクトルを生成
            s = np.sum(K_array)
            parray = K_array / s
            parray /= np.sum(parray)  # 確率の合計を1.0に調整

            # 次数に比例した確率で既存のノードを選び、エッジとする
            cumulative_probs = np.cumsum(parray)
            r = random.random()
            new = node_list[np.searchsorted(cumulative_probs, r)]

            # エッジを追加
            g.add_edge(g.vertex(i), g.vertex(new))

            K_array_before[i] += 1
            K_array_before[new] += 1

            # ノードの次数を0に設定（選ばれたノードは次回選ばれないように）
            K_array[node_list.index(new)] = 0.

        node_list.append(i)
        node_id += 1
        node_id_property[g.vertex(i)] = node_id

    g.vertex_properties["node_id"] = node_id_property
    return g