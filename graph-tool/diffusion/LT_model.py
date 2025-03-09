S = 0
I = 1
R = -1

#閾値T
T = 0.3
#回復率r
r = 0.1

def LT():
    # 全ノードをランダムに並べ替える
    vs = list(G.vertices())
    rnd.shuffle(vs)
    # 並べ替えたノードリストを走査し状態更新を行う
    for v in vs:
        if state[v] == S:
            # S状態のノードの隣接ノードを取得
            ns = list(v.out_neighbors())
            # 隣接ノードの中でI状態のノードの数をカウント
            num_infected_neighbors = sum(1 for n in ns if state[n] == I)
            # 隣接ノードが存在する場合、I状態のノードの割合を計算
            if len(ns) > 0:
                infected_ratio = num_infected_neighbors / len(ns)
                # 割合がT以上なら、状態をIに変更
                if infected_ratio >= T:
                    state[v] = I
        elif state[v] == I:
            # 状態がIの場合、確率rでR状態に変更
            if rnd.random() < r:
                state[v] = R
    return