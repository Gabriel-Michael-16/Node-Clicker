import pygame
import time

class Node:

    def __init__(self, value, center, textContent, game):
        self.value = value
        self.radius = 25
        font = "Arial"
        fontSize = 32
        self.font = pygame.font.SysFont(font, fontSize)
        self.textSurface = self.font.render(textContent, True, (14,60,187))
        self.textRect = self.textSurface.get_rect()
        self.circleCenter = center
        self.children = []
        self.clicked = False
        self.time = 0
        self.game = game
        
       
    def draw(self, surface):
        if not pygame.mouse.get_pressed()[0]:
            self.time = time.time()
        pygame.draw.circle(surface, (255,255,255), self.circleCenter, self.radius)

        pos = pygame.mouse.get_pos()
        pos = (pos[0]/self.game.scaleFactor, pos[1]/self.game.scaleFactor)
        distance = ((self.circleCenter[0]-pos[0])**2 + (self.circleCenter[1]-pos[1])**2)**0.5
        if distance < self.radius and time.time() - self.time < 0.05:
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True

        self.textRect.center = self.circleCenter
        surface.blit(self.textSurface, self.textRect)
        pygame.display.update()
        return self.clicked

    def addChild(self, child):
        self.children.append(child)