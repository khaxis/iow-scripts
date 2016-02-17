#!/usr/bin/env python

import sys

lastuuid = ""
mysegs = set()

for l in sys.stdin:
	uuid, adv,ts,pixel,segs = l.rstrip("\n").split("\t")
	if uuid+adv != lastuuid:
		lastuuid=uuid+adv
		mysegs = set(segs.split(","))	# make sure initial segments set is the same as in the log
	s="\t".join([uuid,adv,ts,pixel,segs] + [",".join(sorted(list(mysegs)))])
	mysegs.discard('')
	for seg in mysegs:
		if seg and uuid and (seg not in segs.split(",")):
			#print seg
			theirSeg = set(segs.split(","))
			print '\t'.join([ts, uuid, str(sorted(list(mysegs))), seg, str(sorted(list(theirSeg)))])
			break
#	if any([seg not in segs.split(",") for seg in mysegs]):
#		print s
	mysegs.add(pixel)
