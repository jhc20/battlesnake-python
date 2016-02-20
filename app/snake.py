import json
    
class Snake:
    
    def __init__(self, snake_id, name, status, message, taunt, age, health, coords, kills):
        self.snake_id = snake_id
        self.name = name
        self.status = status
        self.message = message
        self.taunt = taunt
        self.age = age
        self.health = health
        self.coords = coords
        self.kills = kills
