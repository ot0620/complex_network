###
total_loop = 0
multiple_edge = 0
# グラフ g のすべてのノードとエッジを調査
for v in tqdm(g.vertices()):
    # 自己ループの検出
    if g.edge(v, v) is not None:
        print(f"ノード {int(g.vp.node_id[v])} に自己ループが存在します。")
        total_loop += 1

    # 多重リンクの検出
    for u in g.vertices():
        if u != v:
            edges = list(g.edge(v, u, all_edges=True))
            if len(edges) > 1:
                print(f"ノード {int(g.vp.node_id[v])} と {int(g.vp.node_id[u])} の間に多重リンクが存在します。")
                multiple_edge += 1

print(f"自己ループは{int(total_loop)}個あります。")
print(f"多重リンクは{int(multiple_edge)}個あります。")
