# -*- coding: utf-8 -*-
import random
import numpy as np

""" 
    Naive greedy solution:
       - order servers by decreasing ratio of capacity/size
       - for each s in servers:
          - get row r with lowest sum of capacities so far on which s fits
          - assign r to smallest 'subrow' in r
          - assign a random pool to s
"""

class Server:
    def __init__(self, id, size, capacity):
        self.id       = id
        self.size     = size
        self.capacity = capacity

    def ratio(self):
        return float(self.capacity) / self.size

    def __str__(self):
        return ("server(" + str(self.id) + ","
                          + str(self.size) + "," + str(self.capacity) + ")")
    def __repr__(self):
        return self.__str__()

class Row:
    def __init__(self, id, subrows, value):
        self.id            = id
        self.subrows       = subrows
        self.value         = value

    def get_best_subrow(self, server):
        """ returns subrow with least size for server 'server' """
        best = None                 # best subrow
        best_size = float('inf')    # size of best subrow
        for sr in self.subrows:
            if sr.size - sr.occupied_size >= server.size:
                if best_size > sr.size - sr.occupied_size:
                    best_size = sr.size - sr.occupied_size
                    best = sr
        return best

    def __cmp__(self, other):
        if other == None:
            return 1
        return cmp(self.value, other.value)
    def __str__(self):
        return str(self.subrows)
    def __repr__(self):
        return self.__str__()

class SubRow:
    def __init__(self, size, occupied_size, position):
        self.size          = size
        self.occupied_size = occupied_size
        self.position      = position

    def next_free_slot(self):
        return self.position + self.occupied_size

    def assign(self, server):
        self.occupied_size += server.size

    def __str__(self):
        return (("x" * self.occupied_size) +
                ("-" * (self.size - self.occupied_size)))
    def __repr__(self):
        return self.__str__()

class Assignment:    # assignment of servers
    def __init__(self, server, pool_id, row_id, slot):
        self.server  = server
        self.pool_id = pool_id
        self.row_id  = row_id
        self.slot    = slot

    def is_valid(self):
        return self.row_id != -1

    def set_pool_id(self, pid):
        self.pool_id = pid

    def __str__(self):
        if self.is_valid():
            return (str(self.row_id) + " " +
                    str(self.slot)   + " " +
                    str(self.pool_id) )
        return "x"
    def __repr__(self):
        return self.__str__()

def load_grid():
    grid = [Row(i,[SubRow(S, 0, 0)],0) for i in xrange(R)]
    for u in xrange(U):
        r, s = [int(x) for x in raw_input().split()]
        for i in xrange(len(grid[r].subrows)):
            old = grid[r].subrows[i]
            if (old.position <= s and s <= old.position + old.size - 1):
                new = []
                if old.position < s:
                    new.append( SubRow(s - old.position, 0, old.position))
                if old.position + old.size - 1 > s:
                    new.append( SubRow(old.position + old.size -1 -s, 0, s + 1))
                grid[r].subrows = grid[r].subrows[:i]+new+ grid[r].subrows[i+1:]
                break
    return grid

def load_servers():
    servers = [Server(0,0,0) for _ in range(M)]
    for i in xrange(M):
        s, c  = [int(x) for x in raw_input().split()]
        servers[i] = Server(i,s,c)
    return servers

def get_best_assign(server, choose_pool_fn):
    """ returns assignment to row with least value where server fits """
    global grid, servers
    best_row    = None
    best_subrow = None
    for r in grid:
        sr = r.get_best_subrow(server)
        if sr != None:
            if (best_row == None) or (r.value < best_row.value):
                best_row    = r
                best_subrow = sr

    if best_row != None:
        slot = best_subrow.next_free_slot()
        best_subrow.assign(server)
        best_row.value += server.capacity
        return Assignment(server, choose_pool_fn(), best_row.id, slot)
    return Assignment(server, -1, -1, -1)

def get_pool_uniform():
    """ returns totally random pool id """
    return random.randint(0, P-1)

