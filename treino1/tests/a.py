b = -1
while(1):
	a = input()
	a = a.split(" ")[1]
	n = int(a)
	if n > b:
		b = n
		print(b)
