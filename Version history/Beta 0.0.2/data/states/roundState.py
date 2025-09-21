import pygame
from data.states.state import State
from data.states.analysisState import AnalysisState
from data.particles import Particle
from data.button import Button
import data.node as node, data.player as player
import numpy as np, math, random
import time
import keyboard
import os


class RoundState(State):
    def __init__(self, game, variables):
        State.__init__(self,game)
        font = "Arial"
        fontSize = 32
        self.money = 0
        self.font = pygame.font.SysFont(font, fontSize)
        
        #self.backgroundImg = pygame.image.load(os.path.join(self.game.assetsDir, "binary_tree.png"))
        #self.nodeImg = pygame.image.load(os.path.join(self.game.assetsDir, "circleNode.png"))
        startNode= node.Node(1, (self.game.gameWidth/2,self.game.gameHeight*0.85), "Beginning", game)
        self.player = player.Player(game)
        self.nodes = []
        self.nodes.append(startNode)
        self.root = startNode
        self.current = startNode.circleCenter
        self.lines = []
        self.begun = False
        self.normalisedVector = (0,0)
        self.particleGroup = pygame.sprite.Group()
        self.moving = False
        self.destination = startNode.circleCenter
        self.needNodes = True
        self.scaleFactor = variables["moveSpeedFactor"]
        self.maxNodes = variables["maxNodes"]
        self.count = 0
        # self.variables = variables
        self.multiplier = variables["multiplier"]
        self.maxValue = variables["maxValue"]
        self.minValue = variables["minValue"]
        self.doubleChance = variables["doubleChance"]
        self.doubleMaxTime = variables["doubleMaxTime"]
        self.noNegativeMaxTime = variables["noNegativeMaxTime"]
        self.noNegativeChance = variables["noNegativeChance"]
        self.timeFreezeMaxTime = variables["timeFreezeMaxTime"]
        self.timeFreezeChance = variables["timeFreezeChance"]
        self.maxTime = variables["maxTime"]
        self.timeLeft = self.maxTime
        self.doubleMoneyTimeleft = 0
        self.noNegativeTimeleft = 0
        self.timeFreezeTimeleft = 0
        self.finished = False
        self.analysis = False
        self.double = False
        self.doubleStartTime = 0
        self.noNegative = False
        self.noNegativeStartTime = 0 
        self.timeFreeze = False
        self.timeFreezeStartTime = 0
        startButtonImg = pygame.image.load("data/assets/images/upgradeButton1-export.png")
        self.analysisButton = Button(300+75, 329, startButtonImg, 1, 'tab', game)
    #     self.readValues()

    
    # def readValues(self):
    #     f = open("playerInfo.txt", "r")
    #     lines = f.readlines()
    #     for line in lines:
    #         if line.find("maxTime: ") != -1:
    #             self.variables["maxTime"] = float(line.replace("maxTime: ", ""))
    #     self.timeLeft = self.variables["maxTime"]
    #     f.close()

    def update(self, deltaTime, actions):
        while len(self.particleGroup.sprites()) < 450:
            self.createBackgroundParticles()
        if pygame.mouse.get_pressed()[2]:
            self.exitProtocol() #Create exit function that saves money
        self.particleGroup.update(deltaTime)
        if self.begun and not self.analysis:
            self.roundTimer(deltaTime)
        self.particleSynchroniseMovement()
        
        
        
        self.earlyExit()

        if not self.analysis:
            self.gameLogic(deltaTime)
            self.doubleMoneyPowerup()
            self.noNegativePowerup()
            self.timeFreezePowerup()
            self.nodeClicked()
            self.getCursor()

    def render(self, surface):
        surface.fill((17,17,17)) #background
        self.drawBackgroundParticles(surface)
        self.drawMoneyBox(surface)
        self.drawTimeBox(surface)
        self.drawDoubleMoneyBox(surface)
        self.drawNoNegativeMoneyBox(surface)
        self.drawTimeFreezeBox(surface)
        self.drawNodes(surface)
        if self.analysis:
            self.drawAnalysisBox(surface)

    def particleSynchroniseMovement(self):
        newDir = pygame.math.Vector2(-self.normalisedVector[0],-self.normalisedVector[1])
        for particle in self.particleGroup:
            if self.moving == True:
                particle.direction = newDir
                if particle.maxSpeed == "max":
                    particle.speed = random.randint(80,100)
                elif particle.maxSpeed == "mid":
                    particle.speed = random.randint(40,60)
                elif particle.maxSpeed == "min":
                    particle.speed = random.randint(0,20)   
            else:
                particle.direction = particle.prevDirection
                particle.speed = random.randint(1,8)

    def earlyExit(self):
        if keyboard.is_pressed('enter'):
            time.sleep(.1)
            self.exitProtocol()

    def exitProtocol(self):
        self.moving = False
        self.analysis = True
        self.finished = True
        #self.exitState()

    def drawAnalysisBox(self, surface):
        pygame.draw.rect(surface, (255,255,255), (300, 50, self.game.gameWidth-600, self.game.gameHeight-100), 0, 5)
        moneyAnalysisSurface = self.font.render("Money:               " + str(self.money), True, (0,0,0))
        analysisRect = moneyAnalysisSurface.get_rect()
        analysisRect.topleft = (330,150)
        multiplierSurface = self.font.render("Multiplier:           " + str(round(self.multiplier, 2)), True, (0,0,0))
        multiplierRect = multiplierSurface.get_rect()
        multiplierRect.topleft = (330,185)
        totalSurface = self.font.render("Total:                  " + str(math.trunc(self.multiplier*self.money)), True, (0,0,0))
        totalRect = totalSurface.get_rect()
        totalRect.topleft = (330,220)
        surface.blit(moneyAnalysisSurface, analysisRect)
        surface.blit(multiplierSurface, multiplierRect)
        surface.blit(totalSurface, totalRect)

        self.analysisButton.render(surface)
        if self.analysisButton.action:
            self.analysis = False
            self.exitState()



    def createBackgroundParticles(self):
        pos = (random.randint(-50, self.game.gameWidth+50), random.randint(-50, self.game.gameHeight+50))
        colour = (169,169,169)
        direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        direction = direction.normalize()
        speed = random.randint(1, 8)
        Particle(self.particleGroup, pos, colour, direction, speed, self.game.gameWidth, self.game.gameHeight)

    def drawBackgroundParticles(self, surface):
        self.particleGroup.draw(surface)
        pass
        
    def doubleMoneyPowerup(self):
        timePassed = time.time() - self.doubleStartTime
        if timePassed > self.doubleMaxTime or time.time()-self.doubleStartTime > 1000:
            self.double = False
        else:
            self.double = True
        self.doubleMoneyTimeleft = self.doubleMaxTime - timePassed
    
    def noNegativePowerup(self):
        timePassed = time.time() - self.noNegativeStartTime
        if  timePassed > self.noNegativeMaxTime or time.time() - self.noNegativeStartTime > 1000:
            self.noNegative = False
        else:
            self.noNegative = True
        self.noNegativeTimeleft = self.noNegativeMaxTime - timePassed

    def timeFreezePowerup(self):
        timePassed = time.time() - self.timeFreezeStartTime
        if  timePassed > self.timeFreezeMaxTime or time.time() - self.timeFreezeStartTime > 1000:
            self.timeFreeze = False
        else:
            self.timeFreeze = True
        self.timeFreezeTimeleft = self.timeFreezeMaxTime - timePassed

    def nodeClicked(self):
        for node in self.nodes:
            isInScreen = node.circleCenter[1] - node.radius < self.game.gameHeight
            if(isInScreen):
                if node.clicked and node in self.root.children:
                    for othernode in self.root.children:
                        if othernode != node:
                            index = self.nodes.index(othernode)
                            self.nodes.pop(index)
                    if node.value == "x2":
                        self.doubleStartTime = time.time()
                        self.double = True
                    elif node.value == "Only Positive":
                        self.noNegativeStartTime = time.time()
                        self.noNegative = True
                    elif node.value == "Time Freeze":
                        self.timeFreezeStartTime = time.time()
                        self.timeFreeze = True
                    elif self.double == True:
                        self.money = self.money + node.value * 2
                    else:
                        self.money = self.money + node.value
                    self.createLine(self.root.circleCenter, node.circleCenter)
                    self.root = node
                    self.destination = node.circleCenter
                    self.moving = True
            else:
                index = self.nodes.index(node)
                self.nodes.pop(index)

    def drawNodes(self, surface):
        for node in self.nodes:
            node.draw(surface)

    def drawLines(self, surface):
        for line in self.lines:
            if min(line[0][1], line[1][1]) < self.game.gameHeight:
                pygame.draw.line(surface, (150,150,150), line[0], line[1])
            else:
                index  = self.lines.index(line)
                self.lines.pop(index) 

    def drawMoneyBox(self, surface):
        pygame.draw.rect(surface, (0, 100, 255), (self.game.gameWidth-150, 0, 960, 50))
        moneySurface = self.font.render(str(self.money), True, (0,0,0))
        moneyRect = moneySurface.get_rect()
        moneyRect.topleft = (self.game.gameWidth-150,0)
        surface.blit(moneySurface, moneyRect)

    def drawFrameRate(self, surface):
        frameRateSurface = self.font.render("FPS: " + str(round(1/self.game.dt)), True, (14,60,187))
        frameRateRect = frameRateSurface.get_rect()
        frameRateRect.topleft = (50,50)
        surface.blit(frameRateSurface, frameRateRect)

    def drawTimeBox(self, surface):
        timeProportion = self.timeLeft/self.maxTime  
        self.drawTimeBars(surface, timeProportion, self.game.gameWidth/2-100, self.game.gameHeight-35, 200, 30)
    
    def drawDoubleMoneyBox(self, surface):
        timeProportion = self.doubleMoneyTimeleft/self.doubleMaxTime
        if timeProportion > 0:
            self.drawTimeBars(surface, timeProportion, self.game.gameWidth-220, self.game.gameHeight-145, 200, 30)
        
    def drawNoNegativeMoneyBox(self, surface):
        timeProportion = self.noNegativeTimeleft/self.noNegativeMaxTime
        if timeProportion > 0:
            self.drawTimeBars(surface, timeProportion, self.game.gameWidth-220, self.game.gameHeight-95, 200, 30)
    
    def drawTimeFreezeBox(self, surface):
        timeProportion = self.timeFreezeTimeleft/self.timeFreezeMaxTime
        if timeProportion > 0:
            self.drawTimeBars(surface, timeProportion, self.game.gameWidth-220, self.game.gameHeight-45, 200, 30)

    def drawTimeBars(self, surface, timeProportion, positionX, positionY, width, height):
        timerBorderRect = pygame.Rect(positionX, positionY, width, height)
        timerRect = pygame.Rect(positionX, positionY + height/6, width*timeProportion, 20)
        pygame.draw.rect(surface, (127,127,127), timerBorderRect)
        if timeProportion > 0.5:
            pygame.draw.rect(surface, (int(40+215*(1-timeProportion)*2),int(255-33*(1-timeProportion)*2),0), timerRect)
        elif timeProportion > 0:
            pygame.draw.rect(surface, (int(255-11*(1-timeProportion)*2),int(222*timeProportion*2),0), timerRect)

    def roundTimer(self, deltaTime):
        if not self.timeFreeze:
            self.timeLeft-= deltaTime
        if self.timeLeft < 0:
            self.exitProtocol() #Create exit function that saves money

        
    def gameLogic(self, deltaTime):
        if self.moving:
            if self.begun == False:
                self.begun = True
            self.moveToDestination(self.destination, deltaTime)
        else:
            n = random.randint(2,self.maxNodes)
            if self.needNodes:
                for i in range(n):
                    self.createNode()
                self.needNodes = False       
    
    def getCursor(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            print(pos)

    def moveToDestination(self, destination, deltaTime):
        self.normalisedVector = self.findVector(self.current, destination, deltaTime)
        self.moveNodes(self.normalisedVector)
        return

    def findVector(self, initial, destination, deltaTime):
        vector = tuple(np.subtract(destination, initial))
        magnitude = math.sqrt((vector[0]**2+vector[1]**2))
        if magnitude < 5 * (self.scaleFactor/400):
            self.moving=False
            self.needNodes=True
            self.current=self.root.circleCenter
            return (0,0)
        normalisedVector =  ((vector[0]/magnitude)*deltaTime*self.scaleFactor, (vector[1]/magnitude)*deltaTime*self.scaleFactor)
        return normalisedVector
    
    def moveNodes(self, normalisedVector):
        for line in self.lines:
            
            a = tuple(np.subtract(line[0], normalisedVector))
            b = tuple(np.subtract(line[1], normalisedVector))
            index = self.lines.index(line)
            self.lines.pop(index)
            self.lines.append((a,b))
        for node in self.nodes:
            node.circleCenter = tuple(np.subtract(node.circleCenter, normalisedVector))
        self.current = np.add(self.current, normalisedVector)
        return

    def createNode(self):
        randomX1 = random.randint(100, self.game.gameWidth-100)
        randomY1 = random.randint(50, 300)
        isDouble = random.randint(1,100) <= self.doubleChance
        isNoNegative = random.randint(1,100) <= self.noNegativeChance
        isTimeFreeze = random.randint(1,100) <= self.timeFreezeChance
        if isDouble:
            randomValue = "x2"
        elif isNoNegative:
            randomValue = "Only Positive"
        elif isTimeFreeze:
            randomValue = "Time Freeze"
        elif self.noNegative:
            randomValue = self.maxValue
        else:
            randomValue = random.randint(self.minValue, self.maxValue)
        for otherNode in self.root.children:
            #circleOverlap = (randomX1-otherNode.circleCenter[0] < otherNode.radius*2 and randomX1-otherNode.circleCenter[0] > -otherNode.radius*2) or (randomY1-otherNode.circleCenter[1] < otherNode.radius*2 and randomY1-otherNode.circleCenter[1] > -otherNode.radius*2)
            vector = tuple(np.subtract((randomX1,randomY1), otherNode.circleCenter))
            magnitude = math.sqrt((vector[0]**2+vector[1]**2))
            if magnitude < otherNode.radius*2:
                self.createNode()
                return
        child = node.Node(randomValue, (randomX1,randomY1), str(randomValue), self.game)
        self.nodes.append(child)
        self.root.children.append(child)
        return

    def createLine(self, start, end):
        line = (start, end)
        self.lines.append(line)