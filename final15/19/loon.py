import util
from util import Vec, Path
import random

INF = float('inf')

def metric_kcenter(nodes, k, dist_fn):
    """ farthest-first traversal implementation
        TODO try with random first node """
    assert(k <= len(nodes))
    dist = {n: INF for n in nodes}
    res  = []
    for i in xrange(k):
        n,_ = max(dist.items(), key=lambda (u,du): du)
        dist.pop(n)
        res.append(n)
        for u in dist:
            dist[u] = min(dist[u], dist_fn(u,n))
    return res




def mk_wind_graph(wind):
    max_alt = len(wind)-1
    res = {}
    for a, altitude in enumerate(wind):
        for r, row in enumerate(altitude):
            for c, vec in enumerate(row):
                res[vec] = []
                a_up, a_stay, a_down = min(a+1, max_alt), a, max(a-1, 0)
                up   = wind[a_up][r][c]
                stay = wind[a][r][c]
                down = wind[a_down][r][c]
                res[vec].append( wind[a_up][r+up.x] )


                if altitude == 0:
                    res[vec].append(wind[a+1][r+])

#     return res

# def shortest_path(s, t, neigh_fn):
#     """ BFS is enough as all distances in the wind graph are 1 """
#     q    = [s]
#     prev = {s: s}
#     while q != []:
#         u = q.pop(0)
#         if u == t: break
#         for v in neigh_fn(u):
#             if v not in prev:
#                 q.append(v)
#                 prev[v] = u
#     if u != t:
#         return Path()  # no path between s and t
#     path = []
#     while u != s:
#         path[:0] = [u]  # insert in the beggining
#         u = prev[u]
#     return Path(path)

# def shortest_cluster_path(s, t, wind):
#     best = Path()
#     for alt1 in xrange(len(wind)):
#         for alt2 in xrange(len(wind)):
#             u    = wind[alt1][s.x][s.y]
#             v    = wind[alt2][t.x][t.y]
#             best = max(best, shortest_path(u,v))
#     return best

# def mk_clusters_graph(clusters, wind):
#     res = {}
#     for a in clusters:
#         for b in clusters:
#             if a != b:
#                 res[a].append( (b, shortest_cluster_path(a,b,wind)) )
#                 best = Path()
#                 for i in xrange(len(wind)):
#                     for j in xrange(len(wind)):
#                         best = max(best, shortest_path())
#                 res[a].append(p)
#     pass

# def MST(clusters, neigh_fn):

#     pass

# def TSP(wind, clusters):
#     pass

if __name__ == '__main__':
    read_integers = lambda: [int(x) for x in raw_input().split()]
    read_pairs    = lambda: (lambda l: zip(l[::2],l[1::2]))(read_integers())
    read_vectors  = lambda: map(lambda x: Vec(*x), read_pairs())

    R, C, A    = read_integers()
    L, V, B, T = read_integers()
    r0, c0     = read_integers()
    targets    = [Vec(*read_integers()) for _ in xrange(L)]
    wind       = [[read_vectors() for r in xrange(R)] for a in xrange(A)]

    ##  get clusters of targets
    manhatan = lambda t1,t2:  abs(t1.x-t2.x)    + abs(t1.y-t2.y)
    euclid   = lambda t1,t2: (abs(t1.x-t2.x)**2 + abs(t1.y-t2.y)**2) ** 0.5
    clusters = metric_kcenter(targets, B, manhatan)

    ## get approximate TSP on clusters
    

    # STATISTICS
    # util.print_targets(R, C, targets)
    # util.print_wind_dir(wind)
    # util.print_clusters(R, C, targets, clusters)

