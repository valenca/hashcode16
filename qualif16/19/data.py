#!/usr/bin/python2

import math
import sys

def distance(x1,y1,x2,y2):
    return int(math.ceil( ( (x1-x2)**2 + (y1-y2)**2)**0.5 ))

class ItemType:
    def __init__(self, index, weight):
        self.index  = index
        self.weight = weight

    def __str__(self):
        return "(" + str(self.index) + ",w="+ str(self.weight) + ")"
    def __repr__(self):
        return self.__str__()

class Inventory(object):
    def __init__(self, index, x, y, items):
        self.index = index
        self.x     = x
        self.y     = y
        self.items = items 

    def __getitem__(self,i):
        return self.items.get(i,0)
    def __setitem__(self,i,x):
        return self.items.__setitem__(i,x)
    def __str__(self):
        return "(%d,%d)%s" % (self.x, self.y, str(self.items))
    def __repr__(self):
        return self.__str__()

class Warehouse(Inventory):
    def __init__(self, index, x, y, items):
        super(self.__class__, self).__init__(index, x, y, items)
        self.orders = []

    def load(self, item, quant):
        assert(self[item] >= quant)
        self[item] -= quant
        if self[item] == 0:
            self.items.pop(item)

class Order(Inventory):
    def __init__(self, index, x, y, items):
        super(self.__class__, self).__init__(index, x, y, items)
        # self.warehouses = warehouses[:]
        # self.warehouses.sort(key=lambda w:distance(self.x,self.y, w.x,w.y))

    def deliver(self, drone, item, quant):
        assert(self[item] >= quant)
        drone.travel(self.x, self.y)
        # drop items
        self[item] -= quant
        if self[item] == 0:
            self.items.pop(item)
        drone.deliver(item, quant)
        return [ActionD(drone, item, quant, self)]

    def totalWeight(self):
        return sum([item.weight * quant for (item,quant) in self.items.items()])

    def isDone(self):
        return all([quant == 0 for quant in self.items.values()])

    def getEarliestDeliver(self, warehouses, drones):
        earliest = float('inf')
        # for it in sorted(self.items, key=lambda i: -i.weight):
        for it in self.items:
            if self.items[it] > 0:
                for w in warehouses:
                    if w[it] > 0:
                        ow_dist = distance(w.x,w.y, self.x,self.y)
                        for d in drones:
                            next = d.time + distance(d.x,d.y, w.x,w.y) + ow_dist
                            if next < earliest:
                                best_d    = d
                                best_w    = w
                                best_it   = it
                                earliest = next
        return (best_d, best_w, best_it, earliest)

class SuperOrder(Inventory):
    def __init__(self, x, y, orders):
        items = {}
        for o in orders:
            for it in o.items:
                items[it] = items.get(it, 0) + o[it]        
        super(self.__class__, self).__init__(-1, x, y, items)
        self.orders = orders

    def isDone(self):
        return all([o.isDone() for o in self.orders])

    def totalWeight(self):
        return sum([o.totalWeight() for o in self.orders])

    def getEarliestDeliver(self, warehouses, drones):
        earliest = float('inf')
        for o in filter(lambda o: not o.isDone(), self.orders):
            d, w, item, next = o.getEarliestDeliver(warehouses, drones)
            if next < earliest:
                best_d = d
                best_w = w
                best_it = item
                earliest = next
        return (best_d, best_w, best_it, earliest)

    def deliver(self, drone, item, quant):
        assert(self[item] >= quant)

        actions = []
        for o in self.orders:
            if quant <= 0:
                break
            if o[item] > 0:
                qnt = min(o[item], quant)
                self.items[item] -= qnt
                if self.items[item] == 0:
                    self.items.pop(item)
                actions.extend(o.deliver(drone, item, qnt))
                quant -= qnt
        return actions

class Drone:
    def __init__(self, index, x, y, w_max):
        self.index  = index
        self.x      = x
        self.y      = y
        self.time   = 0
        self.w_max  = w_max
        self.weight = 0

    def load(self, warehouse, item, quant):
        assert(item.weight * quant <= self.w_max) 
        self.travel(warehouse.x, warehouse.y)
        self.time += 1
        self.weight += item.weight * quant 
        warehouse.load(item, quant)
        return ActionL(self, item, quant, warehouse)

    def deliver(self, item, quant):
        self.time += 1
        self.weight -= item.weight * quant

    def travel(self, newx, newy):
        dist   = distance(self.x,self.y, newx, newy)
        self.x = newx
        self.y = newy
        self.time += dist
        return dist

    def __str__(self):
        return "t=%d(%d,%d)" % (self.time, self.x, self.y)
    def __repr__(self):
        return self.__str__()

class Action(object):
    def __init__(self, drone, item_type, quant):
        self.drone     = drone
        self.quant     = quant
        self.item_type = item_type

class ActionL(Action):
    def __init__(self, drone, item_type, quant, warehouse):
        super(self.__class__, self).__init__(drone, item_type, quant)
        self.warehouse = warehouse

    def __str__(self):
        return ("%d L %d %d %d" % (self.drone.index, self.warehouse.index,
                                   self.item_type.index, self.quant))

class ActionD(Action):
    def __init__(self, drone, item_type, quant, order):
        super(self.__class__, self).__init__(drone, item_type, quant)
        self.order = order

    def __str__(self):
        return ("%d D %d %d %d" % (self.drone.index, self.order.index,
                                   self.item_type.index, self.quant))

class Simulator:
    def __init__(self, orders, drones, warehouses, T):
        self.T      = T
        self.orders = [Order(o.index, o.x, o.y, {k:v for k,v in o.items.items()}) for o in orders]
        self.drones = [Drone(d.index, d.x, d.y, d.w_max) for d in drones]
        self.warehouses = [Warehouse(w.index, d.x, d.y, {k:v for k,v in w.items.items()}) for w in warehouses]
        self.orders_time = {o: float('-inf') for o in self.orders}
        self.finishing = []

    def execute(self, action):
        if isinstance(action, ActionD):
            o = self.orders[action.order.index]
            d = self.drones[action.drone.index]
            o.deliver(d, action.item_type, action.quant)
            self.orders_time[o] = max(self.orders_time[o], d.time)
            if o.isDone():
                self.finishing.append(self.orders_time[o])

        elif isinstance(action, ActionL):
            w = self.warehouses[action.warehouse.index]
            d = self.drones[action.drone.index]
            d.load(w, action.item_type, action.quant)

    def score(self):
        return int(sum([math.ceil(float(self.T-t)/self.T * 100) \
                        for t in self.finishing]))
