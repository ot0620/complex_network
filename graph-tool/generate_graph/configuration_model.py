#チェーン構造を解消するためのリワイヤリングコード
def rewire_network(g, rewiring_times):
    #print("random_rewire開始")
    gt.random_rewire(g, model = "configuration", n_iter = rewiring_times, edge_sweep=True)
    #print("random_rewire終了")
    return g