# -*- coding: utf-8 -*-

def print_wind(wind_grid):
    for alt in wind_grid:
        for row in alt:
            print ''.join(row)
        print ''

def print_wind_dir(wind_grid):
    norm = lambda p: (p.x/abs(p.x) if p.x!=0 else 0,
                      p.y/abs(p.y) if p.y!=0 else 0)
    d = { (0,1):'→', (0,-1):'←', (1,0):'↓', (-1,0):'↑', 
          (1,1):'↘', (-1,-1):'↖', (-1,1):'↗', (1,-1):'↙'}

    for i, altitude in enumerate(wind_grid):
        print 'Altitute', i
        for row in altitude:
            print ''.join([d[norm(c)] for c in row])
        print ''

def print_targets(R, C, targets):
    res = [list('-'*C) for _ in xrange(R)]
    for t in targets:
        res[t.x][t.y] = 'X'
    for line in res:
        print "".join(line)

def print_clusters(R, C, targets, clusters):
    res = [list('-'*C) for _ in xrange(R)]
    for t in targets:
        res[t.x][t.y] = 'X'
    for c in clusters:
        res[c.x][c.y] = '⬤'
    for line in res:
        print "".join(line)