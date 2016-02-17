#!/usr/bin/env python

import sys
import urlparse
from datetime import timedelta, datetime
import copy
from math import exp, log
from lload import *
from uniqueList import *
import httpagentparser

LLOAD_KEYS = ['lload_conv_7d', 'lload_conv_1d', 'lload_conv_7h', 'lload_activ_7d', 'lload_activ_1d', 'lload_activ_7h']
LLOAD2_KEYS = ['lload2_conv_7d', 'lload2_conv_1d', 'lload2_conv_7h', 'lload2_activ_7d', 'lload2_activ_1d', 'lload2_activ_7h']
CONV = ['3133337']

LLOAD_KEYS = ['lload_adv_pixel_1d', 'lload_adv_pixel_7d', 'lload_adv_conversion_45d', 'lload_adv_session_30d']
LLOAD2_KEYS = ['lload2_adv_pixel_1d', 'lload2_adv_pixel_7d']
		
def setToStr(S):
	return ','.join(sorted([s for s in S]))


def printEntry(headers1, CONV, conversions, rrCopy):
	#return
	res = []
	
	historyPar = rrCopy.pop('historyPar', dict())
	
	for k in historyPar:
		rrCopy[k] = historyPar[k]

	for k in headers1:
		if k in rrCopy:
			res.append(str(rrCopy[k]).rstrip('\n'))
		else:
			res.append('')
	s = '\t'.join(res)
	for c in CONV:
		suc, tri = 0,1
		if conversions[c]:
			suc = 1
		print s + '\t' + '\t'.join([c, str(tri), str(suc)])
		
secIn1Day	= float(60*60*24)
secIn7Days	= secIn1Day*7
secIn7Hours	= float(60*60*7)
secIn30Days = secIn1Day*30
secIn45Days = secIn1Day*45


def computeLloads(lload, rr, currentTime, sessionStarted):
	'''
	if rr['segID'] in CONV:
		d = lload['lload_conv_7d']
		if not d.initiated:
			d.timestamp = currentTime
		d.addVal(currentTime, secIn7Days)
		
		d = lload['lload_conv_1d']
		if not d.initiated:
			d.timestamp = currentTime
		d.addVal(currentTime, secIn1Day)
		
		d = lload['lload_conv_7h']
		if not d.initiated:
			d.timestamp = currentTime
		d.addVal(currentTime, secIn7Hours)
	
	d = lload['lload_activ_7d']
	d.addVal(currentTime, secIn7Days)
	
	d = lload['lload_activ_1d']
	d.addVal(currentTime, secIn1Day)
	
	d = lload['lload_activ_7h']
	d.addVal(currentTime, secIn1Day)
	'''
	
	lload['lload_adv_pixel_1d'].addVal(currentTime, secIn1Day)
	lload['lload_adv_pixel_7d'].addVal(currentTime, secIn7Days)
	lload['lload2_adv_pixel_1d'].addVal(currentTime, secIn1Day)
	lload['lload2_adv_pixel_7d'].addVal(currentTime, secIn7Days)
	
	if sessionStarted:
		lload['lload_adv_session_30d'].addVal(currentTime, secIn30Days)
	
	
	if rr['segID'] in CONV:
		d = lload['lload_adv_conversion_45d']
		if not d.initiated:
			d.timestamp = currentTime
		d.addVal(currentTime, secIn7Days)
	
	
