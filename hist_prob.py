#!/usr/bin/env python

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys


data = []
for l in sys.stdin:
	#uuid, checkIn, duration, success = l.rstrip("\n").split("\t")
	uuid, dow, hour, ci_dow, success = l.rstrip("\n").split("\t")
	e = dict()
	e['uuid'], e['dow'], e['hour'], e['ci_dow'], e['success'] = uuid, int(dow), int(hour), int(ci_dow), int(success)
	data.append(e)

key = 'ci_dow'

allValues = [e[key] for e in data]
start = min(allValues)
end = max(allValues)
N = end - start + 1

tries   = np.zeros(N)
successes = np.zeros(N)
probs   = np.zeros(N)

for e in data:
	index = e[key] - start
	if index<0 or index >= N:
		continue
	tries[index] += 1
	successes[index] += e['success']
	probs[index] = float(successes[index])/tries[index]

coef = max(tries)
allValues = np.array(range(start, end+1))

plt.plot(allValues, tries, 'r')
plt.plot(allValues, successes, 'g')
plt.plot(allValues, probs*coef, 'b')

plt.show()

