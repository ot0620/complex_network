S = 0
I = 1
R = -1

x = 0.3
T = 0.3
r = 0

max_itr = 200

# 何回で平均をとるのか？
num_iterations = 100

def Hybrid_SIR():
    # 全ノードをランダムに並べ替える
    vs = list(G.vertices())
    rnd.shuffle(vs)

    # 並べ替えたノードリストを走査し状態更新を行う
    for v in vs:
        if state[v] == I:  # 状態が 'I' の場合
            ns = list(v.out_neighbors())  # 'I'状態のノードにおける隣接ノードを取得

            for w in ns:
                if state[w] == S and rnd.random() < x:  # 'S'状態のノードを確率xで取得する
                    ws = list(w.out_neighbors())  # 'S状態のノード'における隣接ノードを取得

                    # 20の値は1モジュールあたりのノード数や次数分布によって変動する。
                    if len(ws) > 20:
                        ws_subset = random.sample(ws, 20)  # 隣接ノードの総数が20より大きい場合、ランダムで20個ノードを選ぶ。
                    else:
                        ws_subset = ws  # 隣接ノードの総数が20より小さい場合、全ての隣接ノードを参照する

                    num_infected_neighbors = sum(
                        1 for n in ws_subset if state[n] == I)  # 取得した隣接ノードの中から、'I'状態のノードの個数を数える

                    # もし、1つでも'I'状態のノードがあるのであれば、'I'状態のノードの割合を求める
                    if len(ws_subset) > 0:
                        infected_ratio = num_infected_neighbors / len(ws_subset)

                        # 割合がT以上なら、状態をIに変更
                        if infected_ratio >= T:
                            state[w] = I

            # 状態が確率 r で 'R' 状態に変更
            if rnd.random() < r:
                state[v] = R

    return

def node_data_numpy(G):
    # ノードの情報を格納するNumPy配列を作成
    node_ids = np.array([int(G.vp.node_id[v]) for v in G.vertices()])
    module_numbers = np.array([int(G.vp.module_number[v]) for v in G.vertices()])

    # NumPy配列を結合して2次元の配列を作成
    numpy_array = np.column_stack((node_ids, module_numbers))

    return numpy_array


# 100個のグラフの状態の平均を格納するリスト
avg_suscept_st = []
avg_infect_st = []
avg_recov_st = []

for i in tqdm(range(num_iterations)):
    G = load_graph(
        f"~/yhayashi_result/my_code/create_module/"
        f"network_data_N={number_of_node}/{net}_N={number_of_node}_L={number_of_new_link}_"
        f"M={number_of_module}_w={w}/{i}.gt.gz"
    )
    # G = load_graph(
    # f"~/yhayashi_result/my_code/create_module/"
    # f"network_data_N={number_of_node}/{net}_N={number_of_node}_L={number_of_new_link}_"
    # f"M={number_of_module}_beta_{beta}_w={w}/{i}.gt.gz"
    # )
    # 状態初期化
    state = G.new_vertex_property("int")
    for v in G.vertices():
        state[v] = S
    numpy_data = node_data_numpy(G)
    # Module_Numberが1のノードだけを抜き出す
    module_1_nodes = numpy_data[numpy_data[:, 1] == 1]
    # 取得したNode_ID（0に入っている）をリストに変換
    node_ids = module_1_nodes[:, 0].tolist()
    # ランダムに3つのノードを選択して状態をIに変更
    selected_node_ids = random.sample(node_ids, min(50, len(node_ids)))
    for v in selected_node_ids:
        state[v] = I

    suscept_st = []
    infect_st = []
    recov_st = []

    suscept_st.append(list(state.a).count(S))
    infect_st.append(list(state.a).count(I))
    recov_st.append(list(state.a).count(R))

    # シミュレーションの実行
    for updt in range(max_itr):
        SIR()
        suscept_st.append(list(state.a).count(S))
        infect_st.append(list(state.a).count(I))
        recov_st.append(list(state.a).count(R))

    # グラフごとに状態を格納
    avg_suscept_st.append(suscept_st)
    avg_infect_st.append(infect_st)
    avg_recov_st.append(recov_st)

# 100個のグラフの平均を計算
avg_suscept_st = np.mean(np.array(avg_suscept_st), axis=0)
avg_infect_st = np.mean(np.array(avg_infect_st), axis=0)
avg_recov_st = np.mean(np.array(avg_recov_st), axis=0)