if True:
	overflow = False
	newUser = False
	lastuuid = ""
	mysegs = UniqueList()
	last_session_daypart = ''
	
	headers0 = ['conversion_id','trials', 'success']
	
	KEYS = ['amenities', 'categories', 'checkin', 'ci', 'checkout', 'co', 'city', 'distance', 'offerPrice', 'priceRange', 'propertyName', 'q', 'r', 'sort', 'stars', 'toSkip', 'utm_content', 'utm_medium', 'utm_source', 'utm_term', 'variation']
	headers1 = ['uuid', 'ts', 'ip', 'country', 'region', 'px', 'url', 'useragent', 'script', 'segID', 'segments', 'unknown_col', 'browser', 'browser_version', 'os', 'os_version', 'device_model', 'device_version', 'duration_of_stay', 'checkin_in_days', 'checkin_in_category', 'session_day_of_the_week', 'session_hour', 'checkin_day_of_the_week', 'destination_town', 'destination_country', 'priceRange_min', 'priceRange_max', 'priceRange_range', 'last_session_daypart'] + KEYS + LLOAD_KEYS + LLOAD2_KEYS
	headers = headers1 + headers0
	#print '#' + '\t'.join(headers)
	sys.stderr.write('\t'.join(headers) + '\n')
	conversions = dict()
	rrCopy = None
	
	ST = set()
	lloads = dict()
	
	for l in sys.stdin:
		rr = dict()
		#uuid	ts	ip	country	region	px	url	useragent	uuid	script	segID	11	12	13	segments	15	unknown_col	browser	os

		rr['uuid'], rr['ts'], rr['ip'], rr['country'], rr['region'], rr['px'], rr['url'], rr['useragent'], rr['uuid'], rr['script'], rr['segID'], rr['11'], rr['12'], rr['13'], rr['segments'], rr['15'], rr['unknown_col'], rr['browser'], rr['os'], rr['19'], rr['20'], rr['21'], rr['22'], rr['23'], rr['24'], rr['25'], rr['26'] = l.rstrip("\n").split("\t")
		
		if rr['segID'] == '3133338':
			continue
		"""
		####################################
		####################################
		####################################
		"""
		#if rr['uuid'] != '0001dadf-19f8-46e1-a702-800291067ef0':
		#	continue
		
			
		sessionStarted = False
		
		if len(rr['uuid'])<10:
			continue
		
		currentTime = datetime.strptime(rr['ts'], "%Y-%m-%d %H:%M:%S")
		par = urlparse.parse_qs(urlparse.urlparse(rr['url']).query)

		if rr['uuid'] not in lloads:
			ll = dict()
			for k in LLOAD_KEYS:
				ll[k] = Lload()
				ll[k].timestamp = currentTime
			for k in LLOAD2_KEYS:
				ll[k] = Lload2()
				ll[k].timestamp = currentTime
			lloads[rr['uuid']] = ll
		
		lload = lloads[rr['uuid']]
		for k in LLOAD_KEYS+LLOAD2_KEYS:
			rr[k] = lload[k].logVal()
		
		
		if rr['uuid'] != lastuuid or (currentTime-sessionStart).total_seconds()>120*60:	# new record or session expired
			if rrCopy is not None:
				printEntry(headers1, CONV, conversions, rrCopy)
				
			sessionStarted = True
			
			if rr['uuid'] != lastuuid:
				mysegs = UniqueList()
				last_session_daypart = ''
				historyPar = dict()
				
			for c in CONV:
				conversions[c] = 0
			rr['trials'] = 1
			
			lastuuid=rr['uuid']
			sessionStart = datetime.strptime(rr['ts'], "%Y-%m-%d %H:%M:%S")
			
			
			rr['last_session_daypart'] = last_session_daypart
			rr['historyPar'] = historyPar
			
			s = rr['useragent']
			userAgentData = httpagentparser.detect(s)
			
			if 'dist' in userAgentData:
				u = userAgentData['dist']
				if 'name' in u:
					rr['device_model'] = u['name']
					if 'version' in u:
						rr['device_version'] = u['name'] + '_' + u['version'].split('.')[0]
					
			rr['browser_version'] = rr['browser']
			rr['os_version'] = rr['os']
			rr['browser'] = rr['browser_version'].split('_')[0]
			rr['os'] = rr['os_version'].split('_')[0]
			if rr['os'] == 'Windows' or rr['os'] == 'Linux':
				rr['device_model'] = 'PC'
			elif rr['os'] == 'OSX':
				rr['device_model'] = 'Mac'
			
			rrCopy = copy.deepcopy(rr)

		for k in par:
			ST.add(k)
			#print "%s\t%s"%(k,par[k][0])
	
		#par = urlparse.parse_qs(urlparse.urlparse(rr['url']).query)
		#has_medium = 'utm_medium' in par
		#has_src = 'utm_source' in par
		#has_camp = 'utm_campaign' in par
		#if has_medium:
		#	for p in par['utm_medium']:
		#		utm_mediums.add(p)
		#if has_src:
		#	for p in par['utm_source']:
		#		utm_sources.add(p)
		#if has_camp:
		#	for p in par['utm_campaign']:
		#		utm_campaigns.add(p)
		
		pixel_id = rr['segID']
		if pixel_id in CONV:
			conversions[pixel_id] = 1

		mysegs.add(pixel_id)
		computeLloads(lloads[rr['uuid']], rr, currentTime, sessionStarted)
		
		if 1 <= currentTime.hour < 8:
			last_session_daypart = '1'
		elif 8 <= currentTime.hour < 10:
			last_session_daypart = '8'
		elif 10 <= currentTime.hour < 19:
			last_session_daypart = '10'
		else:
			last_session_daypart = '19'
			
		
		
		# checkin
		# checkout
		# ci
		# city
		# co
		# distance
		# offerPrice
		# priceRange
		# 'utm_content', 'utm_medium', 'utm_source'

		historyPar = dict()
		
		for k in KEYS:
			if k in par:
				historyPar[k] = ','.join([p.strip() for p in par[k]])
			else:
				historyPar[k] = ''
				
		
		######################
		# Specific for clickdistrict
		######################
		
		today = sessionStart.date()
		checkInDateStr, checkOutDateStr = None, None
		checkInDate = None
		checkOutDate = None
		ci, co = None, None
		if 'checkin' in par:
			checkInDateStr = par['checkin'][0]
		elif 'ci' in par:
			checkInDateStr = par['ci'][0]
		if 'checkout' in par:
			checkOutDateStr = par['checkout'][0]
		elif 'co' in par:
			checkOutDateStr = par['co'][0]
		if checkInDateStr is not None:
			ci = datetime.strptime(checkInDateStr, "%Y-%m-%d")
		if checkOutDateStr is not None:
			co = datetime.strptime(checkOutDateStr, "%Y-%m-%d")
		
		historyPar['session_day_of_the_week'] = sessionStart.weekday()
		historyPar['session_hour'] = sessionStart.hour
		
		if ci is not None and co is not None:
			historyPar['duration_of_stay'] = (co-ci).days
		if ci is not None:
			historyPar['checkin_in_days'] = (ci-sessionStart).days
			historyPar['checkin_day_of_the_week'] = ci.weekday()
			category = 'more_than_28days'
			if historyPar['checkin_in_days'] <= 1:
				category = '1days'
			elif historyPar['checkin_in_days'] <= 4:
				category = '2days'
			elif historyPar['checkin_in_days'] <= 7:
				category = '7days'
			elif historyPar['checkin_in_days'] <= 14:
				category = '14days'
			elif historyPar['checkin_in_days'] <= 28:
				category = '28days'
			historyPar['checkin_in_category'] = category
			
		#'duration_of_stay', 'checkin_in_days', 'checkin_in_category', 'destination_town', 'destination_country', 'priceRange_min', 'priceRange_max', 'priceRange_range'
		
		if 'city' in par:
			place = par['city'][0]
			pp = place.split(", ")
			historyPar['destination_town'] = pp[0]
			if len(pp)>1:
				historyPar['destination_country'] = pp[1]
		
		if 'priceRange' in par:
			priceRange = par['priceRange'][0]
			pp = priceRange.split(',')
			m = int(pp[0])
			historyPar['priceRange_min'] = str(m)
			if len(pp)>1:
				M = int(pp[1])
				historyPar['priceRange_max'] = str(M)
				historyPar['priceRange_range'] = str(M-m)
		
		
		
	if rrCopy is not None:
		printEntry(headers1, CONV, conversions, rrCopy)
	
	
elif False:
	for l in sys.stdin:
		uuid, adv,ts, lload,pixel,segs,mysegs = l.rstrip("\n").split("\t")
		if uuid != '' and len(mysegs.split(','))>5:
			print l,
else:
	ts = ['2015-07-13 14:00:00','2015-07-13 14:00:00','2015-07-13 14:00:00','2015-07-13 15:00:00','2015-07-13 15:00:00','2015-07-13 15:00:00','2015-07-13 16:00:00','2015-07-13 16:00:00','2015-07-13 16:00:00','2015-07-15 13:00:00','2015-07-15 13:00:00']
	
	T = float(60*60*24)
	l = Lload2()
	firstTime = True
	for t in ts:
		tn = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
		l.addVal(tn, T)
		print l.logVal(), ('\t' if not firstTime else '\t\t') , l.toString()
		
		firstTime = False
		#print l.logVal()
		
	ul = UniqueList()
	print ul.get()
	for x in [1, 2, 3, 4, 1, 5, 6, 7]:
		print x,
		ul.add(x)
		print ul.get()
	
	
