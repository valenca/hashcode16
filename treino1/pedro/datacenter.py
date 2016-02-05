from heapq import *

class Assignment:
    # assignment of servers
    def __init__(self, server_id, pool_id, row_id, slot):
        self.server_id = server_id
        self.pool_id   = pool_id
        self.row_id    = row_id
        self.slot      = slot
    def __str__(self):
        if self.row_id != -1:
            return ("Server " + str(self.server_id) +
                    " placed in row " + str(self.row_id) +
                    " at slot " + str(self.slot) +
                    " and assigned to pool " + str(self.pool_id))
        return "Server " + str(self.server_id) + " x"
    def __repr__(self):
        return self.__str__()

class Server:
    def __init__(self, id, size, capacity):
        self.id       = id
        self.size     = size
        self.capacity = capacity
    def __str__(self):
        return "server(" + str(self.size) + "," + str(self.capacity) + ")"
    def __repr__(self):
        return self.__str__()
    def ratio(self):
        return float(self.capacity) / self.size

class Row:
    def __init__(self, id, size, position, occupied_size, value):
        self.id            = id
        self.size          = size
        self.occupied_size = occupied_size
        self.value         = value
    def __str__(self):
        return ("row(" + str(self.size) + "," + str(self.original_row) + ","  
                + str(self.value) + ")")
    def __repr__(self):
        return self.__str__()
    def __cmp__(self, other):
        return cmp(self.value, other.value)        


def solve_greedy(servers, rows):
    # sort servers
    q_servers = servers[:]
    q_servers.sort(key = lambda s : -s.ratio())

    # greedy assign
    assignments = [Assignment(i,-1,-1,-1) for i in xrange(len(servers))]

    while q_servers != [] and rows != []:
        s = q_servers.pop(0)
        r = heappop(rows)
        if r.size >= s.size:
            heappush(rows, Row(r.id,
                               r.size - s.size,
                               r.position,
                               r.occupied_size + s.size,
                               r.value + s.capacity))
            assignments[s.id] = Assignment(s.id, -1, r.id, r.occupied_size)
        else:
            heappush(rows, r)
            # left.append(s)

    # left.extend(q_servers)

    # print "rows=", rows
    # print "q_servers=", q_servers
    # print "assignments=", assignments
    return assignments


if __name__ == '__main__':
    R, S, U, P, M = [int(x) for x in raw_input().split()]

    # read xslots
    xslots = ['-'*S for x in xrange(R)]
    for i in xrange(U):
        r, s = [int(x) for x in raw_input().split()]
        xslots[r] = xslots[r][:s] + 'x' + xslots[r][s+1:]

    # read servers
    servers = [Server(0,0,0) for _ in range(M)]
    for i in xrange(M):
        s, c  = [int(x) for x in raw_input().split()]
        servers[i] = Server(i,s,c)

    # order servers
    # servers.sort(key = lambda srv : -srv.ratio())

    # split rows into a heap ordered increasing by sum of capacities
    rows = []
    for i in xrange(len(xslots)):
        print "xslots[i]=", xslots[i]
        sizes     = [ len(_) for _ in xslots[i].split('x') if _ != '']

        j = 0
        while j < len(xslots[i]) and xslots[i][j] == 'x':
            j+= 1
        positions = []
        while j < len(xslots[i]):
            positions.append(j)
            while j < len(xslots[i]) and xslots[i][j] != 'x':
                j += 1
            while j < len(xslots[i]) and xslots[i][j] == 'x':
                j += 1
        print positions

        xpos = [j for j in range(len(xslots[i])) if xslots[i][j] == 'x']
        s = 'x' + xslots[i]
        to_remove

        xpos = 

        print sizes

    #     for row_size in :
    #         rows.append( Row(i, row_size, 0, 0) )
    # heapify(rows)

    # print 'ASSIGNMENTS: '
    # for assign in solve_greedy(servers, rows):
    #     print assign