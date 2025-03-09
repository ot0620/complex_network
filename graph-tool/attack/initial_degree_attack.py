def initial_degree_attack(g,Node):

    vertices = sorted([v for v in g.vertices()], key=lambda v: v.out_degree())
    sizes, comp = gt.vertex_percolation(g, vertices)
    degree_attack = [frc for frc in sizes]
    perc = np.array(degree_attack)
    perc = perc / Node

    return perc