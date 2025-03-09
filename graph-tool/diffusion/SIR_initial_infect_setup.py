# 状態初期化、ランダムに初期感染者を選ぶ場合
for v in G.vertices():
    state[v] = S
nodes = list(G.vertices())
random.shuffle(nodes)
for v in nodes[:v_change]:
    state[v] = I

# 状態初期化、ノードの次数の高い順に初期感染者を選ぶ場合
for v in G.vertices():
    state[v] = S
nodes = list(G.vertices())
nodes_degrees = [(v, G.vertex(v).in_degree() + G.vertex(v).out_degree()) for v in nodes]
nodes_sorted = [v for v, _ in sorted(nodes_degrees, key=lambda x: x[1], reverse=True)]
for v in nodes_sorted[:v_change]:
    state[v] = I

# 状態初期化、ノードの次数の低い順に初期感染者を選ぶ場合
for v in G.vertices():
    state[v] = S
nodes = list(G.vertices())
nodes_degrees = [(v, G.vertex(v).in_degree() + G.vertex(v).out_degree()) for v in nodes]
nodes_sorted = [v for v, _ in sorted(nodes_degrees, key=lambda x: x[1])]
for v in nodes_sorted[:v_change]:
    state[v] = I
