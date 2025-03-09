def max_abs_fiedler(fiedler_vector, g):
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

    # 最大値とそのインデックスを取得
    max_diff = np.max(diff_matrix)
    node_pair = np.unravel_index(np.argmax(diff_matrix), diff_matrix.shape)

    np_tuple = (node_pair)

    # 通常の Python の整数タプルに変換
    python_tuple = tuple(int(x) for x in np_tuple)

    return python_tuple