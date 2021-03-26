print("TESTING TESTING")
import pygame, random

class Explosion:
	def __init__(self, x, y, radius = 1, thickness = 10):
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
		self.grav = 0
	
class Disappeario:
	def __init__(self, x, y, number = 260, size = 150):
		self.number = number
		self.size = size
		self.particles = []
		for p in range(self.number):
			self.particles.append(Particle(x, y, self.size))
	def shrink(self):
		for particle in self.particles:
			if particle.radius > 0:
				particle.radius -= 0.25
	def move(self):
		for particle in self.particles:
			particle.x += particle.xdirection/4
			particle.y += particle.ydirection/4
	def gravity(self):
		for particle in self.particles:
			particle.grav += 0.0125
			if particle.grav > 3:
				self.grav = 3
			particle.y += particle.grav
	def draw(self, display, scroll):
		for particle in self.particles:
			pygame.draw.circle(display, (255,255,255), (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
			if particle.radius < 1:
				self.particles.remove(particle)

class SmokeParticles:
	def __init__(self, x, y, number = 14, size = 6):
		self.number = number
		self.size = size
		self.particles = []
		for p in range(self.number):
			self.particles.append(Particle(x, y, self.size))
	def shrink(self):
		for particle in self.particles:
			hmm = random.randint(0,26)
			if hmm < 13:
				if particle.radius > 0:
					particle.radius -= 0.25
	def move(self):
		for particle in self.particles:
			particle.x += particle.xdirection/3
			particle.y += particle.ydirection/3
	def gravity(self):
		for particle in self.particles:
			particle.grav -= 0.0125
			if particle.grav < -3:
				self.grav = -3
			particle.y += particle.grav
	def draw(self, display, scroll, spritebox):
		for particle in self.particles:
			pygame.draw.circle(display, (255,255,255), (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
			if particle.radius < 1:
				self.particles.remove(particle)
				self.particles.append(Particle(spritebox.x+6, spritebox.y-6, self.size))

class Firework:
	pass
			
