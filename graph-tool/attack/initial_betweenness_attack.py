def initial_betweenness_attack(g,Node):

    vertex_IB_list, edge_IB_list = gt.betweenness(g)
    vertex_list = [v for v in g.vertices()]
    randomized_vertex_list = list(range(0, len(vertex_list)))
    random.shuffle(randomized_vertex_list)
    combined_vertex_list = list(zip(vertex_list, vertex_IB_list, randomized_vertex_list))
    sorted_combined_vertex_list = sorted(combined_vertex_list, key=lambda v: (v[1], v[2]))
    IB_rewiring_g = [v for (v, s, t) in sorted_combined_vertex_list]

    sizes, comp = gt.vertex_percolation(g, IB_rewiring_g)
    betweenness_attack = [frc for frc in sizes]
    perc = np.array(betweenness_attack)
    perc = perc / Node
    return perc