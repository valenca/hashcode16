# -*- coding: utf-8 -*-

import sys
from data import *
from heapq import * 

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
    O = input()
    orders = []
    for i in range(O):
        x, y   = read_ints()
        nitems = input()
        items = {}
        for t in read_ints():
            items[item_types[t]] = items.get(item_types[t], 0) + 1
        orders.append(Order(i, x, y, items))

    ## drones
    drones = [Drone(i,warehouses[0].x, warehouses[0].y, WMAX) for i in range(D)]

    return item_types, warehouses, orders, drones, WMAX, T, R, C

def get_superorders(orders, range):
    neighbours = {}
    orders.sort(key = lambda o: (o.x, o.y))
    for o in orders:
        neighbours[o] = [n for n in orders 
                            if n != o and distance(o.x,o.y, n.x,n.y) <= range]
    res = []
    while neighbours != {}:
        so = max(neighbours, key = lambda n: len(neighbours[n]))
        neigh = neighbours.pop(so)
        for n in neigh:
            for n2 in neighbours:
                try:
                    neighbours[n2].remove(n)
                except: pass
                try:
                    neighbours[n2].remove(so)
                except: pass
            neighbours.pop(n, None)
        res.append(SuperOrder(so.x, so.y, [so]+neigh))
    return res

def print_map(orders, superorders, warehouses, R, C, output):
    grid = [['-'] * C for r in range(R)]
    for o in orders:
        grid[o.x][o.y] = 'o'
    for so in superorders:
        grid[so.x][so.y] = '⬤'
    for w in warehouses:
        grid[w.x][w.y] = '🏭'
    print >> output, '\n'.join( [''.join(line) for line in grid] )
    output.close()


def solve(orders):
    actions = []
    todo = [(o.totalWeight(), o) for o in orders]
    heapify(todo)
    while todo != []:
        weight_o, o   = heappop(todo)
        d, w, item, _ = o.getEarliestDeliver(warehouses, drones)
        quant         = min(o[item], w[item], d.w_max / item.weight)

        # travel to warehouse and load required item
        actions.append(d.load(w, item, quant))

        # load extra items that fit
        to_carry = {item: quant}
        while d.weight < d.w_max:
            last_w = d.weight
            for it in o.items:
            # for it in sorted(o.items, key=lambda i: i.weight):
                if o[it] - to_carry.get(it,0) > 0 and w[it] > 0:
                    if d.weight + it.weight <= d.w_max:
                        to_carry[it] = to_carry.get(it, 0) + 1
                        actions.append( d.load(w, it, 1) )
            if last_w == d.weight:
                break


        # deliver all items
        for it in to_carry:
            actions.extend(o.deliver(d, it, to_carry[it]))

        if not o.isDone():
            heappush(todo, (o.totalWeight(), o))
    return actions

if __name__ == '__main__':
    if len(sys.argv) > 1:
        outfile = open(sys.argv[1], "w")
    else:
        outfile = sys.stdout

    item_types, warehouses, orders, drones, WMAX, T, R, C = read_input()
    S = Simulator(orders, drones, warehouses, T)

    ## all available items
    available = {it: sum([w[it] for w in warehouses]) for it in item_types}
    orders.sort(key = lambda o: o.totalWeight())

    ## get doable orders
    doable = []
    for o in orders:
        if any([it.weight > WMAX for it in o.items]):
            continue
        if all([o[it] <= available[it] for it in o.items]):
            for it in o.items:
                available[it] -= o[it]
            doable.append(o)

    ## normal orders
    # actions = solve(doable)

    ## super orders
    superorders = get_superorders(doable, 13)
    actions = solve(superorders)
    # print_map(orders, super_todo, warehouses, R, C, open("map.txt","w"))
    
    print >> outfile, len(actions)
    for a in actions:
        print >> outfile, a
        S.execute(a)

    print "SCORE=", S.score()
