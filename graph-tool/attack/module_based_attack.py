def inter_intra(g):
    # intra, interlinkのリストを初期化
    intra_link = []
    inter_link = []

    # intra, interlinkを識別
    for edge in g.edges():
        source_vertex = edge.source()
        target_vertex = edge.target()

        if g.vp.module_number[source_vertex] == g.vp.module_number[target_vertex]:
            intra_link.append(edge)
        else:
            inter_link.append(edge)

    return intra_link

def module_based_attack(graph, intra_link):

    #### 3. コミュニティ間の接続に参加しているノード（またはエッジ）のリストを作成する。 ####

    # 空の集合を作成（重複の排除）
    intercommunity_nodes = set()
    # Gの全てのedgeに対してループを回す
    for edge in graph.edges():
        # 現在のedgeの始点ノードを取得
        source_vertex = edge.source()
        # 現在のedgeの終点ノードを取得
        target_vertex = edge.target()
        # 始点ノードと終点ノードが異なるモジュールに所属していれば、
        if graph.vp.module_number[source_vertex] != graph.vp.module_number[target_vertex]:
            # intercommunity_nodesにノードを追加
            intercommunity_nodes.add(source_vertex)
            intercommunity_nodes.add(target_vertex)

    #### 4. (ノードまたはエッジの)間の中心性の降順に従ってリストをソートする。 ####
    # ノードの媒介中心性のリストを返す
    node_betweenness = gt.betweenness(graph)[0]
    # intercommunity_nodesのリストを媒介中心性の高い順にソートする
    sorted_nodes = sorted(intercommunity_nodes, key=lambda v: node_betweenness[v], reverse=True)

    #### 5. リストの先頭から1つずつノード（またはエッジ）を削除する。 ####
    #### 6. 2つのコミュニティ間のリンクからノードが削除されると、他のコミュニティ間の接続にもう一方のノードが参加していない限り、 ####
    ####    そのノードはリストからスキップされる。 ####
    #### 7. 攻撃は常にネットワークの最大連結成分に限定される。####

    # 削除されるノードの保存用リストを初期化
    removed_nodes = []
    # ソートされたノードがなくなるまでループ
    while sorted_nodes:
        # リストからノードを取り出す
        node = sorted_nodes.pop(0)
        # ノードがすでにremoved_nodesにないかを確認。リストになければ、、
        if node not in removed_nodes:
            # removed_nodesにノードを追加
            removed_nodes.append(node)

            # そのノードに隣接する全てのノードを取得し、その数だけループを繰り返す
            for neighbor in node.all_neighbors():

                # 隣接ノードとそのノードのモジュール番号が違ければ、、、
                if graph.vp.module_number[neighbor] != graph.vp.module_number[node]:
                    # その隣接ノードがまだsorted_nodesに存在すれば、、、
                    if neighbor in sorted_nodes:
                        # sorted_nodesから隣接ノードを削除する
                        sorted_nodes.remove(neighbor)

            # Gの最大連結成分に含まれるノードに対してTrueを、それ以外のノードに対してFalseを持つブールマスクを返す
            lcc_vertex_mask = gt.label_largest_component(graph)
            # Trueとなるノードのみをsorted_nodesに格納
            sorted_nodes = [v for v in sorted_nodes if lcc_vertex_mask[v]]

    # 削除されたノードの数がグラフ graphの全ノード数より少ない場合
    if len(removed_nodes) < graph.num_vertices():
        # まだ削除リストに含まれていないノードのセットを計算
        nodes_not_removed = set(graph.iter_vertices()) - set(removed_nodes)
        # どれだけのノードが削除リストに追加されるべきかを計算
        padding_required = graph.num_vertices() - len(removed_nodes)

        # 削除リストに含まれていないノードの数だけループ
        for node in nodes_not_removed:
            # もし、padding_requiredが0になれば、処理を終了
            if padding_required <= 0:
                break
            # 削除リストノードを追加
            removed_nodes.append(node)
            # 必要なノード数を１減少
            padding_required -= 1

    #print(len(removed_nodes))
    # リストを逆順に。
    removed_nodes.reverse()
    return removed_nodes