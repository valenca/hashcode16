import util
import random

class Vec:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    def __repr__(self):
        return self.__str__()

def metric_kcenter(nodes, k, dist_fn):
    """ TODO add random first node """
    assert(k <= len(nodes))
    dist = {n: float('inf') for n in nodes}
    res  = []
    for i in xrange(k):
        n,_ = max(dist.items(), key=lambda (u,du): du)
        dist.pop(n)
        res.append(n)
        for u in dist:
            dist[u] = min(dist[u], dist_fn(u,n))
    return res



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
    dist_fn = lambda t1,t2: abs(t1.x-t2.x) + abs(t1.y-t2.y)
    clusters   = metric_kcenter(targets, B, dist_fn)

    ## get approximate TSP on clusters
    

    # STATISTICS
    # util.print_targets(R, C, targets)
    # util.print_wind_dir(wind)
    util.print_clusters(R, C, targets, clusters)