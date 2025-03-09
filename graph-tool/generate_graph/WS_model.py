# WSモデルの関数
def ws_graph(n, k, p):
    # 基本となる円形格子を生成
    base_g = gt.circular_graph(n, k)

    # p = 0、リンクの張替えをしない場合は、そのまま円形格子を返却する
    if p == 0:
        return base_g

    # リンクの張替えがあり得る場合、空の無向グラフ(directed = False)を生成し、n個のノード数を付け加える
    g = gt.Graph(directed=False)
    g.add_vertex(n)
    # 張替え前のbase_gのすべてのリンクを走査し、生成乱数がpより少なければ、リンクの張替えを行う
    # ただし、複数リンク・自己ループとならないようにする
    for edg in base_g.edges():
        st_vtx = edg.source()
        tg_vtx = edg.target()
        if rnd.random() < p:
            # 新しいリンク先の候補を生成
            nw_tg_idx = rnd.choice(n)
            nw_tg_vtx = base_g.vertex(nw_tg_idx)
            while ((nw_tg_vtx in st_vtx.all_neighbors())
                   or nw_tg_vtx == st_vtx):
                # もし、新しいリンク先によって複数リンク・自己ループになる場合、別のリンク先を新たに探す
                nw_tg_idx = rnd.choice(n)
                nw_tg_vtx = base_g.vertex(nw_tg_idx)
            if g.edge(st_vtx, nw_tg_vtx) == None:
                # 以前のリンク張替えによって、張ろうとするリンクがすでにある場合をのぞき、リンクの張替えを行う
                g.add_edge(st_vtx, nw_tg_vtx)
        else:
            if g.edge(st_vtx, tg_vtx) == None:
                g.add_edge(st_vtx, tg_vtx)
    return g