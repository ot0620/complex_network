def min_abs_fiedler(fiedler_vector, g, removed_edges):
    # フィードラーベクトルを1次元配列として取得
    fiedler_vector = np.array(fiedler_vector)

    # グラフのエッジリストを取得（削除されたエッジは除外）
    edges = [(e.source(), e.target()) for e in g.edges() if e not in removed_edges]

    # エッジリストからノードペアのインデックスを抽出
    node_pairs = np.array(edges, dtype=int)  # データ型を明示的に整数型に変換

    # 各エッジに対応するノードペアの差分を計算
    diffs = np.abs(fiedler_vector[node_pairs[:, 0]] - fiedler_vector[node_pairs[:, 1]])

    # 最小差分と対応するノードペアを取得
    min_diff_idx = np.argmin(diffs)
    min_diff = diffs[min_diff_idx]
    node_pair = tuple(node_pairs[min_diff_idx])

    np_tuple = (node_pair)

    # 通常の Python の整数タプルに変換
    python_tuple = tuple(int(x) for x in np_tuple)

    return python_tuple