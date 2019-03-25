class Whisky:
	
	def __init__(self, name, distillery, region, age, abv, notes):
		if not len(name) < 256:
			raise ValueError("Length of name exceeds 255 chars")
		if not len(distillery) < 256:
			raise ValueError("Length of distillery exceeds 255 chars")
		if not len(region) < 256:
			raise ValueError("Length of region exceeds 255 chars")
		if not len(notes) < 256:
			raise ValueError("Length of notes exceeds 255 chars")
				
		self._name = name
		self._distillery = distillery
		self._region = region
		self._age = age
		self._abv = abv
		self._notes = notes
	
	def name(self):
		return self._name
	def region(self):
		return self._region
	def distillery(self):
		return self._distillery
	def age(self):
		return self._age
	def abv(self):
		return self._abv
	def notes(self):
		return self._notes
		
		
	
		
	