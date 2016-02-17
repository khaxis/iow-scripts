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
			print 'try', filename
			try:
				with DataFileReader(open(filename, "r"), DatumReader()) as reader:
					for entry in reader:
						
						#for key, value in entry.iteritems():
						#	S.add(key)
						
						#getKeys(entry, S)
						uuid = entry['uuid']
						if uuid != 'bf36d24a-6a15-4b96-804c-80f50a0ccd33':
							continue
						for k in entry:
							if k not in D:
								D[k] = []
							D[k].append(entry[k])
						 
						#for key in entry.iteritems():
						#	S.add(key)
						
						#if 'uh_snapshot' not in entry:
						#	continue
						#tmp = entry['uh_snapshot']
						#if len(tmp["utm_campaigns"] +  tmp["utm_mediums"] + tmp["utm_sources"])==0:
						#	continue
						
						#print filename
						print json.dumps(entry, sort_keys=True, indent=4)
						#print "--------------- %d"%(i)
						#break
			except:
				print "ERR: " + filename
				print sys.exc_info()
				raise
	for k in D:
		print k
		for u in D[k]:
			print u
		print "-"*60
	
	for s in sorted([x for x in S]):
		print s

main(sys.argv)
