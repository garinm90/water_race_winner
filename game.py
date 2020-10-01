class GameState():
    name = 'state'
    allowed = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def switch(self, state):
        if state.name in self.allowed:
            print('Current: ', self, '-> switched to new state -> ',
                  state.name)
            self.__class__ = state
        else:
            print('Current: ', self, ' -> switching to ',
                  state.name, 'not_possible')


class Attract(GameState):
    """ Sets the game state into Attract mode after recieving a requests from GameOver
    """
    name = "Attract"
    allowed = ['GameStart']


class GameOver(GameState):
    """ Sets the game state into GameOver mode after recieving a requests from GameStart
    """
    name = "GameOver"
    allowed = ['Attract']


class GameStart(GameState):
    """ Sets the game state into GameStart mode after recieving a requests from Attract
    """
    name = "GameStart"
    allowed = ['GameOver']

class Game():
    def __init__(self):
        self.state = Attract()

    def change(self, state):
        self.state.switch(state)

    def __repr__(self):
        return self.state.name