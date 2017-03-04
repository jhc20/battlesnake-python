import json
# from SnakeStates import SnakeState

    
class Snake(object):
    def __init__(self):
        # self.curState = SnakeState()
        self.currTaunt = 'meow'
        self.ourSnake = {}
        self.headOfOurSnake = None
        self.ourSnake = None
        self.otherSnakes = []
        # self.curState.setState()
        # print type(self.curState)
        return



# Old code from inside the snake Object
# Being ignored for now
    # def __init__(self, snake_id, name, status, message, taunt, age, health, coords, kills):
    #     # self.snake_id = snake_id
    #     # self.name = name
    #     # self.status = status
    #     # self.message = message
    #     # self.taunt = taunt
    #     # self.age = age
    #     # self.health = health
    #     # self.coords = coords
    #     # self.kills = kills
