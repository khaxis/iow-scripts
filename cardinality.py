#!/usr/bin/env python

import sys
from collections import defaultdict

d = defaultdict(set)
N = 0
for l in sys.stdin:
	line = l.rstrip("\n").split("\t")
	for i in range(0, len(line)):
		d[i].add(line[i])
	N += 1

print "Total: ", N
for i in range(0, len(line)):
	print "\t".join( [str(t) for t in  [i, len(d[i]), float(len(d[i]))/N]  ] )
