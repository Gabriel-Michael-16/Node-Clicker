## To Package - C:\Personal Projects\Gamble Tree>python -m PyInstaller Game.py --onefile --noconsole --icon=icon.ico
import os, time, pygame 
from data.states.title import Title
import data.button

class Game():

    def __init__(self):
        pygame.init()
        self.gameWidth, self.gameHeight = 960, 540
        self.screenWidth, self.screenHeight = 960, 540
        self.scaleFactor = self.screenWidth / self.gameWidth
        self.gameCanvas = pygame.Surface((self.gameWidth,self.gameHeight))
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))
        self.running, self.playing = True, True
        self.dt, self.prevTime = 0, 0
        self.stateStack = []
        self.actions = []
        self.loadAssets()
        self.loadStates()

    def gameLoop(self):
        while self.playing:
            self.getDt()
            self.getEvents()
            self.update()
            self.render()

    def getEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.stateStack[-1].update(self.dt,self.actions)

    def render(self):
        self.stateStack[-1].render(self.gameCanvas)
        self.screen.blit(pygame.transform.scale(self.gameCanvas,(self.screenWidth,self.screenHeight)), (0,0))
        pygame.display.flip()
    
    def getDt(self):
        now = time.time()
        self.dt = now - self.prevTime
        if self.dt < 0.01667:
            self.dt = 0.01667
        self.prevTime = now
    
    def drawText(self, surface, text, colour, x, y):
        textSurface = self.font.render(text, True, colour)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        surface.blit(textSurface, textRect)

    def loadAssets(self):
        dataDir = os.path.join("data")
        assetsDir = os.path.join(dataDir, "assets")
        fontDir = os.path.join(assetsDir, "font")
        self.font = pygame.font.Font(os.path.join(fontDir, "04B_30__.TTF"), 20)
        
    def loadStates(self):
        self.titleScreen = Title(self)
        self.stateStack.append(self.titleScreen)
        
    def resetKeys(self):
        for action in self.actions:
            self.actions[action] = False




if __name__ == "__main__":
    g = Game()
    #write values from file here

    while g.running:
        g.gameLoop()