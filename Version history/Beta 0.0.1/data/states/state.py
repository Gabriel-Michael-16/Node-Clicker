class State:
    def __init__(self, game):
        self.game = game
        self.prevState = None

    def update(self, deltaTime, actions):
        pass
    def render(self, surface):
        pass

    def enterState(self):
        if len(self.game.stateStack) > 1:
            self.prevState = self.game.stateStack[-1]
        self.game.stateStack.append(self)
    
    def exitState(self):
        self.game.stateStack.pop()