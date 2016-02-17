# LLoad module

from math import exp, log

class Lload:
	def __init__(self):
		self.timestamp = None
		self.prevMultiplier=1.0
		self.initiated=False
		self.value=0
	
	def toString(self):
		return "["+ str(self.value) + ", " + str(self.prevMultiplier) + ", " + str(self.initiated) + "]"
		
	def logVal(self):
		if not self.initiated:
			return 0 # log(1+0)
		else:
			return log(self.value*self.prevMultiplier)

	def addVal(self, tn, T):
		if not self.initiated:
			self.timestamp = tn
		self.initiated = True
		
		self.prevMultiplier = exp( -(tn-self.timestamp).total_seconds()/T )
		self.value = self.value + 1/self.prevMultiplier
	

class Lload2:
	def __init__(self):
		self.timestamp = None
		self.initiated=False
		self.value=0
		self.fresh = True
	
	def toString(self):
		return self #"["+ str(self.value) + ", " + str(self.initiated) + "]"
	
	def __str__(self):
		return '[' + "\t".join([str(x) for x in [self.value, self.initiated]]) +  ']'
		
	def logVal(self):
		if not self.initiated or self.fresh:
			return 0 # log(1+0)
		else:
			return log(1+self.value)

	def addVal(self, tn, T):
		if not self.initiated:
			self.timestamp = tn
		else:
			self.fresh = False
		self.initiated = True
		
		self.value = exp( -(tn-self.timestamp).total_seconds()/T )
		self.timestamp = tn
		
