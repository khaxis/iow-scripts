#!/usr/bin/env python

import sys
import urlparse
from datetime import timedelta, datetime
import copy

lastuuid = ""
mysegs = set()

uuids2015filename = "/home/ikhomyakov/tmp/uuids_2015"

def setToStr(S):
	return ','.join(sorted([s for s in S]))


def f(headers1, CONV, conversions, rrCopy):
	res = []
	for k in headers1:
		res.append(str(rrCopy[k]))
	s = '\t'.join(res)
	for c in CONV:
		suc, tri = 0,1
		if conversions[c]:
			suc = 1
		if c==104 and rr['IDENTIFIED']:
			suc=0
		print s + '\t' + '\t'.join([c, str(tri), str(suc)])

if True:
	overflow = False
	newUser = False
	utm_mediums = set()
	utm_sources = set()
	utm_campaigns = set()
	
	headers0 = ['conversion_id','trials', 'success']
	
	headers1 = ['uuid','utm_mediums','utm_sources','utm_campaigns','IDENTIFIED',   'advertiser_id','user.geo.country','user.geo.country_region','user.agent.device.model','user.agent.device.type','user.agent.device.maker','user.agent.os.name','user.agent.os.version','user.browser.os.name','user.browser.os.version','segments','uh_snapshot.lload_brand_pixel_1d','uh_snapshot.lload_brand_pixel_7d','uh_snapshot.lload2_brand_pixel_1d','uh_snapshot.lload2_brand_pixel_7d','uh_snapshot.lload_brand_conversion_45d','uh_snapshot.lload_brand_session_30d','uh_snapshot.last_session_daypart']
	headers = headers1 + headers0
	#print '\t'.join(headers)
	conversions = dict()
	CONV = ['104', '106']
	rrCopy = None
	
	indentifiedUsers = set()
	with open(uuids2015filename, 'r') as qq:
		for l in qq:
			indentifiedUsers.add(l)
	
	for l in sys.stdin:
		rr = dict()
		uuid, adv,ts,pixel_id,referer,request_uri,lload,pixel,segs,rr['advertiser_id'],rr['user.geo.country'],rr['user.geo.country_region'],rr['user.agent.device.model'],rr['user.agent.device.type'],rr['user.agent.device.maker'],rr['user.agent.os.name'],rr['user.agent.os.version'],rr['user.browser.os.name'],rr['user.browser.os.version'],rr['segments'],rr['uh_snapshot.lload_brand_pixel_1d'],rr['uh_snapshot.lload_brand_pixel_7d'],rr['uh_snapshot.lload2_brand_pixel_1d'],rr['uh_snapshot.lload2_brand_pixel_7d'],rr['uh_snapshot.lload_brand_conversion_45d'],rr['uh_snapshot.lload_brand_session_30d'],rr['uh_snapshot.last_session_daypart'] = l.rstrip("\n").split("\t")
		currentTime = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
		if len(uuid)<10:
			continue
		if uuid+adv != lastuuid or (currentTime-sessionStart).total_seconds()>120*60:	# new record or session expired
			if 'IDENTIFIED' in request_uri:
				indentifiedUsers.add(uuid)
			
			if rrCopy is not None:
				f(headers1, CONV, conversions, rrCopy)
			
			if uuid+adv != lastuuid:
				mysegs = set()
				overflow = False
				newUser = False
				utm_mediums = set()
				utm_sources = set()
				utm_campaigns = set()
			for c in CONV:
				conversions[c] = False
			trials, success = 1,0
			
			lastuuid=uuid+adv
			
			sessionStart = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
			
			rr['utm_mediums'] = setToStr(utm_mediums)
			rr['utm_sources'] = setToStr(utm_sources)
			rr['utm_campaigns'] = setToStr(utm_campaigns)
			rr['IDENTIFIED'] = uuid in indentifiedUsers
			rr['uuid'] = uuid
			
			if newUser:
				indentifiedUsers.add(uuid)
			rrCopy = copy.deepcopy(rr)
		
		#print ts, (currentTime-sessionStart).total_seconds()
		
		s="\t".join([uuid,adv,ts,pixel_id,referer,request_uri,lload,pixel,segs] + [",".join(sorted(list(mysegs)))] + [str(overflow), str(newUser), setToStr(utm_mediums), setToStr(utm_sources), setToStr(utm_campaigns), str(trials), str(success)])
		#for seg in mysegs:
		#	if uuid and (seg not in segs.split(",")):
		#		print seg		
		
		#print s
		#if any([seg not in segs.split(",") for seg in mysegs]):
		#	print s
	
	
		par = urlparse.parse_qs(urlparse.urlparse(referer).query)
		has_medium = 'utm_medium' in par
		has_src = 'utm_source' in par
		has_camp = 'utm_campaign' in par
		if has_medium:
			for p in par['utm_medium']:
				utm_mediums.add(p)
		if has_src:
			for p in par['utm_source']:
				utm_sources.add(p)
		if has_camp:
			for p in par['utm_campaign']:
				utm_campaigns.add(p)
		
		if pixel_id in CONV and not conversions[pixel_id]:
			conversions[pixel_id] = True
			trials, success = 0,1
		else:
			trials, success = 1,0
	
		mysegs.add(pixel)
		
		overflow = len(mysegs)>5
		if 'IDENTIFIED' in request_uri:
			newUser = True
	if rrCopy is not None:
		f(headers1, CONV, conversions, rrCopy)
	
	
else:
	for l in sys.stdin:
		uuid, adv,ts, lload,pixel,segs,mysegs = l.rstrip("\n").split("\t")
		if uuid != '' and len(mysegs.split(','))>5:
			print l,
