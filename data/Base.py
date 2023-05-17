
class Base:
	def __init__(self, *args, **kwargs):
		if hasattr(self, 'init') and callable(self.init):
			self.init(*args, **kwargs)