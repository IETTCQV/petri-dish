from .Gen import *
from .Point import *

from random import randint as random
from pygame import draw

class Bacteria(Point):
	def init(self, app, pos):
		self.pos = list(pos) # строка из Point класса
		self.app = app
		self.color = [90,90,90]

		self.gen = Gen()
		self.gen += (2, 0)
		for _ in range(random(1,3)):
			self.gen += self.get_random_gen()

		self.index = 0

		self.enegry = 10
		self.cost_move = 1.2
		self.generation_efficiency = 2

	def get_direction(self, x):
		if x == 1:   return  1,  0
		elif x == 2: return  0, -1
		elif x == 3: return -1,  0
		elif x == 4: return  0,  1
		else:        return  0,  0

	def get_random_gen(self):
		x = random(0,99)
		if x >= 0 and x < 80:
			return (1, random(1,4)) # ген передвижения с шансом 80%

		elif x >= 80 and x < 90:
			return (3, random(1,4)) # ген поедания бактерии с шансом 10%

		elif x >= 90 and x < 100:
			return (3, random(1,4)) # ген размножения с шансом 10%

		return (0, 0)

	def get_bacteria(self, x, y):
		return self.app.bacteria[y][x]

	def set_bacteria(self, x, y, value):
		self.app.bacteria[y][x] = value
		
	def update(self):

		# удаление бактерий без генов
		if (len(self.gen) == 0) or (self.gen.get(0)[0] != 2):
			self.set_bacteria(*self.pos, 0)
			return

		# удаление бактерий без энергии
		if (self.enegry < 0):
			self.set_bacteria(*self.pos, 0)
			return

		if len(self.gen) == 0:
			return

		if self.enegry > 1000:
			self.enegry = 1000

		if self.index >= len(self.gen):
			self.index = 0

		gen, arg = self.gen.get(self.index)

		# движение
		if gen == 1:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)

			if self.get_bacteria(*pos) == 0:
				self.set_bacteria(*pos, self)
				self.set_bacteria(*self.pos, 0)
				self.x += zx
				self.y += zy

				if self.x >= self.app.sw: self.x = 0
				elif self.x < 0: self.x = self.app.sw-1

				if self.y >= self.app.sh: self.y = 0
				elif self.y < 0: self.y = self.app.sh-1
				
		# мутация генов
		elif gen == 2:
			x = random(0,100)

			# замена гена шанс 50%
			if x >= 0 and x < 50:
				index = random(0, len(self.gen)-1)
				gen2, arg2 = self.gen.get(index)
				if gen2 != 2:
					self.gen.set(index, self.get_random_gen())

			# добавление гена шанс 30%
			elif x >= 50 and x < 80 and len(self.gen) < 15:
				if self.enegry > 5:
					self.gen += self.get_random_gen()
					self.enegry -= 5

			# удаление гена 10%
			elif x >= 80 and x < 90:
				index = random(0, len(self.gen)-1)
				gen2, arg2 = self.gen.get(index)
				if gen2 != 2:
					self.gen.rem(index)
					self.enegry += 2.5

			# изменение цвета 3%
			elif x >= 90 and x < 93:
				arg = random(-16, 16)
				index = random(0,2)
				self.color[index] += arg
				if self.color[index] > 255:
					self.color[index] = 255
				elif self.color[index] < 0:
					self.color[index] = 0

			# изменение цены хода 7%
			elif x >= 93 and x < 100:
				if self.enegry > 10:
					self.cost_move = random(20,200)/100
					self.enegry -= 10

		# копирование
		elif gen == 3:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)

			if (self.get_bacteria(*pos) == 0) and self.enegry > 50:
				bacteria = Bacteria(self.app, pos)
				bacteria.color = self.color.copy()
				# bacteria.enegry = 10
				bacteria.cost_move = self.cost_move
				bacteria.gen = self.gen.copy()

				self.set_bacteria(*pos, bacteria)
				self.enegry -= 50

		# поедание других
		elif gen == 4:
			zx, zy = self.get_direction(arg)
			pos = (self.x+zx, self.y+zy)
			bacteria = self.get_bacteria(*pos)

			if (bacteria != 0) and (bacteria.gen.bytes != self.gen.bytes):
				self.enegry += bacteria.enegry / 2
				bacteria.enegry = -1
				self.set_bacteria(*pos, 0)

		self.enegry -= self.cost_move
		self.enegry += self.generation_efficiency * (1-self.x/(self.app.sw-1))
		self.index += 1

	def draw(self):
		block = self.app.block
		draw.rect(self.app.win, self.color, (self.x*block, self.y*block, block, block))

		# if 5 in self.gen:
		# 	image = font.render('M', True, (200,0,0))
		# 	self.app.win.blit(image, (self.x*size+5, self.y*size+2))