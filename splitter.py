#!/usr/bin/env python

import sys
import random
from optparse import OptionParser

#for l in sys.stdin:
#	sys.std l, random.random()

def main():
	usage = "usage: %prog [options] "
	parser = OptionParser(usage)
	parser.add_option("-r", "--rate", dest="rate",
					help="percentage of lines going to stdout")
	(options, args) = parser.parse_args()
	
	
	if options.rate is None:
		parser.error('Rate (-r) is not given')
	try:
		rate = float(options.rate)
	except:
		parser.error('Cannot parse rate')
	
	for l in sys.stdin:
		if random.random()<rate:
			sys.stdout.write(l)
		else:
			sys.stderr.write(l)

	

if __name__ == "__main__":
	main()
