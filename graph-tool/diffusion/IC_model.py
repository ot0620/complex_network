S = 0
I = 1
R = -1

#感染確率x
x = 0.1
#回復率r
r = 0.1

def SIR():
    # 全ノードをランダムに並べ替える
    vs = list(G.vertices())
    rnd.shuffle(vs)
    # 並べ替えたノードリストを走査し状態更新を行う
    for v in vs:
        if state[v] == I:  # 状態が 'I' の場合
            # 隣接ノードを取得
            ns = list(v.out_neighbors())
            for w in ns:
                # 隣接ノードが 'S' 状態かどうかを確認し、確率 x で 'I' 状態に変更
                if state[w] == S and rnd.random() < x:
                    state[w] = I
            # 状態が確率 r で 'R' 状態に変更
            if rnd.random() < r:
                state[v] = R
    return