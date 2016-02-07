from operator import itemgetter, attrgetter, methodcaller
from itertools import cycle
from pprint import pprint

R,S,U,P,M=list(map(int,raw_input().split()))

slot=[]
for i in range(U):
	slot.append(list(map(int,raw_input().split())))

servers=[]
for i in range(M):
	servers.append(list(map(float,raw_input().split())))
	servers[i].append(i)
str_slot=list("0"*R*S)

for i in slot:
	str_slot[(i[0]*S)+(i[1])]="1"

r=[]
	
for i in range(R):
	x = "".join(str_slot[i*S:((i+1)*S)])
	r.extend(map(lambda x:[i,len(x)],x.split("1")))

r.sort(key=itemgetter(1),reverse=True)
for i in range(len(r)):
	if r[i][1]==0:
		break
	
r=r[:i]
	
servers.sort(key=lambda(x):x[0]/x[1])

for i in range(len(servers)):
	servers[i].append(i%P)


print len(r)

pool=[]
for i in range(P):
	pool.append([0]*R)

sol=0

#Servers = Size,Capacity,Number,Pool
#Row = Number,Size

for s in servers:
	for row in r:
		if r[1]==s[0]:
			pass
	
for i in range(len(r)):
	if r[i][1]==0:
		break
	
r=r[:i]

print len(r)
