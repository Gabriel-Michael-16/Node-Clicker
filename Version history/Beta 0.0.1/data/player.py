class Player:

    def __init__(self, game):
        self.game = game
        self.money = 0
        self.currentFrame, self.lastFrameUpdate = 0, 0

    def update(self, deltaTime, actions):
        pass