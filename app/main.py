import bottle
import os
import json


''' 
Example Recieved Snake Object

{
    "id": "1234-567890-123456-7890",
    "name": "Well Documented Snake",
    "status": "alive",
    "message": "Moved north",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ,]
    "kills": 4,
    "food": 12,
    "gold": 2
}

'''

def directionsCanGo(mapdata, ourSnake, mapHeight, mapLength ):
    #if len(ourSnake.coords) == 0:
    #    return
    canGo = ['north', 'west', 'south', 'east']
    # Code to decide which dirs we can go
    head = ourSnake['coords'][0]
    #length = len(ourSnake.coords)
    
    #-----WALLS-----
    
    #if head co-ord x is 0, cant move north
    if head[0] == 0:
        canGo.remove('north')
    
    #if head co-ord x is height-1 cant move south
    if head[0] == mapHeight-1:
        canGo.remove('south')
        
    #if head co-ord y is 0, cant move west
    if head[1] == 0:
        canGo.remove('west')
        
    #if head co-ord y is  width - 1 cant more east 
    if head[1] == mapWidth-1:
        canGo.remove('east')
    
    #-----Ourselves-----
    '''
    for coord in ourSnake.coords:
        if coord == head:
            continue
        if (coord[0] - head[0] == 1) and (coord[1] - head[1] == 0):
            canGo.remove('south')
        if (coord[1] - head[1] == 1) and (coord[0] - head[0] == 0):
            canGo.remove('east')
        if (coord[0] - head[0] == -1) and (coord[1] - head[1] == 0):
            canGo.remove('north')
        if (coord[1] - head[1] == -1) and (coord[0] - head[0] == 0):
            canGo.remove('west')
    '''
    return canGo

ourSnakeId = "902f27c7-400a-4316-9672-586bf72bee07"
snakes = []
food = []
movementLeft = 0
movementRight = 0
movementUp = 0
movementDown = 0


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    #head_url = '%s://%s/static/head.png' % (
    #    bottle.request.urlparts.scheme,
    #    bottle.request.urlparts.netloc
    #)

    return {
        'color': '#4099ff',
        'head': "http://i.imgur.com/uajfGft.png"
    }


''' 
Object recieved for /start
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 0,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [],
    "walls": [],  // Advanced Only
    "gold": []    // Advanced Only
}
'''

def snakemake(snakes_given):
    for snake in snakes_given:
        temp = Snake(snake['id'],snake['name'], snake['status'], snake['message'], snake['taunt'], snake['age'], snake['health'], snake['coords'], snake['kills'])
        snakes.append(temp)
        #print "Made snake coords: " + str(temp.coords)

def foodmake(food):
    for coords in food:
        food.append(coords)


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'Lorem Ipsum'
    }

'''  
Recieved Move object for /move
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}

'''



@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    
    #Step one: Parse Map data
    
    mapWidth = data['width']
    #print data['width']
    #print data['height']
    #print data['snakes']
    
    mapHeight = data['height']
    #snakemake(data['snakes'])
    #foodmake(data['food'])
    
    '''
    for snake in snakes:
        if(snake.coords == 0):
            snake.coords = []
        print "snake name: " + str(snake.name)
        print "snake taunt: " + str(snake.taunt)
        print "snake id: " + str(snake.snake_id)
        print "snake age: " + str(snake.age)
        print "snake coords: " + str(snake.coords)
    '''
    
    #currTaunt = taunt.gettaunt().strip()
    currTaunt = 'meow'
    #currMove = 'north'
    #data = {'move': currMove, 'taunt': currTaunt}
    #ret = json.dumps(data)
    
    
    parsedMapData = []
    
    for snake in data['snakes']:
        if snake['id'] == ourSnakeId:
            ourSnake = snake
            break
    
    dirsCanGo = directionsCanGo( parsedMapData, ourSnake, mapHeight, mapWidth )
    currMove = dirsCanGo[0]
    data = {'move': currMove, 'taunt': 'meow' }
    ret = json.dumps(data)
    
    return ret
    '''
    parsedMapData = fillBoard(mapHeight, mapWidth, snakes, food, ourSnakeId)
    
    #Step two: Decide which direction we can go so we dont die
    for snake in snakes:
        if snake.snake_id == ourSnakeId:
            ourSnake = snake
            break
        
    dirsCanGo = directionsCanGo( parsedMapData, ourSnake, mapHeight, mapWidth )
    
    
    #Step three: choose which of the availbale directions to choose/ Add strategy
    
    if len(dirsCanGo) == 0:
        currMove = 'north'
    else:
        currMove = dirsCanGo[0]
    
    currTaunt = taunt.gettaunt().strip()
    #currMove = 'north'
    data = {'move': currMove, 'taunt': currTaunt}
    ret = json.dumps(data)
    return ret
    '''
    '''
    {
        'move': 'north',
        'taunt': 'Meow'
    }
    '''

'''  
Object revcieved for /end
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "height": 20,
    "width": 30,
    "snakes": [
        <Snake Object>, <Snake Object>, ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ],
    "walls": [    // Advanced Only
        [2, 2]
    ],
    "gold": [     // Advanced Only
        [5, 5]
    ]
}

'''


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'YEEZY YEEZY YEEZY JUST JUMPED OVER JUMPMAN'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
