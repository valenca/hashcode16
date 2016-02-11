class Drone():
	item = -1
	quant = 0
	eta=0
	
	def __init__(self,start):
		self.pos=start


class Warehouse():
	items={}
	pos= [-1,-1]

	def __init__(self,position,items):
		self.pos=position
		self.items={}

class Order():
	pos=[-1,-1]
	items={}

	def __init__(self,position,items):
		self.pos=position
		self.items={}

class Product:
	def __init__(self,weight):
		self.weight=weight
	
		
if __name__ == "__main__":
	n_rows,n_cols,D,T,PL = map(int,raw_input().split())
	P = input()
	prods = [Product(int(w)) for w in raw_input().split()]
	W = input()	
	prods = [Product(int(w)) for w in raw_input().split()]
		
		
	
	print n_rows,n_cols,D,T,PL
	print P 
	print prods
