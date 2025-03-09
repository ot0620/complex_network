# 頂点ごとにコミュニティ（モジュール番号）が割り当てられたグラフを用意する
state = gt.BlockState(g, b=g.vp.module_number)
# graph_tool.inference.modularity 関数を使ってモジュラリティ Q を計算
Q = gt.modularity(g, state.get_blocks())