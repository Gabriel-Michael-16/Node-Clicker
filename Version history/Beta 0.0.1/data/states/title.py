from data.states.state import State
from data.states.roundState import RoundState
from data.states.upgradeState import UpgradeState
import pygame, os
import data.button as button

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        assetsDir = os.path.join("data", "assets")
        startButtonImg = pygame.image.load(os.path.join(assetsDir, "startBtn.jpg"))
        self.startButton = button.Button(100, game.gameHeight/2, startButtonImg, .3, 'enter', game)
        

    def update(self, deltaTime, actions):
        
        self.game.resetKeys()
    
    def render(self, surface):
        surface.fill((255,255,255))
        self.game.drawText(surface, "Node Clicker", (0,0,0), self.game.gameWidth/2, self.game.gameHeight/4 )
        self.startButton.render(surface)
        if self.startButton.action:
            #newState = RoundState(self.game)
            newState = UpgradeState(self.game)
            newState.enterState()