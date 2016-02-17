#!/usr/bin/env python
import sys
import avro.schema
from avro.datafile import DataFileReader
from avro.io import DatumReader

from os import listdir
from os.path import isfile, join

import json


def getKeys(d, S):
	for k, v in d.iteritems():
		if isinstance(v, dict):
			getKeys(v, S)
		S.add(k)

def main(argv):
	if len(argv)<2:
		print "No arguments provided"
		exit(1)
	S = set()
	D=dict()
	for path in argv[1:]:
		
		if isfile(path):
			fnames = [path]
		else:
			fnames = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
		
		for filename in fnames:
			try:
				with DataFileReader(open(filename, "r"), DatumReader()) as reader:
					for entry in reader:
						
						uuid = entry['uuid']
						#print uuid
						if uuid == 'd8217c4c-4cde-4dc9-9197-1d81897f9c31':
							print filename
							break
						
			except:
				print "ERR: " + filename
				print sys.exc_info()
				raise
	
main(sys.argv)
