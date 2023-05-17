import pygame
from pygame import display, draw, Surface, Rect, init
from pygame import QUIT, KEYDOWN
from random import randint
from threading import Thread

from data.Bacteria import *

init()

class LList(list):
	def __init__(self, *args):
		super().__init__(args)

	def __getitem__(self, index):
		if index >= len(self):
			return self[index % len(self)]
		else:
			return super().__getitem__(index)

	def __setitem__(self, index, value):
		if index >= len(self):
			index %= len(self)
		super().__setitem__(index, value)

font = pygame.font.SysFont('Consolas', 16)

class App(Base):

	wm = 16 # множитель ширины
	hm = 9 # множитель высоты

	@property
	def w(self): return self.wh[0]

	@w.setter
	def w(self, value): self.wh[0] = value

	@property
	def h(self): return self.wh[1]

	@h.setter
	def h(self, value): self.wh[1] = value

	def init(self, size, block):
		# size - множитель размера окна (1 = 16x9 пикселей)
		
		self.block = block      # размер блока
		self.wh = [size*block*self.wm, size*block*self.hm]
		self.sw = self.w//block # ширина окна в блоках
		self.sh = self.h//block # высота окна в блоках

		class clock:
			event = pygame.time.Clock()
			update = pygame.time.Clock()
			draw = pygame.time.Clock()

		class fps:
			event = 60
			update = 20
			draw = 60

		self.clock = clock
		self.fps = fps

		self.win = display.set_mode(self.wh)
		self.running = True
		self.events = []
		self.background = (30,30,30)

		self.bacteria = LList(*[LList(*[0]*self.sw) for _ in range(self.sh)])
		self.pause = False
			
		self.spawn()

	def spawn(self, chance = 10):
		# chance - шанс спавна бактерий (%)
		for x in range(self.sw):
			for y in range(self.sh):
				if randint(0, 99) < chance:
					self.bacteria[y][x] = Bacteria(self, (x, y))

	def run(self):
		Thread(target=self.update, daemon=True).start()
		Thread(target=self.draw, daemon=True).start()
		self.event()

	def event(self):
		while self.running:
			self.events = pygame.event.get()
			for event in self.events:

				if event.type == QUIT:
					self.running = False
					continue

				elif event.type == KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.pause = not self.pause

					elif event.key == pygame.K_r:
						self.spawn()

			self.clock.event.tick(self.fps.event)

	def update(self):
		while self.running:
			while self.pause:
				pass

			for level in self.bacteria:
				for bacteria in level:
					if bacteria == 0:
						continue
					bacteria.update()
			self.clock.update.tick(self.fps.update)

	def draw(self):
		while self.running:
			self.win.fill(self.background)
			for x in range(self.sw):
				z = 60*x/self.sw
				draw.rect(self.win, (30-z//2,60-z,90-z), (x*self.block, 0, self.block, self.h))

			for level in self.bacteria:
				for bacteria in level:
					if bacteria == 0:
						continue
					bacteria.draw()

			if self.pause:
				x,y = x2,y2 = pygame.mouse.get_pos()
				x //= self.block
				y //= self.block

				bacteria = self.bacteria[y][x]
				if bacteria != 0:
					text = []
					for i in range(len(bacteria.gen)):
						gen, arg = bacteria.gen.get(i)
						text.append(f'{gen}-{arg}')
					text = ','.join(text)
					image = font.render(text, True, (200,0,0), (0,0,0))
					self.win.blit(image, (x2+10, y2+10))

					text = "e: "+str(round(bacteria.enegry, 1))
					image = font.render(text, True, (200,0,0), (0,0,0))
					self.win.blit(image, (x2+10, y2+30))

			# отладочная информация
			text = str(int(self.clock.event.get_fps()))
			image = font.render(text, True, (200,0,0))
			self.win.blit(image, (10, 10))

			text = str(int(self.clock.update.get_fps()))
			image = font.render(text, True, (200,0,0))
			self.win.blit(image, (10, 30))

			text = str(int(self.clock.draw.get_fps()))
			image = font.render(text, True, (200,0,0))
			self.win.blit(image, (10, 50))

			display.flip()
			self.clock.draw.tick(self.fps.draw)


if __name__ == '__main__':
	app = App(size=5, block=16)
	app.run()