s = 9
v = [[0,3], [1,1], [1,2], [1,3], [2,1], [2,3], [3,1], [3,2], [3,3], [4,1]]
#v = [[0,1], [0,2], [0,3], [0,4], [1,1], [1,2], [1,3], [1,4], [2,1], [2,2], [2,4], [3,1], [3,2], [3,3], [3,4]]
#v = [[0,0], [1,0], [4, 0], [5,0], [7,0]]
t = s*s

m = [[0]*s for i in range(s)]

for r,c in v:
	m[r][c] = 1
	#print(r,c)

#for i in range(s):
#	print(str(m[i]))

fit = []
# paint all > erase after
aux = t - len(v) + 1
fit += [[aux, 0]]
fit += [[len(v), 3]]

rBounds = [[s, -1]] * s

for i in range(s):
	init = s
	end = -1
	for j in range(s):
		if m[i][j] == 1:
			if init > j:
				init = j
			if end < j:
				end = j
	rBounds[i] = [init, end]

cBounds = [[s, -1]] * s
for j in range(s):
	init = s
	end = -1
	for i in range(s):
		if m[i][j] == 1:
			if init > i:
				init = i
			if end < i:
				end = i
	cBounds[j] = [init, end]

#print(rBounds)
#print(cBounds)

# paint row
aux = 0
for i in range(s):
	x,y = rBounds[i]
	if y != -1:
		aux += y-x+1 - sum(m[i][x:y+1]) + 1

#print(aux)
fit += [[aux, 1]]

# paint small row
#print(rBounds)
rSplits = []
aux = 0
for i in range(s):
	x,y = rBounds[i]
	if y != -1:
		b = -1
		e = -1
		for j in range(x, y+1):
			if m[i][j] == 0:
				if b != -1:
					rSplits += [[i, b, i, e]]
					b = -1
			else:
				if b == -1:
					b = j
				e = j
		if b != -1:
			rSplits += [[i, b, i, e]]

#print(rSplits)
fit += [[len(rSplits), 4]]

# paint col
aux = 0
for j in range(s):
	x,y = cBounds[j]
	if y != -1:
		tmp = 0
		for i in range(x, y+1):
			tmp += m[i][j]
		aux += y-x+1 - tmp + 1

#print(aux)

fit += [[aux, 2]]

# paint small col
#print(cBounds)
cSplits = []
aux = 0
for j in range(s):
	x,y = cBounds[j]
	if y != -1:
		b = -1
		e = -1
		for i in range(x, y+1):
			if m[i][j] == 0:
				if b != -1:
					cSplits += [[b, j, e, j]]
					b = -1
			else:
				if b == -1:
					b = i
				e = i
		if b != -1:
			cSplits += [[b, j, e, j]]

#print(cSplits)
fit += [[len(cSplits), 5]]


fit.sort()

#print(fit)

if fit[0][1] == 0:
	print("PAINT_SQUARE %d %d %d" % (s/2, s/2, s/2))
	for i in range(s):
		for j in range(s):
			print("ERASE_CELL %d %d" % (i,j))
elif fit[0][1] == 1:
	for i in range(s):
		x,y = rBounds[i]
		if y != -1:
			print("PAINT_LINE %d %d %d %d" % (i, x, i, y))
			for j in range(x, y+1):
				if m[i][j] == 0:
					print("ERASE_CELL %d %d" % (i,j))
elif fit[0][1] == 2:
	for j in range(s):
		x,y = cBounds[j]
		if y != -1:
			print("PAINT_LINE %d %d %d %d" % (x, j, y, j))
			for i in range(x, y+1):
				if m[i][j] == 0:
					print("ERASE_CELL %d %d" % (i,j))
elif fit[0][1] == 3:
	for r,c in v:
		print("PAINT_LINE %d %d %d %d" % (r, c, r, c))
elif fit[0][1] == 4:
	for a,b,c,d in rSplits:
		print("PAINT_LINE %d %d %d %d" % (a, b, c, d))
elif fit[0][1] == 5:
	for a,b,c,d in cSplits:
		print("PAINT_LINE %d %d %d %d" % (a, b, c, d))


