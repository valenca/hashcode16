import greedy

class Slot:
    def __init__(self, x, y, painted=False):
        self.x = x
        self.y = y
        self.painted = painted

    def dist(self, s):
        return max(abs(self.x-s.x) , abs(self.y-s.y))

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    def __repr__(self):
        return self.__str__()

class Cluster:
    def __init__(self, slot, neigh):
        self.slot  = slot
        self.neigh = neigh

class Grid:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[Slot(x,y) for y in range(n_cols)] for x in range(n_rows)]
        self.to_paint = []

    def neighbours(self, slot, dist):
        res = []
        for i in xrange(max(0, slot.x-dist), min(slot.x+dist, self.n_rows-1)+1):
            for j in xrange(max(0, slot.y-dist),min(slot.y+dist, self.n_cols-1)+1):
                if i != 0 or j != 0:
                    res.append(self.grid[i][j])
        return res

    def line_sweep(self, size):
        neigh = {}
        for i, slot in enumerate(self.to_paint):
            neigh[slot] = filter(lambda  s: s.painted ,
                                 self.neighbours(slot, size))
        res = {}
        while neigh != {}:
            next      = max(neigh, key = lambda x: len(neigh[x]))
            to_remove = neigh.pop(next)
            res[next] = to_remove
            for n in to_remove:
                neigh.pop(n, None)
        return res

def read_input():
    N, M = list(map(int, raw_input().split()))
    g = Grid(N, M)

    for x in range(N):
        line = list(raw_input())
        for y in range(len(line)):
            if line[y]=="#":
                g.grid[x][y].painted = True
                g.to_paint.append(g.grid[x][y])
    g.to_paint.sort(key = lambda s: s.x)
    return g

def solve(g):
    size = 20
    clusters = g.line_sweep(size)
    for c in clusters:
        arr = [[] for n in clusters[c]]
        s = clusters[x]
        greedy.greedy(2*size+1, clusters[c], )

if __name__ == '__main__':
    g = read_input()


    # clusters = g.line_sweep(100)
    # for c in clusters:
    #     print c, "neigh=", clusters[c]
