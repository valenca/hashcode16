class Slot:
    def __init__(self, x, y, painted=False):
        self.x = x
        self.y = y
        self.painted = painted

class Grid:
    def __init__(self, n_rows, n_collumns):
        self.n_rows = n_rows
        self.n_collumns = n_collumns
        self.grid = [[Slot(x,y) for y in range(n_collumns)] for x in range(n_rows)]

    def print_grid(self):
        for line in self.grid:
            s = ""
            for slot in line:
                if slot.painted:
                    s = s + "#"
                else:
                    s = s + "."
            print(s)

def read_input():
    N, M = list(map(int, raw_input().split()))
    g = Grid(N, M)

    for x in range(N):
        line = list(raw_input())
        for y in range(len(line)):
            if line[y]=="#":
                g.grid[x][y].painted = True

    return g

if __name__ == '__main__':
    g = read_input()
    g.print_grid()
