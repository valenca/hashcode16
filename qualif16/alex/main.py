import data
from math import sqrt, ceil

hilbert_map = {
   'a': {(0, 0): (0, 'd'), (0, 1): (1, 'a'), (1, 0): (3, 'b'), (1, 1): (2, 'a')},
   'b': {(0, 0): (2, 'b'), (0, 1): (1, 'b'), (1, 0): (3, 'a'), (1, 1): (0, 'c')},
   'c': {(0, 0): (2, 'c'), (0, 1): (3, 'd'), (1, 0): (1, 'c'), (1, 1): (0, 'b')},
   'd': {(0, 0): (0, 'a'), (0, 1): (3, 'c'), (1, 0): (1, 'd'), (1, 1): (2, 'd')},
}

def point_to_hilbert(x, y, h, w):
    order=1
    while order<max(h,w):
        order*=2
    current_square = 'a'
    position = 0
    for i in range(order - 1, -1, -1):
        position <<= 2
        quad_x = 1 if x & (1 << i) else 0
        quad_y = 1 if y & (1 << i) else 0
        quad_position, current_square = hilbert_map[current_square][(quad_x, quad_y)]
        position |= quad_position
    return position


def dist(x1, y1, x2, y2):
    return ceil(sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)))

def dist_warehouses(o, warehouses):
    m = dist(warehouses[0].x, warehouses[0].y, o.x, o.y)
    for w in warehouses:
        if dist(w.x, w.y, o.x, o.y) < m:
            m = dist(w.x, w.y, o.x, o.y)
    return m
        

T, prods, warehouses, orders, drones, nr, nc = data.read_input()
orders2 = orders[::]

orders.sort(key=lambda o: o.total_weight())

# Sort warehouses per order
ow = []
for o in orders:
    ow.append([])
    for w in warehouses:
        ow[-1].append([w, dist(o.x, o.y, w.x, w.y)])
    ow[-1].sort(key=lambda w: w[1])

work_list = []
# Get items from warehouses
for i in range(len(orders)):
    for it in orders[i].items:
        for j in range(orders[i].items[it]):
            for w in ow[i]:
                if w[0].items[it.index] > 0:
                    orders[i].items[it] -= 1
                    w[0].items[it.index] -= 1
                    work_list.append([w[0], orders[i].index, it])
                    break

# Remove unfinished orders of work list
to_remove = []
for i in range(len(work_list)):
    a = True
    for it in orders[work_list[i][1]].items:
        if orders[work_list[i][1]].items[it] > 0:
            a = False
            break
    if a == False:
        to_remove.append(i)
        #work_list.remove(w)

for it in to_remove[::-1]:
    work_list.pop(it)

ot = [0] * len(orders)
tasks = []
d = 0
w = 0
d_task = {}
# Give tasks to drones
for i in range(len(work_list)):
    if work_list[i][1] == work_list[i-1][1]:
        if w + work_list[i][2].weight > drones[d].max_weight:
            # print loads
            for t in d_task:
                tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
            for t in d_task:
                tasks.append("%d D %d %d %d" % (d, work_list[i][1], int(t.split(":")[1]), d_task[t]))
            w = 0
            d_task = {}

    elif work_list[i][1] != work_list[i-1][1]:
        for t in d_task:
            tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
        for t in d_task:
            tasks.append("%d D %d %d %d" % (d, work_list[i-1][1], int(t.split(":")[1]), d_task[t]))

        d = (d + 1) % len(drones)
        w = 0
        d_task = {}
        
    try:
        d_task["%d:%d" % (work_list[i][0].index, work_list[i][2].index)] += 1
        ot[work_list[i][1]] += 1 + dist(work_list[i][0].x, work_list[i][0].y, orders2[work_list[i][1]].x, orders2[work_list[i][1]].y) 
    except KeyError:
        d_task["%d:%d" % (work_list[i][0].index, work_list[i][2].index)] = 1
        ot[work_list[i][1]] += 1 + dist(work_list[i][0].x, work_list[i][0].y, orders2[work_list[i][1]].x, orders2[work_list[i][1]].y) 

    w += work_list[i][2].weight


for t in d_task:
    tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
for t in d_task:
    tasks.append("%d D %d %d %d" % (d, work_list[-1][1], int(t.split(":")[1]), d_task[t]))




# AGAIN
work_list.sort(key=lambda wl: (ot[wl[1]],ot[wl[0].index]))

ot = [0] * len(orders)
tasks = []
d = 0
w = 0
d_task = {}
# Give tasks to drones
for i in range(len(work_list)):
    if work_list[i][1] == work_list[i-1][1]:
        if w + work_list[i][2].weight > drones[d].max_weight:
            # print loads
            for t in d_task:
                tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
            for t in d_task:
                tasks.append("%d D %d %d %d" % (d, work_list[i][1], int(t.split(":")[1]), d_task[t]))
            w = 0
            d_task = {}

    elif work_list[i][1] != work_list[i-1][1]:
        for t in d_task:
            tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
        for t in d_task:
            tasks.append("%d D %d %d %d" % (d, work_list[i-1][1], int(t.split(":")[1]), d_task[t]))

        d = (d + 1) % len(drones)
        w = 0
        d_task = {}
        
    try:
        d_task["%d:%d" % (work_list[i][0].index, work_list[i][2].index)] += 1
    except KeyError:
        d_task["%d:%d" % (work_list[i][0].index, work_list[i][2].index)] = 1

    w += work_list[i][2].weight


for t in d_task:
    tasks.append("%d L %d %d %d" % (d, int(t.split(":")[0]), int(t.split(":")[1]), d_task[t]))
for t in d_task:
    tasks.append("%d D %d %d %d" % (d, work_list[-1][1], int(t.split(":")[1]), d_task[t]))

print(len(tasks))
for t in tasks:
    print t

