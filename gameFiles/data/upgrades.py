import pygame
import time
import os

class Upgrades():
    def __init__(self, center, name, tooltip, amountIncrease, cost, nameOfVariable, revealPurchase, prevUpgrade, imagePath, game):
        self.center = center
        self.width = 40
        self.height = 40
        self.textWidth = 100 
        self.rect = pygame.Rect(center[0]-self.width/2, center[1]-self.height/2, self.width, self.height)
        self.name = name
        self.tooltip = tooltip
        self.cost = cost
        self.amountIncrease = amountIncrease
        self.nameOfVariable = nameOfVariable
        self.prevUpgrade = prevUpgrade
        self.revealPurchase = revealPurchase
        self.game = game
        self.purchaseCount = 0
        self.unlocked = False
        font = "Arial"
        self.fontSize = 18
        self.font = pygame.font.SysFont(font, self.fontSize)
        
        self.textHeight = self.fontSize*4+16
        self.clicked = False
        self.prevClickTime = 0
        self.fullyBought = False
        self.ready = True
        self.totalPurchases = len(cost)
        self.textBGClr = (255,255,255)
        if imagePath != None:
            self.upgradeImageSurface = pygame.image.load(os.path.join("data/assets/upgradeAsset", imagePath)).convert_alpha()
        else:
            self.upgradeImageSurface = None

        
    def removeInitalPurchase(self):
        for i in range(0, int(self.purchaseCount)):
            self.cost.pop(0)

    def update(self, deltaTime):
        if len(self.cost) <= 0:
            self.fullyBought = True
        if self.prevUpgrade == None or self.prevUpgrade.purchaseCount >= self.revealPurchase:
            self.unlocked = True
        if self.ready == False:
            self.makeReady()

    def render(self, surface):
       self.draw(surface)
    
    def makeReady(self):
        if time.time() - self.prevClickTime > .05:
            self.ready = True

    def draw(self, surface):
        if len(self.cost)>0:
            pygame.Surface.fill(surface, (221, 221, 221), self.rect)
            pygame.draw.rect(surface, (84,84,84), self.rect, 2)
        else:
            pygame.Surface.fill(surface, (128, 128, 128), self.rect)
            pygame.draw.rect(surface, (84,84,84), self.rect, 2)
        if self.upgradeImageSurface:
            pygame.Surface.blit(surface, self.upgradeImageSurface, self.rect.topleft)

    
    def isHovering(self, surface):
        pos = pygame.mouse.get_pos()
        pos = (pos[0]/self.game.scaleFactor, pos[1]/self.game.scaleFactor)
        if self.rect.collidepoint(pos) and self.unlocked == True:
            self.drawTextBox(surface)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.prevClickTime = time.time()
                
                self.clicked = True

    def drawTextBox(self, surface):
        if len(self.cost) > 0:
            self.drawPurchaseTextBox(surface)
        else:
            self.drawCompleteTextBox(surface)

    def drawPurchaseTextBox(self, surface):
        

        nameText = pygame.font.Font.render(self.font, self.name, 1, (0,0,0), self.textBGClr )
        nameRect = nameText.get_rect()
        
        tooltipText = pygame.font.Font.render(self.font, self.tooltip, 1, (0,0,0), self.textBGClr )
        tooltipRect = tooltipText.get_rect()        
        
        costText = pygame.font.Font.render(self.font, "Cost: " + str(self.cost[0]), 1, (0,0,0), self.textBGClr )
        costRect = costText.get_rect()   
                
        totalPurchasesText = pygame.font.Font.render(self.font, str(int(self.purchaseCount)) + "/" + str(self.totalPurchases), 1, (0,0,0), self.textBGClr )
        totalPurchasesRect = totalPurchasesText.get_rect() 

        textWidth = tooltipText.get_size()[0]+10
        topLeft = (self.center[0]-textWidth/2, self.center[1]-100-self.textHeight/2)
        if topLeft[1] < 0:
            topLeft = (self.center[0]-textWidth/2, self.center[1]+self.textHeight/2)



        nameRect.topleft = (topLeft[0] + 5 , topLeft[1])
        tooltipRect.topleft = (topLeft[0] + 5, topLeft[1] + self.fontSize + 3)
        costRect.topleft = (topLeft[0] + 5, topLeft[1] + self.fontSize*2 + 6)   
        totalPurchasesRect.topleft = (topLeft[0] + 5, topLeft[1] + self.fontSize*3 + 9)
        
        textRect = pygame.Rect(topLeft[0], topLeft[1], textWidth ,self.textHeight)

        pygame.draw.rect(surface, self.textBGClr , textRect, 0 , 3)
        surface.blit(nameText, nameRect)
        surface.blit(tooltipText, tooltipRect)
        surface.blit(costText, costRect)
        surface.blit(totalPurchasesText, totalPurchasesRect)

    def drawCompleteTextBox(self, surface):
        

        nameText = pygame.font.Font.render(self.font, self.name, 1, (0,0,0), self.textBGClr )
        nameRect = nameText.get_rect()
        
        tooltipText = pygame.font.Font.render(self.font, self.tooltip, 1, (0,0,0), self.textBGClr )
        tooltipRect = tooltipText.get_rect()        
        
                
        totalPurchasesText = pygame.font.Font.render(self.font, "Complete", 1, (0,0,0), self.textBGClr )
        totalPurchasesRect = totalPurchasesText.get_rect() 

        textWidth = tooltipText.get_size()[0]+10
        topLeft = (self.center[0]-textWidth/2, self.center[1]-100-self.textHeight/2)
        if topLeft[1] < 0:
            topLeft = (self.center[0]-textWidth/2, self.center[1]+self.textHeight/2)

        nameRect.topleft = (topLeft[0] + 5 , topLeft[1])
        tooltipRect.topleft = (topLeft[0] + 5, topLeft[1] + self.fontSize + 3)
        totalPurchasesRect.topleft = (topLeft[0] + 5, topLeft[1] + self.fontSize*2 + 6)
        
        textRect = pygame.Rect(topLeft[0], topLeft[1], textWidth ,self.textHeight-self.fontSize-3)

        pygame.draw.rect(surface, self.textBGClr , textRect, 0 , 3)
        surface.blit(nameText, nameRect)
        surface.blit(tooltipText, tooltipRect)
        surface.blit(totalPurchasesText, totalPurchasesRect)
