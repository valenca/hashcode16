class Drone():
	item = -1
	quant = 0
	pos= [-1,-1]
	dest= [-1,-1]
	eta=0
	
	def __init__(start):
		self.pos=start


class Warehouse():
	items={}
	pos= [-1,-1]

	def __init__(position,items):
		self.pos=position
		self.items={}

class Order():
	pos=[-1,-1]
	items={}

	def __init__(position,items):
		self.pos=position
		self.items={}


if __name__ == "__main__":
	
