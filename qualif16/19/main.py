import timeline
import data

class Agent:
    def __init__(self):
        self.x = x
        self.y = y

    def nextAction(self):
        pass

if __name__ == '__main__':
    T, prods, warehouses, orders, drones = data.read_input()

    q = timeline.Timeline()

    while not q.isEmpty():
        event = q.nextEvent()
