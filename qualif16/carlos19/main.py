from timeline import *
from data import *

if __name__ == '__main__':
    outfile = open("out", "w")
    T, prods, warehouses, orders, drones = read_input()
    q = Timeline()
    for d in drones:
        q.addEvent( Event(d, 0, "avail") )

    avail_items = warehouses[0].items[:]
    for w in warehouses[1:]:
        for i in range(len(w.items)):
            avail_items[i] += w.items[i]

    needed_items = [0] * len(prods)
    for o in orders:
        for i in o.items:
            needed_items[i.index] += o.items[i]

    instructions = []

    print "warehouses=", warehouses
    print "prods=", prods


    while not q.isEmpty() and orders != [] :
        # print "orders=", orders
        # print "needed_items=", needed_items
        # print "avail_items=", avail_items
        # print "len(instructions)=", len(instructions)
        # print "len(orders)=", len(orders)


        # print "len(orders)=", len(orders)

        event = q.nextEvent()
        if event.time > T:
            break

        d = event.drone
        print "drone=", d.index
        next_time = event.time + d.nextAction(prods, orders, warehouses, needed_items, avail_items, instructions)
        print "next_time=", next_time
        q.addEvent(Event(d, next_time, ""))

        orders = filter(lambda o: not o.is_finished(), orders)

        print ""
    

    print len(instructions)
    for inst in instructions:
        print inst