# Layoutアルゴリズムで頂点の位置を決定
pos = gt.sfdp_layout(g)
gt.graph_draw(g, pos=pos, output_size=(800, 800), output=None)