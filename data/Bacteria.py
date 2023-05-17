from .Gen import *
from .Point import *

from random import randint as random
from pygame import draw


def bytes_similarity(str1: bytes, str2: bytes) -> float:
	"""
	Функция расчета коэффициента равенства двух байтовых строк.

	:param str1: Первая байтовая строка.
	:param str2: Вторая байтовая строка.
	:return: Коэффициент равенства двух байтовых строк.
	"""
	# if len(str1) != len(str2):
	# 	return 0.0

	match_count = sum(1 for b1, b2 in zip(str1, str2) if b1 == b2)
	similarity = match_count / len(str1)
	return similarity


class Bacteria(Point):
	def init(self, app, pos):
		self.pos = list(pos) # строка из Point класса
		self.app = app
		self.color = [90,90,90]

		self.gen = Gen()
		self.gen += (2, 0)
		# for _ in range(random(1,3)):
		# 	self.gen += self.get_random_gen()

		self.index = 0

		class cost:
			move = random(100,400)/100
			mutation = 3
			copy = 50

		self.cost = cost
		self.enegry = random(7,15)
		self.efficiency = 1

	def get_direction(self, x):
		if x == 1:   return  1,  0
		elif x == 2: return  0, -1
		elif x == 3: return -1,  0
		elif x == 4: return  0,  1
		else:        return  0,  0

	def get_random_gen(self):
		x = random(0,99)

		if x < 40:               # ген генерации с шансом 40%
			x = random(0,99)
			if x < 90:               # уровень 1 с шансом 90%
				return (5, 1) 

			elif x < 99:             # уровень 2 с шансом 9%
				return (5, 2) 

			elif x < 100:            # уровень 3 с шансом 1%
				return (5, 3) 

		elif x < 60:             # ген поедания бактерии с шансом 20%
			return (4, random(1,4)) 

		elif x < 99:             # ген размножения с шансом 39%
			return (3, random(1,4)) 

		elif x < 100:            # ген мутации с шансом 1%
			return (2, 1)           

		return (0, 0)

	def get_bacteria(self, x, y):
		return self.app.bacteria[y][x]

	def set_bacteria(self, x, y, value):
		self.app.bacteria[y][x] = value
		
	def update(self):

		# удаление бактерий без генов
		if (len(self.gen) == 0) or (self.gen.get(0)[0] != 2):
			# self.set_bacteria(*self.pos, 0)
			self.gen.bytes = b'\x02\x00'
			# print('удаление бактерий без генов')
			# return

		# удаление бактерий без энергии
		if (self.enegry < 0):
			self.set_bacteria(*self.pos, 0)
			return

		if self.enegry > 1000:
			self.enegry = 1000

		if self.index >= len(self.gen):
			self.index = 0

		gen, arg = self.gen.get(self.index)

		# движение
		if gen == 0:
			self.gen.rem(self.index)

		elif gen == 1:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)

			if (self.get_bacteria(*pos) == 0):
				self.set_bacteria(*pos, self)
				self.set_bacteria(*self.pos, 0)
				self.x += zx
				self.y += zy

				if self.x >= self.app.sw: self.x = 0
				elif self.x < 0: self.x = self.app.sw-1

				if self.y >= self.app.sh: self.y = 0
				elif self.y < 0: self.y = self.app.sh-1
				self.enegry -= self.cost.move
				
		# мутация генов
		elif gen == 2:
			x = random(0,100)

			# замена гена шанс 52%
			if x < 53:
				if len(self.gen) > 1:
					index = random(1, len(self.gen)-1)
					self.gen.set(index, self.get_random_gen())
					self.enegry -= self.cost.mutation

			# добавление гена шанс 40%
			elif x < 93:
				if len(self.gen) < 15:
					self.gen += self.get_random_gen()
					self.enegry -= self.cost.mutation

			# удаление гена 5%
			elif x < 98:
				if len(self.gen) > 1:
					index = random(1, len(self.gen)-1)
					self.gen.rem(index)
					self.enegry += 2.5
					self.enegry -= self.cost.mutation

			# изменение цвета 2%
			elif x < 100:
				arg = random(-16, 16)
				index = random(0,2)
				self.color[index] += arg
				if self.color[index] > 255:
					self.color[index] = 255
				elif self.color[index] < 0:
					self.color[index] = 0
				self.enegry -= self.cost.mutation

			# изменение цены хода 7%
			# elif x >= 93 and x < 100:
			# 	self.cost.move = random(20,200)/100
			# 	self.enegry -= self.cost.mutation

		# копирование
		elif gen == 3:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)

			if (self.get_bacteria(*pos) == 0) and (self.enegry > self.cost.copy):
				bacteria = Bacteria(self.app, pos)
				bacteria.color = self.color.copy()
				bacteria.enegry = self.cost.copy/2
				bacteria.cost.move = self.cost.move
				bacteria.gen = self.gen.copy()

				self.set_bacteria(*pos, bacteria)
				self.enegry -= self.cost.copy

		# поедание других
		elif gen == 4:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)
			bacteria = self.get_bacteria(*pos)

			if (bacteria != 0) and bytes_similarity(self.gen.bytes, bacteria.gen.bytes) < 0.8:
				self.enegry += bacteria.enegry / 2
				bacteria.enegry = -1
				self.set_bacteria(*pos, 0)

		# генерация энергии
		elif gen == 5:
			self.enegry += arg * self.efficiency * (1-self.x/(self.app.sw-1))

		self.enegry += self.efficiency * (1-self.x/(self.app.sw-1))
		self.index += 1

	def draw(self):
		block = self.app.block
		draw.rect(self.app.win, self.color, (self.x*block, self.y*block, block, block))

		# if 5 in self.gen:
		# 	image = font.render('M', True, (200,0,0))
		# 	self.app.win.blit(image, (self.x*size+5, self.y*size+2))