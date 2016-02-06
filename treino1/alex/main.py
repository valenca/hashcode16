#!/usr/bin/python2

from operator import attrgetter
from itertools import cycle
#from __future__ import print_function

class Pool:
    def __init__(self,index):
        self.index = index
        self.total_capacity = 0
        self.max_capacity = 0
        self.servers = []
        self.current_server = -1

    def score(self):
        return self.total_capacity - self.max_capacity

    def add_server(self, server):
        self.servers.append(server)

    def next_server(self):
        if self.current_server == len(self.servers):
            return None

        self.current_server += 1
        if self.current_server == len(self.servers):
            return None

        return self.servers[self.current_server]

class Server:
    def __init__(self,index,size,capacity):
        self.index = index
        self.size = size
        self.capacity = capacity
        self.pool = None
        self.row = -1
        self.slot = -1
        
    def __str__(self):
        return "Server: size(%d) capacity(%d) row(%d) slot(%d)" % (self.size,self.capacity,self.row,self.slot)

    def __repr__(self):
        return self.__str__()+"\n"

class Slot:
    def __init__(self,index,unavailable=False,server=None):
        self.index = index
        self.unavailable = unavailable
        self.server = server

    def __str__(self):
        if self.unavailable:
            return "U"
        elif self.server == None:
            return "."
        else:
            return str(s.server.index)

class Row:
    def __init__(self,index,size):
        self.index = index
        self.size = size
        self.slots = [Slot(i) for i in range(size)]

    def __str__(self):
        sr = ""
        for s in self.slots:
            sr = sr + str(s)
        return sr

    def __repr__(self):
        return self.__str__()

class Grid:
    def __init__(self,size,rows_size):
        self.size = size
        self.rows = [Row(i,rows_size) for i in range(size)]

    def __str__(self):
        sr = ""
        for r in self.rows:
            sr = sr + str(r) + "\n"
        return sr

if __name__ == "__main__":
    R,S,U,P,M=list(map(int,input().split()))

    global grid 
    global servers

    grid = Grid(R,S)
    servers = []
    pools = [Pool(i) for i in range(P)]

    for _ in range(U):
        r,s = list(map(int,input().split()))
        grid.rows[r].slots[s].unavailable = True

    for i in range(M):
        s,c = list(map(int,input().split()))
        servers.append(Server(i,s,c))

    servers_by_ratio    = sorted(servers, key=lambda server: server.capacity/server.size)
    servers_by_size     = sorted(servers, key=lambda server: server.size)
    servers_by_capacity = sorted(servers, key=lambda server: server.capacity)

    for s in servers_by_capacity:
        pools.sort(key=attrgetter("total_capacity"))
        pools[0].add_server(s)
        s.pool = pools[0]
        pools[0].total_capacity += s.capacity

    p = 0
    c = 0
    while True:
        server = pools[p].next_server()
        if server != None:
            for r in grid.rows:
                put = False
                for s in range(len(r.slots)):
                    if len(r.slots[s:s+server.size]) < server.size:
                        break

                    put = True
                    for a in r.slots[s:s+server.size]:
                        if a.unavailable or a.server != None:
                            put = False
                            break
                    if put:
                        server.row = r.index
                        server.slot = s
                        for a in r.slots[s:s+server.size]:
                            a.server = server
                        break
                if put:
                    c = c + 1
                    break
        if c == 0:
            break
        p = p + 1
        if p == len(pools):
            c = 0
            p = 0
    
    """pi = [[0]*P for _ in range(R)]
    for s in servers:
        if s.row != -1:
            pi[s.row][s.pool.index] += s.capacity

    for r in pi:
        print(r)
        print()
        print()
    """
            
    for s in servers:
        if s.row == -1:
            print("x")
        else:
            print("%d %d %d" % (s.row, s.slot, s.pool.index))
    
