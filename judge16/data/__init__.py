class Slot:
    def __init__(self, x, y, paint=False):
        self.x = x
        self.y = y
        self.paint = paint
        self.painted = False
        self.neigh = set()
        self.neigh_count = 0

    def __str__(self):
        return "%d %d" % (self.x, self.y)

class Grid:
    def __init__(self, n_rows, n_collumns):
        self.n_rows = n_rows
        self.n_collumns = n_collumns
        self.grid = [[Slot(x,y) for y in range(n_collumns)] for x in range(n_rows)]
        self.paint = []

    def print_grid(self, cluster=None):
        for line in self.grid:
            s = ""
            for slot in line:
                if cluster != None:
                    a = False
                    for c in cluster:
                        if slot == c.center:
                            s = s + "X"
                            a = True
                            break
                    if a == True:
                        continue
                if slot.paint:
                    s = s + "*"
                else:
                    s = s + " "
            print(s)

class Cluster:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.grid = Grid(size, size)

    def add_point(self, p):
        self.grid.paint.append(p)

    def __str__(self):
        return "Center: %d %d Size: %d" % (self.center.x, self.center.y, self.size)



def read_input():
    N, M = list(map(int, raw_input().split()))
    g = Grid(N, M)

    for x in xrange(N):
        line = list(raw_input())
        for y in xrange(len(line)):
            if line[y]=="#":
                g.grid[x][y].paint = True
                g.paint.append(g.grid[x][y])

    return g

def make_clusters(g, d):
    clusters = []

    # Get neighbors to all points
    for i in xrange(len(g.paint)):
        g.paint[i].neigh.add(g.paint[i])
        g.paint[i].neigh_count += 1
        for j in xrange(i+1, len(g.paint)):
            if g.paint[j].x - g.paint[i].x > d:
                break
            elif abs(g.paint[j].y - g.paint[i].y) > d:
                continue
            else:
                g.paint[i].neigh.add(g.paint[j])
                g.paint[j].neigh.add(g.paint[i])

    # Check neigh count
    sorted_points = sorted(g.paint, reverse=True, key=lambda p:len(p.neigh))
    p = max(sorted_points, key=lambda p:len(p.neigh))

    # Build clusters
    while True:
        if len(p.neigh) > 0:
            c = Cluster(p, d)
            clusters.append(c)
            for s in list(p.neigh):
                c.add_point(s)
                if s == p:
                    continue
                for sp in list(s.neigh):
                    if sp == s:
                        continue
                    sp.neigh.remove(s)
                s.neigh = set()
            p.neigh = set()
            p = max(sorted_points, key=lambda p:len(p.neigh))
        else:
            break


    return clusters

def print_clusters(clusters):
    for c in clusters:
        print(c)

if __name__ == '__main__':
    g = read_input()
    #for s in g.paint:
    #    print("%d %d" % (s.x, s.y))
    #print(g.paint)
  
    c = make_clusters(g, 1)
    print_clusters(c)
    
    g.print_grid(c)

