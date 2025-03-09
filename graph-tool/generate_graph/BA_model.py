# SFネットワーク生成関数
def ba(n, m, seed=None):
    # 乱数生成のシードを設定可能
    if seed is not None:
        np.random.seed(seed=seed)

    m0 = m + 1  # 初期次数:m + 1
    g = gt.Graph(directed=False)  # 初期のスター型グラフを生成
    g.add_vertex(n=m0)  # 初期のノードを追加

    for i in range(1, m0):
        g.add_edge(g.vertex(0), g.vertex(i))  # 中心の頂点とエッジを追加

    initial_edges = list(g.edges())  # 初期のリンクの一覧を生成
    node_list = list(range(m0))  # 初期のノードの一覧を生成

    # ノードを追加し、リンクを次数に比例して追加していく
    for i in range(m0, n):
        g.add_vertex()  # ノードを追加
        # 現在のネットワークの各ノードの次数を計算しk_array_before配列に保管
        K_array_before = np.array(
            [v.out_degree() for v in g.vertices() if v.out_degree() != 0])  # 次数の配列 全頂点の次数（次数が0のノードを除外）

        #      -----------------------------
        K_array = K_array_before ** 1
        #      -----------------------------

        for j in range(m):
            # 次数に比例した確率ベクトルを生成
            s = np.sum(K_array)
            parray = K_array / s

            # 次数に比例した確率で既存のノードを選び、エッジとする
            new = np.random.choice(node_list, p=parray)
            g.add_edge(g.vertex(i), g.vertex(new))

            K_array[node_list.index(new)] = 0.

        node_list.append(i)

    for edge in initial_edges:
        g.remove_edge(edge)
    return g