matrix=[[0,1,0,0,0],
		[0,1,0,0,0],
		[0,1,1,1,1],
		[0,0,0,1,1],
		[0,1,0,1,1]
]


def flood(x,y):
	l=[]
	if (-1 < x < 5) and (-1 < y < 5):
		if(matrix[x][y]==1):
			matrix[x][y]=0
			l.extend((x,y))
			l.extend(flood(x,y+1))
			l.extend(flood(x+1,y))
			l.extend(flood(x-1,y))
			l.extend(flood(x,y-1))
		return l
		
for i in range(5):
	for j in range(5):
		if matrix[i][j]==1:
			print flood(i,j)
