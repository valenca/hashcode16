import greedy
import data
from sys import argv

g = data.read_input()
c = data.make_clusters(g, int(argv[1]))
for i in range(len(c)):
    a = c[i]
    d = a.size*2 +1
    ox = a.center.x - a.size
    oy = a.center.y - a.size
    v = [[s.x-ox, s.y-oy] for s in list(a.grid.paint)]
    greedy.greedy(d, v, ox, oy)