def get_pool_roulette(pool_capacities):
    """ returns pool id based on roulette wheel selection """
    assert(len(pool_capacities) > 0)

    inv_pl_capacities = [1.0 / c for c in pool_capacities]
    acum = inv_pl_capacities[0]
    x = random.uniform(0, sum(inv_pl_capacities))
    for pool_id in xrange(len(inv_pl_capacities)):
        if x <= acum:
            return pool_id
        acum += inv_pl_capacities[pool_id+1]
    assert(False)  # should never reach this point

def get_pool_cycle(srv_counter):
    """ cycles over all pools in the same order """
    return srv_counter % P

def get_pool_mincap(pool_capacities):
    """ returns pool with minmum capacity """
    return min(zip(pool_capacities, range(len(pool_capacities))))[1]

def get_pool_none():
    return -1

def solve():
    """ TODO: use ordered set to store rows """
    global grid, servers
    result = [Assignment(i,-1,-1,-1) for i in xrange(M)]

    # assign an equal *positive* capacity for all pools
    # pool_capacities = [1] * P
    # pool_capacities = [0] * P
    # counter = 0
    servers.sort(key = lambda s : (-s.ratio(), s.size)  )
    for s in servers:
        ### get random pool ###
        # result[s.id] = get_best_assign(s, get_pool_uniform)

        ### get random pool based on roulette wheel selection ###
        # result[s.id] = get_best_assign(s, lambda : 
        #                                     get_pool_roulette(pool_capacities))
        # pool_capacities[result[s.id].pool_id] += s.capacity
        
        ### cycle over all pools ###
        # result[s.id] = get_best_assign(s, lambda: get_pool_cycle(counter))
        # counter += 1
        
        ### return pool with least capacity every time ###
        # result[s.id] = get_best_assign(s, lambda: get_pool_mincap(pool_capacities))
        # pool_capacities[result[s.id].pool_id] += s.capacity

        ### assign pools when all servers all assigned ###
        result[s.id] = get_best_assign(s, get_pool_none)

    ### assign pools when all servers are assigned ###
    pool_capacities = [0] * P
    servers_by_row = [[] for i in xrange(R)]
    for assign in result:
        servers_by_row[assign.row_id].append( assign.server )
    for r in xrange(R):
        for s in servers_by_row[r]:
            pid = get_pool_mincap(pool_capacities)
            result[s.id].set_pool_id( pid ) 
            pool_capacities[pid] += s.capacity


    return result

def compute_score(assignments):
    pool_capacities = [[0] * R for j in xrange(P)]
    GC = [0] * P   # guaranteed capacities for all pools
    for a in assignments:
        if a.is_valid():
            pool_capacities[a.pool_id][a.row_id] += a.server.capacity
    for p in xrange(P):
        total = sum(pool_capacities[p])
        GC[p] = min( [total - x for x in pool_capacities[p] ] )
    return min(GC)

def print_stats(assignments):
    pool_capacities = [[0] * R for j in xrange(P)]
    row_capacities  = [0] * R

    num_servers = 0
    for a in assignments:
        if a.is_valid():
            num_servers += 1
            row_capacities[a.row_id] += a.server.capacity
            pool_capacities[a.pool_id][a.row_id] += a.server.capacity

    print 'STATISTICS:'
    print '% assigned servers=', float(num_servers) / M * 100
    print u'Stand. deviation rows ∑capacities=',  np.std(row_capacities)
    # print u'Maximum row ∑capacities=', max(row_capacities)
    # print u'Minimum row ∑capacities=', min(row_capacities)
    print u'Stand. deviation pools ∑capacities=', np.std(
                                            [sum(x) for x in pool_capacities])
    pl_worse_cap_frac = [ max([float(c) / sum(pc) * 100 for c in pc ])
                                for pc in pool_capacities ]
    print u'Average worse %pool_row_cap/pool_total_cap=', np.average(
                                                pl_worse_cap_frac), '%'


if __name__ == '__main__':
    R, S, U, P, M = [int(x) for x in raw_input().split()]
    grid    = load_grid()
    servers = load_servers()
    assignments = solve()
    for a in assignments:
        print a

    print '\nSCORE=', compute_score(assignments), '\n'
    print_stats(assignments)