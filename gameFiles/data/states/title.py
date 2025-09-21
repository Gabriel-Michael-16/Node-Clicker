from data.states.state import State
from data.states.roundState import RoundState
from data.states.upgradeState import UpgradeState
import pygame, os
import data.button as button

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)

        startButtonImg = pygame.image.load("data/assets/images/startButton2.png")
        self.startButton = button.Button(100, game.gameHeight/2, startButtonImg, .25, 'enter', game)
       # pygame.mixer.music.load('data/assets/sounds/ComingOfAge - Background2.mp3')
        pygame.mixer.music.load('data/assets/sounds/Time - Background1.mp3')
        pygame.mixer.music.play(-1)
        
        

    def update(self, deltaTime, actions):
        
        self.game.resetKeys()
    
    def render(self, surface):
        surface.fill((255,255,255))
        icon = pygame.image.load('data/assets/upgradeAsset/DoubleCoin.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Node Clicker")
        self.game.drawText(surface, "Node Clicker", (0,0,0), self.game.gameWidth/2, self.game.gameHeight/4 )
        self.startButton.render(surface)
        if self.startButton.action:
            #newState = RoundState(self.game)
            newState = UpgradeState(self.game)
            newState.enterState()