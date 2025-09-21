import pygame
import keyboard
import time
class Button():

    def __init__(self, x, y, image, scale, buttonPress, game):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect() 
        self.rect.topleft = (x, y)
        self.buttonPress = buttonPress
        self.clicked = False
        self.action = False
        self.game  = game

    def render(self, surface):
        self.update()
        self.draw(surface)
    
    def update(self):
        self.action = False
        self.exit()

    def draw(self, surface):

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint((pos[0]/self.game.scaleFactor, pos[1]/self.game.scaleFactor)):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                self.action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # pos = pygame.mouse.get_pos()
        # if pygame.mouse.get_pressed()[0]:
        #          print(pos)

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        return self.action
    
    def exit(self):
        if keyboard.is_pressed(self.buttonPress):
            self.clicked = True
            self.action = True
        return