from .Base import *

class Point(Base):
	def init(self, pos):
		self.pos = list(pos)

	@property
	def x(self): return self.pos[0]

	@x.setter
	def x(self, value): self.pos[0] = value

	@property
	def y(self): return self.pos[1]

	@y.setter
	def y(self, value): self.pos[1] = value