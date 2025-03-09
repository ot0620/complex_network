# 最大連結成分を求める
def max_component(g):
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    sum_u = u.num_vertices()
    return sum_u