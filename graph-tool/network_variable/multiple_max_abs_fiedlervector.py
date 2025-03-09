def top_k_max_abs_fiedler(fiedler_vector, g, k):
    """
    フィードラーベクトルの差分が大きい順に最大 k 個のノードペアを取得
    """
    # フィードラーベクトルを1次元配列として取得
    fiedler_vector = np.array(fiedler_vector)

    # 差分行列の計算（|fiedler[i] - fiedler[j]|）
    diff_matrix = np.abs(fiedler_vector[:, None] - fiedler_vector[None, :])

    # 隣接行列を取得
    adjacency = gt.adjacency(g).toarray()

    # エッジがないノードペアのみを対象とするフィルタ
    mask = (adjacency == 0)  # 隣接していないノードペアが True

    # 差分行列にマスクを適用
    diff_matrix[~mask] = -np.inf  # エッジが存在する部分は無効化 (-∞)

    # 上三角行列部分のみを対象にする（重複排除）
    triu_indices = np.triu_indices_from(diff_matrix, k=1)
    valid_diff_values = diff_matrix[triu_indices]

    # 大きい順に k 個のインデックスを取得
    top_k_indices = np.argpartition(valid_diff_values, -k)[-k:]
    top_k_indices = top_k_indices[np.argsort(valid_diff_values[top_k_indices])[::-1]]

    # インデックスを2次元に戻し、ノードペアに変換
    node_pairs = [(triu_indices[0][idx], triu_indices[1][idx]) for idx in top_k_indices]

    return node_pairs