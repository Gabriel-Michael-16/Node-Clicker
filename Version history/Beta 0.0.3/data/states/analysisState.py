from data.states.state import State
import pygame

class AnalysisState(State):
    def __init__(self, game):
        State.__init__(self, game)
        font = "Arial"
        fontSize = 32
        self.money = 0
        self.font = pygame.font.SysFont(font, fontSize)

    def update(self, deltaTime, actions):
        pass

    def render(self, surface):
        surface.fill(0,0,0)
        self.drawRoundBox(surface)

    def drawRoundBox(self, surface):
        pygame.draw.rect(surface, (255,255,255), (300, 200, 400, self.game.gameHeight-50), 0, 5)
        moneySurface = self.font.render(str(self.money), True, (0,0,0))
        moneyRect = moneySurface.get_rect()
        moneyRect.center = (self.game.gameWidth/2,500)
        surface.blit(moneySurface, moneyRect)