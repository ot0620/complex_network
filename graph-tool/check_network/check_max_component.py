# Define function to check sum_u
def check_sum_u(g, target_sum):
    l = gt.label_largest_component(g)
    u = gt.GraphView(g, vfilt=l)
    sum_u = u.num_vertices()
    return sum_u == target_sum