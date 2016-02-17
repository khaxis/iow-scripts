class UniqueList:
	CAPACITY = 5
	def __init__(self):
		self.data = []
	def add(self, x):
		if x in self.data:
			self.data.remove(x)
		self.data.append(x)
		if len(self.data)>UniqueList.CAPACITY:
			self.data = self.data[-UniqueList.CAPACITY:]
	def get(self):
		return self.data