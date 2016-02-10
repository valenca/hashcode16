#!/usr/bin/python

from operator import attrgetter
from itertools import cycle
import numpy as np
import sys

class Pool:
    def __init__(self,index):
        self.index = index
        self.servers = []
        self.current_server = -1
        self.total_capacity = 0

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

    @property
    def ratio(self):
        return self.capacity/self.size

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

def create_data():
    global R, S, U, P, M
    global grid
    global servers
    global pools

    R,S,U,P,M=list(map(int,input().split()))

    grid = Grid(R,S)
    servers = []
    pools = [Pool(i) for i in range(P)]

    for _ in range(U):
        r,s = list(map(int,input().split()))
        grid.rows[r].slots[s].unavailable = True

    for i in range(M):
        s,c = list(map(int,input().split()))
        servers.append(Server(i,s,c))

def sort_servers():
    global servers
    servers.sort(reverse=True, key=lambda server: server.ratio)
    #servers.sort(reverse=True, key=lambda server: server.capacity)

def servers_to_pools():
    global servers
    global pools
    
    for s in servers:
        pools.sort(key=attrgetter("total_capacity"))
        pools[0].add_server(s)
        s.pool = pools[0]
        pools[0].total_capacity += s.capacity

def print_output():
    for s in sorted(servers, key=lambda server:server.index):
        if s.row == -1:
            print("x")
        else:
            print("%d %d %d" % (s.row, s.slot, s.pool.index))

def servers_to_slots():
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


if __name__ == "__main__":
    global R, S, U, P, M
    global grid
    global servers
    global pools

    create_data()

    sort_servers()

    servers_to_pools()
    for p in pools:
        print(p.total_capacity, file=sys.stderr)
        for s in p.servers:
            print("%d/%d" % (s.size, s.capacity), end=" ", file=sys.stderr)
        print(file=sys.stderr)

    servers_to_slots()
    
    print_output()

