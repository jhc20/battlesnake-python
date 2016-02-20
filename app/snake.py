import json
    
class Snake:
    
    def __init__(self, snake_id, name, status, message, taunt, age, health, kills, coords, food):
        self.snake_id = snake_id
        self.name = name
        self.status = status
        self.message = message
        self.taunt = taunt
        self.age = age
        self.health = health
        self.coords = coords
        self.kills = kills
        self.food = food
