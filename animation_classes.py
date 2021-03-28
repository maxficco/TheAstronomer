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
	def lighting(self, color):
		surf = pygame.Surface((self.radius * 3, self.radius * 3))
		colorchange = list(color)
		for number in range(len(colorchange)):
			colorchange[number] = colorchange[number]*(30/255)
		color = tuple(colorchange)
		pygame.draw.circle(surf, color, (self.radius*1.5, self.radius*1.5), self.radius*1.5)
		surf.set_colorkey((0, 0, 0))
		return surf
	
class Disappeario:
	def __init__(self, x, y, number = 26, size = 15):
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
	def draw(self, display, scroll):
		for particle in self.particles:
			pygame.draw.circle(display, (255,255,255), (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
			if particle.radius < 1:
				self.particles.remove(particle)

class Torch:
	def __init__(self, x, y, colorindex, number = 14, size = 4.5):
		rgb_list = [(85, 46, 193),(8, 223, 109),(183, 167, 35),(19, 57, 249),(241, 240, 226),(119, 5, 9)]
		self.color = rgb_list[colorindex]
		self.torch = pygame.image.load("sprites/torch.png")
		self.ogx = x
		self.ogy = y
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
		for particle in self.particles:
			particle.grav -= 0.0125
			if particle.grav < -3:
				self.grav = -3
			particle.y += particle.grav
	
	def draw(self, display, scroll, spritebox, sprite1 = False, follow = False):
		if sprite1:
			asdf = 10
		else:
			asdf = 9
		if follow == True:
			display.blit(self.torch, (spritebox.x-scroll[0]-asdf, spritebox.y-scroll[1]-4))
			for particle in self.particles:
				pygame.draw.circle(display, self.color, (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
				if particle.radius < 1:
					self.particles.remove(particle)
					self.particles.append(Particle(spritebox.x-asdf+6, spritebox.y-asdf+6, self.size))
			for particle in self.particles:
				display.blit(particle.lighting(self.color), (particle.x-scroll[0]-particle.radius*1.5, particle.y-scroll[1]-particle.radius*1.5), special_flags=pygame.BLEND_RGB_ADD)

		else:
			display.blit(self.torch, (self.ogx-scroll[0]-asdf, self.ogy-scroll[1]-4))
			for particle in self.particles:
				pygame.draw.circle(display, self.color, (particle.x-scroll[0], particle.y-scroll[1]), int(particle.radius))
				if particle.radius < 1:
					self.particles.remove(particle)
					self.particles.append(Particle(self.ogx-asdf+6, self.ogy-asdf+6, self.size))
			for particle in self.particles:
				display.blit(particle.lighting(self.color), (particle.x-scroll[0]-particle.radius*1.5, particle.y-scroll[1]-particle.radius*1.5), special_flags=pygame.BLEND_RGB_ADD)


class DoubleJump:
	def __init__(self, x, y, number = 9, size = 12):
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