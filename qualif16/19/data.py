#!/usr/bin/python2

class Drone:
    def __init__(self, x, y, PL):
        self.x = x
        self.y = y
        self.max_weight = PL
        self.items={}

    def load_product(self, prod, size):
        try:
            self.items[prod] += size
        except KeyError:
            self.items[prod] = size


class Warehouse:
    def __init__(self, x, y, items):
        self.x = x
        self.y = y
        self.items = items

class Order:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.items={}

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
    for _ in range(W):
        x,y = map(int,raw_input().split())
        items = map(int,raw_input().split())
        warehouses.append(Warehouse(x,y,items))

    C = input()
    orders = []
    for i in range(C):
        x, y = map(int,raw_input().split())
        orders.append(Order(x,y))
        n_prods = input()
        for j in map(int,raw_input().split()):
            orders[-1].add_product(prods[j])

    drones = [Drone(warehouses[0].x, warehouses[0].y, PL) for _ in range(D)]

    return T, prods, warehouses, orders, drones


if __name__ == "__main__":
    read_input()
