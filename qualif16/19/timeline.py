from data import * 
from heapq import *

class Timeline:
	def __init__(self):
		self.events=[]

	def addEvent(self, event):
		heappush(self.events, event)

	def nextEvent(self):
		assert(self.events != [])
		return heappop(self.events)

	def nextEvents(self):
		if self.events == []:
			return []
		cur_time = self.events[0].time
		res = []
		while self.events != [] and self.events[0].time == cur_time:
			res.append( heappop(self.events) )
		return res

	def isEmpty(self):
		return self.events == []

class Event:
	def __init__(self,d,t,a):
		self.time=t
		self.drone=d
		self.action=a

	def __str__(self):
		return "[%d] Drone at (%d,%d) - %s" % (self.time,self.drone.x,self.drone.y,self.action)
	def __repr__(self):
		return self.__str__()

	def __cmp__(self, other):
		return cmp(self.time, other.time)

if __name__ == '__main__':
	q=Timeline()
	d = Drone(0,0,0,100)


	q.addEvent(Event(d,1,"load"))
	q.addEvent(Event(d,0,"load"))
	q.addEvent(Event(d,0,"load"))
	q.addEvent(Event(d,2,"load"))
	q.addEvent(Event(d,2,"load"))
	q.addEvent(Event(d,0,"load"))
	q.addEvent(Event(d,1,"load"))





	while not q.isEmpty():
		print q.nextEvents()
		print ""


