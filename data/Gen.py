
class Gen:
	def __init__(self, bytes=b''):
		self.bytes = bytes
		self.size = 2

	def __str__(self):
		return str(self.bytes)

	def __len__(self):
		return len(self.bytes)//self.size

	def __iadd__(self, other):
		if isinstance(other, Gen):
			self.bytes += other.bytes

		elif isinstance(other, bytes):
			self.bytes += other

		elif isinstance(other, int):
			self.bytes += bytes([other])

		elif isinstance(other, list) or isinstance(other, tuple):
			self.bytes += bytes(other)
		else:
			raise TypeError("unsupported operand type(s) for +=: 'Person' and '{}'".format(type(other).__name__))
		return self
	
	def get(self, index):
		start = index*self.size % len(self.bytes)
		end = (index*self.size + self.size) % len(self.bytes)
		if start < end:
			return list(self.bytes[start:end])
		else:
			return list(self.bytes[start:] + self.bytes[:end])

	def rem(self, index):
		start = index*self.size % len(self.bytes)
		end = (index*self.size + self.size) % len(self.bytes)
		if start < end:
			self.bytes = self.bytes[:start] + self.bytes[end:]
		else:
			self.bytes = self.bytes[start:end]

	def set(self, index, new_string):
		new_string = bytes(new_string)
		start = index*self.size % len(self.bytes)
		end = (index*self.size + self.size) % len(self.bytes)
		if start < end:
			self.bytes = self.bytes[:start] + new_string + self.bytes[end:]
		else:
			self.bytes = new_string[len(self.bytes)-start:] + self.bytes[start:end] + new_string[:len(self.bytes)-end]

	def copy(self):
		return Gen(self.bytes)