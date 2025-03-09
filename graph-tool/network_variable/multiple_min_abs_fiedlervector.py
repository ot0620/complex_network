def top_k_min_abs_fiedler(fiedler_vector, g, k):
    """
    フィードラーベクトルの差分が小さい順に最小 k 個のノードペアを取得
    """
    # フィードラーベクトルを1次元配列として取得
    fiedler_vector = np.array(fiedler_vector)

    # グラフのエッジリストを取得（削除されたエッジは除外）
    edges = [(e.source(), e.target()) for e in g.edges()]

    # ノードペアの順序を固定（小さいノード番号が先に来るようにソート）
    edges = [tuple(sorted(edge)) for edge in edges]

    # 重複を排除
    unique_edges = list(set(edges))

    # 各エッジに対応するノードペアの差分を計算
    node_pairs = np.array(unique_edges, dtype=int)  # データ型を明示的に整数型に変換
    diffs = np.abs(fiedler_vector[node_pairs[:, 0]] - fiedler_vector[node_pairs[:, 1]])

    # 小さい順に k 個のインデックスを取得
    top_k_indices = np.argpartition(diffs, k)[:k]
    top_k_indices = top_k_indices[np.argsort(diffs[top_k_indices])]

    # インデックスからノードペアに変換
    top_k_node_pairs = [tuple(node_pairs[idx]) for idx in top_k_indices]

    return top_k_node_pairs