from graph_tool.all import *
import graph_tool.all as gt
import numpy as np
import random

def create_network(n, m, beta, seed=None):
    # 乱数生成のシードを設定可能
    if seed is not None:
        np.random.seed(seed=seed)

    initial_nodes = m + 1  # 初期ノード数:m + 1

    g = gt.complete_graph(initial_nodes, directed=False)  # 初期の完全グラフを生成

    initial_edges = list(g.edges())  # 初期のリンクの一覧を生成

    node_list = list(range(initial_nodes))  # 初期のノードの一覧を生成

    node_id_property = g.new_vertex_property("int")  # ノードIDを格納する新しいプロパティ

    # 初期ノードのNode_IDを手動で割り当てる
    for i in range(initial_nodes):
        node_id_property[g.vertex(i)] = i

    node_id = initial_nodes - 1  # 次のノードID

    # 新規ノードを追加し、リンクをべき乗の値を参照して追加していく
    for i in range(initial_nodes, n):

        # 現在のネットワークの各ノードの次数を計算しk_array_before配列に保管
        K_array_before = np.array(
            [v.out_degree() for v in g.vertices() if v.out_degree() != 0])  # 次数の配列 全頂点の次数（次数が0のノードを除外）

        # べき乗の値によって、K_array_beforeの中身を再計算する
        if beta == 0 or beta >= 1:
            K_array = K_array_before ** beta
        elif beta == 1 / 2:
            K_array = np.sqrt(K_array_before)
        else:
            ipa = abs(beta)
            K_array = 1 / np.power(K_array_before, ipa, dtype=np.float64)

        g.add_vertex()  # 新規ノードを追加

        for j in range(m):
            # 次数に比例した確率ベクトルを生成
            s = np.sum(K_array)
            parray = K_array / s
            parray /= np.sum(parray)  # 確率の合計を1.0に調整

            # 次数に比例した確率で既存のノードを選び、エッジとする
            cumulative_probs = np.cumsum(parray)
            r = random.random()
            new = node_list[np.searchsorted(cumulative_probs, r)]
            g.add_edge(g.vertex(i), g.vertex(new))

            K_array[node_list.index(new)] = 0.

        node_list.append(i)  # 新規ノードをノードリストに追加する
        node_id += 1  # 新しいノードIDを割り当てる
        node_id_property[g.vertex(i)] = node_id  # ノードIDをプロパティに格納

    g.vertex_properties["node_id"] = node_id_property  # ノードIDのプロパティを設定

    return g