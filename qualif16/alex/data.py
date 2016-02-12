#!/usr/bin/python2

import math

def distance(x1,y1,x2,y2):
    return math.ceil( (abs(x1-x2) + abs(y1-y2))**0.5 )

class Drone:
    def __init__(self, index, x, y, PL):
        self.index = index
        self.x = x
        self.y = y
        self.max_weight = PL
        self.items={}

    def load_product(self, prod, size):
        try:
            self.items[prod] += size
        except KeyError:
            self.items[prod] = size

    def nextAction(self, orders):
        assert(orders != [])

        next_order = orders[0]
        best_dist  = dist(next_order.x, next_order.y, self.x, self.y)
        for o in orders[1:]:
            d = dist(o.x, o.y, self.x, self.y)
            if d < best_dist:
                best_dist = d
                next_order = o


        print len(orders)
        return 1000000


class Warehouse:
    def __init__(self, index, x, y, items):
        self.index = index
        self.x = x
        self.y = y
        self.items = items

class Order:

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.items={}


    def total_weight(self):
        t = 0
        for it in self.items:
            t += (it.weight * self.items[it])
        return t

    def n_items(self):
        t = 0
        for it in self.items:
            t += self.items[it]
        return t

    def dif_items(self):
        return len(self.items.keys())

    def add_product(self, prod, size=1):
        try:
            self.items[prod] += size
        except KeyError:
            self.items[prod] = size

class Product:
    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
	
def read_input():
    n_rows,n_cols,D,T,PL = map(int,raw_input().split())
    
    P = input()
    i = raw_input().split()
    prods = []
    for j in range(len(i)):
        prods.append(Product(j,int(i[j])))
    
    W = input()
    warehouses = []
    i = 0
    for _ in range(W):
        x,y = map(int,raw_input().split())
        items = map(int,raw_input().split())
        warehouses.append(Warehouse(i,x,y,items))
        i += 1

    C = input()
    orders = []
    for i in range(C):
        x, y = map(int,raw_input().split())
        orders.append(Order(x,y,i))
        n_prods = input()
        for j in map(int,raw_input().split()):
            orders[-1].add_product(prods[j])

    drones = [Drone(i, warehouses[0].x, warehouses[0].y, PL) for i in range(D)]

    return T, prods, warehouses, orders, drones, n_rows, n_cols


if __name__ == "__main__":
    read_input()
