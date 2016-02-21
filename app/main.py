import bottle
import os
import json
import random


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

#def bfs(canGo):

def directionsCanGo(mapdata, ourSnake, mapHeight, mapWidth, otherSnakes, food):
    #if len(ourSnake.coords) == 0:
    
    #    return
    canGo = ['north', 'west', 'south', 'east']
    # Code to decide which dirs we can go
    head = ourSnake['coords'][0]
    #length = len(ourSnake.coords)
    print head
    #-----WALLS-----
    
    #if head co-ord x is 0, cant move north
    if head[1] == 0:
        canGo.remove('north')
    
    #if head co-ord x is height-1 cant move south
    if head[1] == mapHeight-1:
        canGo.remove('south')
        
    #if head co-ord y is 0, cant move west
    if head[0] == 0:
        canGo.remove('west')
        
    #if head co-ord y is  width - 1 cant more east 
    if head[0] == mapWidth-1:
        canGo.remove('east')
    print str(canGo)
    #-----Ourselves-----
    del ourSnake['coords'][-1]    
    for coord in ourSnake['coords']:
        if coord == head:
            continue
        if (coord[1] - head[1] == 1) and (coord[0] - head[0] == 0):
            if 'south' in canGo:
                canGo.remove('south')
        if (coord[0] - head[0] == 1) and (coord[1] - head[1] == 0):
            if 'east' in canGo:
                canGo.remove('east')
        if (coord[1] - head[1] == -1) and (coord[0] - head[0] == 0):
            if 'north'  in canGo:
                canGo.remove('north')
        if (coord[0] - head[0] == -1) and (coord[1] - head[1] == 0):
            if 'west' in canGo:
                canGo.remove('west')

    #-----Other Snakes -----
    for snake in otherSnakes:
        del snake['coords'][-1]
        for coord in snake['coords']:
            if (coord[1] - head[1] == 1) and (coord[0] - head[0] == 0):
                if 'south' in canGo:
                    canGo.remove('south')
            if (coord[0] - head[0] == 1) and (coord[1] - head[1] == 0):
                if 'east' in canGo:
                    canGo.remove('east')
            if (coord[1] - head[1] == -1) and (coord[0] - head[0] == 0):
                if 'north'  in canGo:
                    canGo.remove('north')
            if (coord[0] - head[0] == -1) and (coord[1] - head[1] == 0):
                if 'west' in canGo:
                    canGo.remove('west')
                    
    for snake in otherSnakes:
        if (snake['coords'][0][1] - head[1] == 2):
            if 'east' in canGo:
                canGo.remove('east')
        if (snake['coords'][0][1] - head[1] == -2):
            if 'west' in canGo:
                canGo.remove('west')
        if (snake['coords'][0][0] - head[0] == 2):
            if 'north' in canGo:
                canGo.remove('north')
        if (snake['coords'][0][0] - head[0] == -2):
            if 'south' in canGo:
                canGo.remove('south')'''
        if ((snake['coords'][0][1] - head[1] == 1) and (snake['coords'][0][0] - head[0] == 1)):
            if 'east' in canGo:
                canGo.remove('east')
            if 'north' in canGo:
                canGo.remove('north')
        if ((snake['coords'][0][1] - head[1] == 1) and (snake['coords'][0][0] - head[0] == -1)):
            if 'east' in canGo:
                canGo.remove('east')
            if 'south' in canGo:
                canGo.remove('south')
        if ((snake['coords'][0][1] - head[1] == -1) and (snake['coords'][0][0] - head[0] == 1)):
            if 'west' in canGo:
                canGo.remove('west')
            if 'north' in canGo:
                canGo.remove('north')
        if ((snake['coords'][0][1] - head[1] == -1) and (snake['coords'][0][0] - head[0] == -1)):
            if 'west' in canGo:
                canGo.remove('west')
            if 'south' in canGo:
                canGo.remove('south')'''
    return canGo

ourSnakeId = "902f27c7-400a-4316-9672-586bf72bee07"
snakes = []


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
    
    
    #currTaunt = taunt.gettaunt().strip()
    currTaunt = 'meow'
    #currMove = 'north'
    #data = {'move': currMove, 'taunt': currTaunt}
    #ret = json.dumps(data)
    
    
    parsedMapData = []
    otherSnakes = []
    for snake in data['snakes']:
        if snake['id'] == ourSnakeId:
            ourSnake = snake
        else:
            otherSnakes.append(snake)
    food = data['food']
    dirsCanGo = directionsCanGo( parsedMapData, ourSnake, mapHeight, mapWidth, otherSnakes, food)
    currMove = dirsCanGo[random.randint(0, len(dirsCanGo)-1)]
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
