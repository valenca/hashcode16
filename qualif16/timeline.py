from heapq import *

class Timeline:
	def __init__(self):
		self.events=[]

	def addEvent(self, event):
		heappush(self.events, event)

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
	def __init__(self,d,t,x,y,a):
		self.time=t
		self.x=x
		self.y=y
		self.drone=d
		self.action=a

	def __str__(self):
		return "[%d] Drone %d at (%d,%d) - %s" % (self.time,self.drone,self.x,self.y,self.action)
	def __repr__(self):
		return self.__str__()

	def __cmp__(self, other):
		return cmp(self.time, other.time)

if __name__ == '__main__':
	q=Timeline()
	q.addEvent(Event(0,0,1,3,"load"))
	q.addEvent(Event(0,0,1,3,"load"))
	q.addEvent(Event(0,0,1,3,"load"))

	q.addEvent(Event(0,1,1,3,"load"))
	q.addEvent(Event(0,1,1,3,"load"))

	q.addEvent(Event(0,2,1,3,"load"))
	q.addEvent(Event(0,2,1,3,"load"))

	while not q.isEmpty():
		print q.nextEvents()
		print ""


