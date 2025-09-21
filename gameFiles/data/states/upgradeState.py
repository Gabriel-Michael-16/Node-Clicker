from data.states.state import State
from data.states.roundState import RoundState
from data.button import Button
from data.upgrades import Upgrades
import pygame, os

class UpgradeState(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.variables = {
            "maxTime": 7.0,
            "multiplier": 1.0,
            "maxValue": 10,
            "minValue": -10,
            "winState": 0,
            "moveSpeedFactor": 400,
            "maxNodes": 2,
            "doubleChance": 0,
            "doubleMaxTime": 5,
            "noNegativeMaxTime": 5,
            "noNegativeChance": 0,
            "timeFreezeMaxTime": 5,
            "timeFreezeChance": 0,
            "money": 500000
        }
        self.upgrades = {
            "Time Increase 1": 0.0,
            "Time Increase 2": 0.0,
            "Time Increase 3": 0.0,
            "Final Button": 0.0,
            "Multiplier 1": 0.0,
            "Multiplier 2": 0.0,
            "Max Value 1": 0.0,
            "Max Value 2": 0.0,
            "Max Value 3": 0.0,
            "Min Value 1": 0.0,
            "Min Value 2": 0.0,
            "Min Value 3": 0.0,
            "Movement Speed 1": 0.0,
            "Movement Speed 2": 0.0,
            "Double Chance 1": 0.0,
            "Max Nodes 1": 0.0,
            "Max Nodes 2": 0.0,
            "Max Nodes 3": 0.0,
            "Double Time 1": 0.0,
            "Double Time 2": 0.0,
            "Double Time 3": 0.0,
            "Best Nodes Possible 1": 0.0,
            "Best Nodes Possible 2": 0.0,
            "Best Nodes Possible 3": 0.0,
            "Time Freeze 1": 0.0,
            "Time Freeze 2": 0.0,
            "Time Freeze 3": 0.0,
            "Time Freeze 4": 0.0,
        }
        self.upgradeButtons = []
        self.newState = None
        self.roundButtonImage = pygame.image.load("data/assets/images/nextButton1.png")
        self.roundButton = Button(game.gameWidth-144, game.gameHeight-87, self.roundButtonImage, 0.4, 'shift', game)
        self.center =  (self.game.gameWidth/2,self.game.gameHeight/2)
        font = "Arial"
        self.fontSize = 32
        self.font = pygame.font.SysFont(font, self.fontSize)
        self.titleFont = pygame.font.SysFont(font, 48)
        self.subFont = pygame.font.SysFont(font, 22)
        self.count = 0
        #self.upgradeSound = pygame.mixer.Sound("data/assets/sounds/upgradeButtonSound.wav")
        self.upgradeSound = pygame.mixer.Sound("data/assets/sounds/Get Upgrade.wav")
        #pygame.mixer.music.load('data/assets/sounds/Time - Background1.mp3')
        #pygame.mixer.music.play(-1)
        self.createUpgrades()
        self.readFromFile()
        self.paused = False
        self.set = False
        
    
    
    def update(self, deltaTime, actions):
        if self.set == False:
            self.thisState = self.game.stateStack[-1]
            self.set = True
        self.addMoney()
        self.updateUpgrades(deltaTime)
        if self.paused:
            print("paused")
            self.restartMusic()


    def render(self, surface):
        surface.fill((31,55,93))
        self.drawUpgrades(surface)
        self.drawRoundButton(surface)
        self.drawMoneyBox(surface)
        if self.variables["winState"] >= 1:
            self.drawFinalScreen(surface)

    def readFromFile(self):
        f = open("data/playerInfo.txt")
        string = f.readline()
        self.read(self.variables, string, f)
        self.read(self.upgrades, string, f)
        print(self.upgrades["Time Increase 1"])
        for i in range(0,len(self.upgradeButtons)): 
            if self.upgradeButtons[i].name in self.upgrades:
                self.upgradeButtons[i].purchaseCount = self.upgrades[self.upgradeButtons[i].name]
            self.upgradeButtons[i].removeInitalPurchase()
        f.close()

    def read(self, dictionary, string, file):
        while string != "":
            for x in self.variables:
                if x in string:
                    string = string.replace((str(x) + ": "), "")
                    string = string.rstrip(('\n'))
                    self.variables[x] = float(string)
            for y in self.upgrades:
                if y in string:
                    string = string.replace((str(y) + ": "), "")
                    string = string.rstrip(('\n'))
                    self.upgrades[y] = float(string)
            
            string = file.readline()


    def writeVariables(self):
        f = open("data/playerInfo.txt", "w")
        for x in self.variables:
            f.write(str(x) + ": " + str(self.variables[x]) + "\n")
        f.close()

    def writeUpgrades(self):
        f = open("data/playerInfo.txt", "a")
        for x in self.upgrades:
            f.write(str(x) + ": " + str(self.upgrades[x]) + "\n")
        f.close()

    def restartMusic(self):
        print(self.game.stateStack[-1])
        print(self.thisState)
        if self.game.stateStack[-1] == self.thisState:
            print("True")
            self.paused = False
            pygame.mixer.music.load('data/assets/sounds/Time - Background1.mp3')
            pygame.mixer.music.play(-1)

    def updateUpgrades(self, deltaTime):
        for upgrade in self.upgradeButtons:
            upgrade.update(deltaTime)

    def drawRoundButton(self, surface):
        self.roundButton.render(surface)
        if self.roundButton.action == True:
            pygame.mixer.music.pause()
            self.writeVariables()
            self.writeUpgrades()
            self.newState = RoundState(self.game, self.variables)

            self.paused = True
            self.newState.enterState()
        self.roundButton.action = False
    
    def drawFinalScreen(self, surface):
        string1 = "Game complete"
        string2 = "Thank you for playing!"
        background = pygame.Rect(self.game.gameWidth/4, self.game.gameHeight/4, self.game.gameWidth/2, self.game.gameHeight/2)
        pygame.draw.rect(surface, (255,255,255), background)
        winSurface1 = self.titleFont.render(string1, True, (0,0,0))
        winSurface2 = self.subFont.render(string2, True, (0,0,0))
        winRect1 = winSurface1.get_rect()
        winRect1.center = (480, 252)
        surface.blit(winSurface1, winRect1)
        winRect2 = winSurface2.get_rect()
        winRect2.center = (480, 288)
        surface.blit(winSurface2, winRect2)

    def drawMoneyBox(self, surface):
        pygame.draw.rect(surface, (0, 100, 255), (self.game.gameWidth-150, 0, 960, 50))
        moneySurface = self.font.render(str(self.variables["money"]), True, (0,0,0))
        moneyRect = moneySurface.get_rect()
        moneyRect.topleft = (self.game.gameWidth-150,0)
        surface.blit(moneySurface, moneyRect)
    
    def addMoney(self):
        if self.newState != None:
            if self.newState.finished == True:
                self.variables["money"] += self.newState.money * self.variables["multiplier"]
                print(self.newState.money)
                print(self.variables["money"])
                self.newState.finished = False
                self.resetClicks()
        
    def resetClicks(self):
        for upgrade in self.upgradeButtons:
            upgrade.clicked = False


    def getCursor(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            print(str(pos) + str(self.count))
            self.count+=1

    def drawUpgrades(self, surface):
        for upgrade in self.upgradeButtons:
            if upgrade.unlocked:
                upgrade.draw(surface)
                if upgrade.clicked == True and upgrade.fullyBought == False and self.variables["money"] >= upgrade.cost[0] and upgrade.ready == True:
                    self.variables[upgrade.nameOfVariable] += float(upgrade.amountIncrease)
                    pygame.mixer.Sound.play(self.upgradeSound)
                    self.variables["money"] -= upgrade.cost[0]
                    upgrade.cost.pop(0)
                    upgrade.purchaseCount += 1
                    self.upgrades[upgrade.name] += 1
                    upgrade.clicked = False
                    upgrade.ready = False
                else:
                    upgrade.clicked = False

        for upgrade in self.upgradeButtons:
            upgrade.isHovering(surface)


    def createUpgrades(self):
        timeIncrease1 = Upgrades(self.center, "Time Increase 1", "Increases time by 0.5 seconds", 0.5, [40, 60, 70, 80, 100], "maxTime", 2, None, "HourglassBlack.png", self.game)
        self.upgradeButtons.append(timeIncrease1)
        timeIncrease2 = Upgrades((self.center[0]-75, self.center[1]), "Time Increase 2", "Increases time by 1.5 seconds", 1.5, [200, 220, 240, 260], "maxTime", 5, timeIncrease1, "HourglassRed.png", self.game)
        self.upgradeButtons.append(timeIncrease2)
        timeIncrease3 = Upgrades((self.center[0]-150, self.center[1]), "Time Increase 3", "Increases time by 3 seconds", 3, [300, 320, 340, 360], "maxTime",4, timeIncrease2, "HourglassGreen.png", self.game)
        self.upgradeButtons.append(timeIncrease3)

        gameComplete = Upgrades((self.center[0]-300, self.center[1]), "Final Button", "Purchase this to win", 1, [25000], "winState", 4, timeIncrease3, "FinishFlag.png", self.game)
        self.upgradeButtons.append(gameComplete)

        multiplier1 = Upgrades((self.center[0], self.center[1]-80), "Multiplier 1", "Gives a 5% multiplier to the final count", 0.05, [500, 550, 600, 650], "multiplier",5, timeIncrease1, "Multiplier1.png", self.game)
        self.upgradeButtons.append(multiplier1)
        multiplier2 = Upgrades((self.center[0], self.center[1]-160), "Multiplier 2", "Gives a 10% multiplier to the final count", 0.1, [2000, 2200, 2400], "multiplier",4, multiplier1, None, self.game)
        self.upgradeButtons.append(multiplier2)

        maxValue1 = Upgrades((self.center[0]+75, self.center[1]), "Max Value 1", "Increases the maximum value a button can appear as by 10", 10, [100,200,300], "maxValue",3, timeIncrease1, "MaxUp1.png", self.game)
        self.upgradeButtons.append(maxValue1)
        maxValue2 = Upgrades((self.center[0]+150, self.center[1]), "Max Value 2", "Increases the maximum value a button can appear as by 10", 10, [400,450,500], "maxValue",3, maxValue1, "MaxUp2.png", self.game)
        self.upgradeButtons.append(maxValue2)
        maxValue3 = Upgrades((self.center[0]+225, self.center[1]), "Max Value 3", "Increases the maximum value a button can appear as by 10", 10, [550,575,600], "maxValue",3, maxValue2, "MaxUp3.png", self.game)
        self.upgradeButtons.append(maxValue3)

        minValue1 = Upgrades((self.center[0]+75, self.center[1]+80), "Min Value 1", "Reduses the minimum value a button can appear as by 10", 10, [600,650,700], "minValue",2, maxValue3, "MinUp1.png", self.game)
        self.upgradeButtons.append(minValue1)
        minValue2 = Upgrades((self.center[0]+150, self.center[1]+80), "Min Value 2", "Reduses the minimum value a button can appear as by 10", 10, [720,770,820], "minValue",3, minValue1, "MinUp2.png", self.game)
        self.upgradeButtons.append(minValue2)
        minValue3 = Upgrades((self.center[0]+225, self.center[1]+80), "Min Value 3", "Reduses the minimum value a button can appear as by 10", 10, [850,1000,1150], "minValue",3, minValue2, "MinUp3.png", self.game)
        self.upgradeButtons.append(minValue3)

        moveSpeed1 = Upgrades((self.center[0], self.center[1]+80), "Movement Speed 1", "Increases your movement speed by 15", 15, [100,150,200,250], "moveSpeedFactor",2, timeIncrease1, "BootsBlack.png", self.game)
        self.upgradeButtons.append(moveSpeed1)
        moveSpeed2 = Upgrades((self.center[0]-75, self.center[1]+80), "Movement Speed 2", "Increases your movement speed by 20", 20, [500,525,550], "moveSpeedFactor",4, moveSpeed1, "BootsRed.png", self.game)
        self.upgradeButtons.append(moveSpeed2)

        doubleChance1 = Upgrades((self.center[0]-75, self.center[1]-80), "Double Chance 1", "Creates x2 powerup nodes with 1% chance of occuring", 1, [700,800,900,1000], "doubleChance",3, multiplier1, "DoubleCoin.png", self.game)
        self.upgradeButtons.append(doubleChance1)

        maxNodes1 = Upgrades((self.center[0]-75, self.center[1]-160), "Max Nodes 1", "Increase the total number of nodes by 1", 1, [1200], "maxNodes",1, doubleChance1, None, self.game)
        self.upgradeButtons.append(maxNodes1)
        maxNodes2 = Upgrades((self.center[0]-150, self.center[1]-160), "Max Nodes 2", "Increase the total number of nodes by 1", 1, [1600], "maxNodes",1, maxNodes1, None, self.game)
        self.upgradeButtons.append(maxNodes2)
        maxNodes3 = Upgrades((self.center[0]-225, self.center[1]-160), "Max Nodes 3", "Increase the total number of nodes by 1", 1, [2000], "maxNodes",1, maxNodes2, None, self.game)
        self.upgradeButtons.append(maxNodes3)

        doubleTime1 = Upgrades((self.center[0]+75, self.center[1]-80), "Double Time 1", "Increases time of x2 powerup by 2 seconds", 2, [700], "doubleMaxTime",4, multiplier1, "DoubleCoinTime1.png", self.game)
        self.upgradeButtons.append(doubleTime1)
        doubleTime2 = Upgrades((self.center[0]+150, self.center[1]-80), "Double Time 2", "Increases time of x2 powerup by 4 seconds", 4, [1000], "doubleMaxTime",1, doubleTime1, "DoubleCoinTime2.png", self.game)
        self.upgradeButtons.append(doubleTime2)
        doubleTime3 = Upgrades((self.center[0]+225, self.center[1]-80), "Double Time 3", "Increases time of x2 powerup by 6 seconds", 6, [2000], "doubleMaxTime",1, doubleTime2, "DoubleCoinTime3.png", self.game)
        self.upgradeButtons.append(doubleTime3)

        # noNegative1 = Upgrades((self.center[0]+75, self.center[1]-160), "Best Nodes Possible 1", "Gives max value nodes For the time period", 1, [10000], "noNegativeChance",1, multiplier2, None, self.game)
        # self.upgradeButtons.append(noNegative1)
        # noNegative2 = Upgrades((self.center[0]+150, self.center[1]-160), "Best Nodes Possible 2", "Increases time of best nodes powerup by 2 seconds", 1, [10000], "noNegativeMaxTime",1, noNegative1, None, self.game)
        # self.upgradeButtons.append(noNegative2)
        # noNegative3 = Upgrades((self.center[0]+225, self.center[1]-160), "Best Nodes Possible 3", "Increases time of best nodes powerup by 4 seconds", 1, [10000], "noNegativeMaxTime",1, noNegative2, None, self.game)
        # self.upgradeButtons.append(noNegative3)

        timeFreeze1 = Upgrades((self.center[0], self.center[1]+160), "Time Freeze 1", "Creates time freeze powerup with 1% chance of occuring", 1, [400], "timeFreezeChance",4, moveSpeed1, "SnowFlakeAsset.png", self.game)
        self.upgradeButtons.append(timeFreeze1)
        timeFreeze2 = Upgrades((self.center[0]-75, self.center[1]+160), "Time Freeze 2", "Increases length of freeze by 1 second", 1, [600,700,800], "timeFreezeMaxTime",1, timeFreeze1, "SnowFlakeRedTest.png", self.game)
        self.upgradeButtons.append(timeFreeze2)
        timeFreeze3 = Upgrades((self.center[0]-150, self.center[1]+160), "Time Freeze 3", "Increases length of freeze by 1 seconds", 1, [1500,1600,1700], "timeFreezeMaxTime",3, timeFreeze2, "SnowFlakeAssetYellow.png", self.game)
        self.upgradeButtons.append(timeFreeze3)
        timeFreeze4 = Upgrades((self.center[0]-225, self.center[1]+160), "Time Freeze 4", "Increases chance of occuring by 1%", 1, [2000,2500,3000], "timeFreezeChance",3, timeFreeze3, "SnowFlakeAssetGreen.png", self.game)
        self.upgradeButtons.append(timeFreeze4)
