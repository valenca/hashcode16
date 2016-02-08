import util

read_integers = lambda: [int(x) for x in raw_input().split()]
read_pairs    = lambda: (lambda l: zip(l[::2],l[1::2]))(read_integers())

R, C, A    = read_integers()
L, V, B, T = read_integers()
r0, c0     = read_integers()
targets    = [read_integers() for _ in xrange(L)]
wind       = [[read_pairs() for r in xrange(R)] for a in xrange(A)]

