from heapq import *

class Timeline:
	def __init__(self,size):
		self.size=size
		self.slots=[]

	def addEvent(self,event,time):
		heappush(self.slots,(time,event))

	def __str__(self):
		s=""
		for i in range(self.size):
			s += "Slot %d: %d ev.\n" % (i, len(self.slots[i].events))
			for j in range(len(self.slots[i].events)):
				s += "  Event %s\n" % self.slots[i].events[j]
				
		return s
	
class Slot:
	def __init__(self):
		self.events=[]
		self.state=[]

class Event:
	def __init__(self,d,x,y,a):
		self.x=x
		self.y=y
		self.drone=d
		self.action=a

	def __str__(self):
		return "Drone %d at (%d,%d) - %s" % (self.drone,self.x,self.y,self.action)

q=Timeline(4)
q.addEvent(Event(1,3,0,"load"),3)
q.addEvent(Event(1,3,0,"load"),1)
q.addEvent(Event(1,3,0,"load"),2)

