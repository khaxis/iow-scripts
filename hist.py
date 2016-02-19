#!/usr/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab as P
import sys
from optparse import OptionParser

def main():
	
	usage = "usage: %prog [options] "
	parser = OptionParser(usage)
	parser.add_option("-k", "--column", dest="column",
					help="K")
	parser.add_option("-b", "--bins", dest="bins",
					help="B")
	parser.add_option("-s", "--separator", dest="separator",
					help="S")
	
	(options, args) = parser.parse_args()
	
	
	columnNumber    = int([x for x in [options.column, 1] if x is not None][0])
	binsCount    = int([x for x in [options.bins, 10] if x is not None][0])
	separator       = [x for x in [options.separator, '\t'] if x is not None][0]
	
	#############################
	
	data = []
	for l in sys.stdin:
		#uuid, checkIn, duration, success = l.rstrip("\n").split("\t")
		e = float(l.rstrip("\n").split(separator)[columnNumber-1])
		data.append(e)

	start = min(data)
	end   = max(data)

	N = end-start+1
	counter = np.zeros(binsCount)
	total   = np.zeros(N)
	
	step = float(end-start)/binsCount
	
	bins = [start + step*i for i in range(1, binsCount+1)]

	for e in data:
		i = 0
		index = int(e - start)
		if index>0 or index < N:
			total[index] += 1
		while e>bins[i]:
			#print e, bins[i]
			i += 1
		counter[i] += 1
		
	
	print "###########################"
	print "# Statistics"
	print "###########################"
	print "start: ", start
	print "end: ", end
	print '--------------------'
	print ','.join([str(f) for f in total])
	
	print "###########################"
	print "# Bins"
	print "###########################"
	for b in bins:
		print b
	#tries   = np.zeros(N)

	
	print "###########################"
	print "# Hist"
	print "###########################"
	for c in counter:
		print c
	
if __name__ == "__main__":
	main()
