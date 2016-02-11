import data
from math import sqrt, ceil

def dist(x1, y1, x2, y2):
    return ceil(sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)))


T, prods, warehouses, orders, drones = data.read_input()

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
                    work_list.append([w[0], i, it])
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

