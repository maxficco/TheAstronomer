print("TESTING TESTING")
import pygame, random

class Explosion:
	def __init__(self, x, y, radius = 1, thickness = 20):
		self.x = x
		self.y = y
		self.radius = radius
		self.thickness = thickness


	def grow(self):
		self.radius += 1
		if self.thickness > 1:
			self.thickness -= 1

	def draw(self, display, scroll):
		pygame.draw.circle(display, (255,255,255), (self.x-scroll[0], self.y-scroll[1]), int(self.radius), int(self.thickness))

class Particle:
	def __init__(self, x, y, radius):
		self.x = x
		self.y = y
		self.radius = radius
		self.xdirection = (random.randint(0,20)/10)-1
		self.ydirection = (random.randint(0,20)/10)-1
	def shrink(self):
		if self.radius > 1:
			self.radius -= 0.25
	def move(self):
		self.x += self.xdirection/4
		self.y += self.ydirection/4

class ParticleEffect:
	def __init__(self, x, y, number = 26, size = 15):
		self.number = number
		self.size = size
		self.particles = []
		for p in range(self.number):
			self.particles.append(Particle(x, y, self.size))

	def draw(self, display, scroll):
		for particle in self.particles:
			particle.shrink()
			particle.move()
			pygame.draw.circle(display, (255,255,255), (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
			if particle.radius == 1:
				self.particles.remove(particle)
			
