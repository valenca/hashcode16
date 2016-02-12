#!/usr/bin/python2

import math
import sys

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

    def travel(self, newx, newy):
        self.x = newx
        self.y = newy
        return distance(self.x, self.y, newx, newy)

    def nextAction(self, prods, orders, warehouses, needed_items, avail_items, instructions):
        assert(orders != [])

        cnt = 0

        for i, o in enumerate(orders):
            if not o.can_do(prods, avail_items):
                for p in o.items: 
                    needed_items[p.index] -= o.items[p]
                orders.remove(o)

        # get closest oreder
        ordered_o = sorted([(distance(self.x,self.y, o.x, o.y), o) for o in orders])        

        ordered_w = sorted([(distance(self.x,self.y, w.x, w.y), w) for w in warehouses])
        next_w = None
        might_carry = [0] * len(needed_items)
        for dist, w in ordered_w:
            has_items = False
            for item, quant in enumerate(w.items):
                if needed_items[item] > 0 and quant > 0 :
                    has_items = True
                    might_carry[item] += min(quant, needed_items[item])

            if has_items:
                next_w = w
                break

        if next_w == None:
            return float('inf')
        cnt += self.travel(next_w.x, next_w.y)

        cur_weight = 0
        to_carry = [0] * len(needed_items)
        while cur_weight < self.max_weight:
            ind, wgt, qnt = min(filter(lambda (a,b,c): c!=0, [(p.index, p.weight, might_carry[p.index]) for p in prods]))
            cur_weight += wgt
            might_carry[ind] -= 1
            to_carry[ind] += 1


        # print "cur_weight=", cur_weight

        # print "sum(to_carry)=", sum(to_carry)

        for item, quant in enumerate(to_carry):
            if quant != 0:
                avail_items[item]  -= quant
                next_w.items[item] -= quant
                instructions.append( "%d %s %d %d %d" %  (self.index, "L", next_w.index, item, quant) )
                cnt += 1

        for dist, o in ordered_o:
            needs_items = False
            for p in o.items:
                if o.items[p] > 0 and to_carry[p.index] > 0 :
                    needs_items = True
                    qnt = min(o.items[p], to_carry[p.index])
                    to_carry[p.index] -= qnt
                    needed_items[p.index] -= qnt
                    o.items[p] -= qnt
                    instructions.append( "%d %s %d %d %d" %  (self.index, "D", o.index, p.index, qnt) )
                    cnt += 1
            if needs_items:
                cnt += self.travel(o.x, o.y)

        assert(sum(to_carry) == 0)

        for item, quant in enumerate(to_carry):
            avail_items[item] += quant

        return cnt

class Warehouse:
    def __init__(self, index, x, y, items):
        self.index = index
        self.x = x
        self.y = y
        self.items = items

    def __str__(self):
        itms = ["\"" + str(i) + "\":" + str(self.items[i]) for i in range(len(self.items))]
        str_items = ", ".join(itms)
        return ("(id=" + str(self.index) + ",x=" + str(self.x) + 
               ",y=" + str(self.y) + "," + str_items + ")")
    def __repr__(self):
        return self.__str__()

class Order:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y
        self.items={}

    def add_product(self, prod, size=1):
        try:
            self.items[prod] += size
        except KeyError:
            self.items[prod] = size

    def can_do(self, prods, avail_items):
        for item, quant in enumerate(avail_items):
            if prods[item] in self.items:
                if self.items[prods[item]] > quant:
                    return False
        return True

    def is_finished(self):
        for p in self.items:
            if self.items[p] > 0:
                return False
        return True

    def __str__(self):
        itms = ["\"" + str(p.index) + "\":" + str(self.items[p]) for p in self.items]
        str_items = ", ".join(itms)
        return ("(id=" + str(self.index) + ",x=" + str(self.x) + 
                ",y=" + str(self.y) + "," + str_items + ")" )
    def __repr__(self):
        return self.__str__()


class Product:
    def __init__(self, index, weight):
        self.index = index
        self.weight = weight
    
    def __str__(self):
        return "(id=" + str(self.index) + ",w=" + str(self.weight) + ")"
    def __repr__(self):
        return self.__str__()

	
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
    j = 0
    for i in range(C):
        x, y = map(int,raw_input().split())
        orders.append(Order(j,x,y))
        n_prods = input()
        for j in map(int,raw_input().split()):
            orders[-1].add_product(prods[j])
        j += 1

    drones = [Drone(i, warehouses[0].x, warehouses[0].y, PL) for i in range(D)]

    return T, prods, warehouses, orders, drones


if __name__ == "__main__":
    pass
