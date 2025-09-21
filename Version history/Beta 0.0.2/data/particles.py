import pygame, random


class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, colour, direction, speed, maxWidth, maxHeight):
        super().__init__(groups)
        self.pos = pos
        self.colour = colour
        self.direction = direction
        self.speed = speed
        self.maxSpeed = random.choices(("min","mid", "max"))
        self.maxWidth = maxWidth
        self.maxHeight= maxHeight
        self.takeOut = False
        self.prevDirection = direction
        self.alphaDir = random.choices((True,False))
        self.alpha = random.randint(0,160)
        self.fadeSpeed = 20
        self.createSurface()

    def createSurface(self):
        self.image = pygame.Surface((8, 8)).convert_alpha()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image,self.colour,(2,2),100)
        self.rect = self.image.get_rect(center=self.pos)
    
    def fadeDown(self, dt):
        if not self.alphaDir:
            self.alpha -= self.fadeSpeed * dt
            self.image.set_alpha(self.alpha)

    def fadeUp(self, dt):
        if self.alphaDir:
            self.alpha += self.fadeSpeed * dt
            self.image.set_alpha(self.alpha)

    def checkFade(self):
        if self.alpha < 0:
            self.alphaDir = True
        elif self.alpha > 200:
            self.alphaDir = False

    def move(self, dt):
        self.pos += self.direction * self.speed * dt * 5.5
        self.rect.center = self.pos

    def checkPos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > self.maxWidth+50 or
            self.pos[1] < -50 or
            self.pos[1] > self.maxHeight+50 
        ):
            self.takeOut = True
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fadeUp(dt)
        self.fadeDown(dt)
        self.checkFade()
        self.checkPos()