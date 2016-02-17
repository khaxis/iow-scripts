#!/usr/bin/env python

import sys
import random
from math import *
from optparse import OptionParser

#for l in sys.stdin:
#	sys.std l, random.random()

def readFile(filename, probabilityHeader, triesHeader, successesHeader):
	res = []
	with open(filename) as f:
		l = f.readline().strip().lstrip('#')
		header = [ x[0] for x in [t.split(':') for t in l.split(',')]]
		pIdx = header.index(probabilityHeader)
		tIdx = header.index(triesHeader)
		sIdx = header.index(successesHeader)
		
		for l in f:
			a = l.strip().split("\t")
			p = float(a[pIdx])
			m = float(a[tIdx])
			n = float(a[sIdx])
			p = min(p, 0.95)
			res.append([p,m,n])
			
	return res

def main():
	usage = "usage: %prog [options] file_1 [file_2 [...]]"
	parser = OptionParser(usage)
	parser.add_option("-p", "--probability", dest="probability",
					help="P")
	parser.add_option("-t", "--tries", dest="tries",
					help="N")
	parser.add_option("-s", "--successes", dest="successes",
					help="M")
	(options, args) = parser.parse_args()
	
	
	probHeader    = [x for x in [options.probability, 'prob'] if x is not None][0]
	trialsHeader  = [x for x in [options.tries, 'trials'] if x is not None][0]
	successHeader = [x for x in [options.successes, 'success'] if x is not None][0]
	
	if len(args) == 0:
		parser.error('Input files must be provided')
	
	tables = []
	for filename in args:
		tables.append(readFile(filename, probHeader, trialsHeader, successHeader))
	
	total_weights_in_test_data = 0
	llhs = dict()

	print "-------------------"
	print "- LLHs"
	print "-------------------"
	
	for it in range(len(tables)):
		llh = 0.0;
		M = 0;
		N = 0
		t = tables[it]
		for l in t:
			p = l[0]
			m = l[1]
			n = l[2]
			
			#print l
			
			llh += n*log(p) + (m-n)*log(1-p)
			
			M += m
			N += n
		
		if total_weights_in_test_data>0 and total_weights_in_test_data <> M:
			print "Error: you should use the same test data"
			exit(1)
		total_weights_in_test_data = M
		print args[it]
		print 'LLH:',llh
		llhs[args[it]] = llh
		print "-------------------"
	
	print 
	print M, N
	print "-------------------"
	print "- Variances"
	print "-------------------"
	
	sqrtVars = dict()
	
	for it1 in range(len(tables)):
		for it2 in range(len(tables)):
			if it1==it2:
				continue
			var = 0.0;
			M = 0;
			t1 = tables[it1]
			t2 = tables[it2]
			for l1, l2 in zip(t1, t2):
				p1 = l1[0]
				m1 = l1[1]
				n1 = l1[2]
				p2 = l2[0]
				m2 = l2[1]
				n2 = l2[2]
				
				var += (log( (p1/(1-p1))/(p2/(1-p2)) )**2) * m1*p1*(1-p1)
				
				M += m1
			print args[it1], "X", args[it2]
			print 'var:',sqrt(var)/M
			sqrtVars[(args[it1], args[it2])] = sqrt(var)/M
			print "-------------------"
			
	print
	print
	print "-------------------"
	print "- Qualities"
	print "-------------------"
	
	for it1 in range(len(tables)):
		for it2 in range(len(tables)):
			if it1==it2:
				continue
				
			print args[it1], "X", args[it2]
			quality =  (llhs[args[it2]] - llhs[args[it1]])/total_weights_in_test_data
			print "quality:",quality
			print "-------------------"
	

if __name__ == "__main__":
	main()
