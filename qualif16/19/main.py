import sys
from data import *
from heapq import * 
from math import ceil

def read_input():
    read_ints = lambda: [int(x) for x in raw_input().split()]
    R, C, D, T, WMAX = read_ints()

    ## item types
    P = input()
    item_types = [ItemType(i, w) for i,w in enumerate(read_ints())]

    ## warehouses
    W = input()
    warehouses = []
    for i in range(W):
        x, y = read_ints()
        items = {}
        for t, quant in enumerate(read_ints()):
            if quant > 0:
                items[item_types[t]] = quant
        warehouses.append(Warehouse(i, x, y, items))

    ## orders
    C = input()
    orders = []
    for i in range(C):
        x, y   = read_ints()
        nitems = input()
        items = {}
        for t in read_ints():
            items[item_types[t]] = items.get(item_types[t], 0) + 1
        orders.append(Order(i, x, y, items, warehouses))

    ## drones
    drones = [Drone(i,warehouses[0].x, warehouses[0].y, WMAX) for i in range(D)]

    return item_types, warehouses, orders, drones, WMAX, T


def get_best_task(order, warehouses, drones):
    for it in order.items:
        for w in warehouses:
            if w[it] > 0:
                ow_dist   = distance(w.x,w.y, order.x,order.y)
                best_dist = float('inf')
                for d in drones:
                    tmp_dist = d.time + distance(d.x,d.y, w.x,w.y) + ow_dist
                    if tmp_dist < best_dist:
                        best_d    = d
                        best_w    = w
                        best_it   = it
                        best_dist = tmp_dist
    return (best_d, best_w, best_it)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        outfile = open(sys.argv[1], "w")
    else:
        outfile = sys.stdout


    item_types, warehouses, orders, drones, WMAX, T = read_input()
    # print "item_types=",item_types
    # print "warehouses=",warehouses
    # print "orders=",orders
    # print "drones=",drones

    ## all available items
    available = {it: sum([w[it] for w in warehouses]) for it in item_types}
    orders.sort(key = lambda o: o.totalWeight())

    ## remove impossible orders
    to_do = []
    for o in orders:
        if any([it.weight > WMAX for it in o.items]):
            continue
        if all([o[it] <= available[it] for it in o.items]):
            for it in o.items:
                available[it] -= o[it]
            to_do.append(o)

    actions   = []
    simulator = []
    heapify(to_do)
    while to_do != []:
        o          = heappop(to_do)
        d, w, item = get_best_task(o, warehouses, drones)
        quant      =  min(o[item], w[item], d.w_max / item.weight)

        # travel to warehouse and load required item
        actions.append(d.load(w, item, quant))

        # load extra items that fit
        extra = {item: quant}
        while d.weight < d.w_max:
            last_w = d.weight
            for it in o.items:
                if o[it] - extra.get(it,0) > 0 and w[it] > 0 and d.weight + it.weight <= d.w_max:
                    extra[it] = extra.get(it, 0) + 1
                    actions.append( d.load(w, it, 1) )
            if last_w == d.weight:
                break

        # print "extra=",extra

        # travel to order and deliver
        # actions.append(d.deliver(o, item, quant))

        # deliver all items
        for it in extra:
            actions.append(d.deliver(o, it, extra[it]))
        

        if not o.isDone():
            heappush(to_do, o)
        else:
            simulator.append(d.time)
    
    print >> outfile, len(actions)
    for a in actions:
        print >> outfile, a

    score = int(sum([ ceil(float(T-t)/T * 100) for t in simulator]))
    print "SCORE=", score
