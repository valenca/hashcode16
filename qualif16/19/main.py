from timeline import *
from data import *

# class Act

# class Action:
#     def __init__(self, drone, tag, warehouse, prod, quant):
#         self.drone = drone
#         self.tag = tag
#         self.warehouse = warehouse
#         self.prod = prod
#         self.quant = quant

#     def __str__(self):
#         return self.drone.index + " " + self.tag + " " + self.index + " "
        # if self.tag == ""

# class Agent:
#     def __init__(self):
#         self.x = x
#         self.y = y

#     def nextAction(self):
#         pass

if __name__ == '__main__':
    T, prods, warehouses, orders, drones = read_input()
    q = Timeline()
    for d in drones:
        q.addEvent( Event(d, 0, "avail") )

    avail_items = warehouses[0].items

    while not q.isEmpty():
        event = q.nextEvent()
        if event.time > T:
            break



        d = event.drone
        next_time = d.nextAction(orders)
        q.addEvent(Event(d, next_time, ""))


        print event
