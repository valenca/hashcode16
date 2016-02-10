class Slot:
    def __init__(self, x, y, paint=False):
        self.x = x
        self.y = y
        self.paint = paint
        self.painted = False
        self.neigh = None

class Grid:
    def __init__(self, n_rows, n_collumns):
        self.n_rows = n_rows
        self.n_collumns = n_collumns
        self.grid = [[Slot(x,y) for y in range(n_collumns)] for x in range(n_rows)]
        self.paint = []

    def print_grid(self):
        for line in self.grid:
            s = ""
            for slot in line:
                if slot.paint:
                    s = s + "#"
                else:
                    s = s + "."
            print(s)

class Cluster:
    def __init__(self, center, size):
        self.center = center
        self.size = size
        self.grid = Grid(size, size)

def read_input():
    N, M = list(map(int, raw_input().split()))
    g = Grid(N, M)

    for x in range(N):
        line = list(raw_input())
        for y in range(len(line)):
            if line[y]=="#":
                g.grid[x][y].paint = True
                g.paint.append(g.grid[x][y])

    return g


if __name__ == '__main__':
    g = read_input()
    for s in g.paint:
        print("%d %d" % (s.x, s.y))
    print(g.paint)
    g.print_grid()
