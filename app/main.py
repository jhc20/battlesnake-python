import bottle
import os
import json
import random
from snake import *

'''
Example Recieved Snake Object

{
    "id": "1234-567890-123456-7890",
    "name": "Well Documented Snake",
    "status": "alive",
    "message": "Moved up",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ,]
    "kills": 4,
    "food": 12,
    "gold": 2
}
'''

import bottle
import os
import json
import random
from snake import *

'''
Example Recieved Snake Object

{
    "id": "1234-567890-123456-7890",
    "name": "Well Documented Snake",
    "status": "alive",
    "message": "Moved up",
    "taunt": "Let's rock!",
    "age": 56,
    "health": 83,
    "coords": [ [1, 1], [1, 2], [2, 2] ,]
    "kills": 4,
    "food": 12,
    "gold": 2
}
'''

ourSnakeId = ""
ourName = "battlesnake-python"
snakes = []


def directionsCanGo(mapdata, ourSnake, mapHeight, mapWidth, otherSnakes, food):
    # if len(ourSnake.coords) == 0:

    #    return
    canGo = ['up', 'left', 'down', 'right']
    # Code to decide which dirs we can go
    head = ourSnake['coords'][0]
    # length = len(ourSnake.coords)
    print head
    # -----WALLS-----

    # if head co-ord x is 0, cant move up
    if head[1] == 0:
        canGo.remove('up')

    # if head co-ord x is height-1 cant move down
    if head[1] == mapHeight - 1:
        canGo.remove('down')

    # if head co-ord y is 0, cant move left
    if head[0] == 0:
        canGo.remove('left')

    # if head co-ord y is  width - 1 cant more right
    if head[0] == mapWidth - 1:
        canGo.remove('right')
    print str(canGo)
    # -----Ourselves-----
    del ourSnake['coords'][-1]
    for coord in ourSnake['coords']:
        if coord == head:
            continue
        if (coord[1] - head[1] == 1) and (coord[0] - head[0] == 0):
            if 'down' in canGo:
                canGo.remove('down')
        if (coord[0] - head[0] == 1) and (coord[1] - head[1] == 0):
            if 'right' in canGo:
                canGo.remove('right')
        if (coord[1] - head[1] == -1) and (coord[0] - head[0] == 0):
            if 'up' in canGo:
                canGo.remove('up')
        if (coord[0] - head[0] == -1) and (coord[1] - head[1] == 0):
            if 'left' in canGo:
                canGo.remove('left')

    # -----Other Snakes -----
    for snake in otherSnakes:
        del snake['coords'][-1]
        for coord in snake['coords']:
            if (coord[1] - head[1] == 1) and (coord[0] - head[0] == 0):
                if 'down' in canGo:
                    canGo.remove('down')
            if (coord[0] - head[0] == 1) and (coord[1] - head[1] == 0):
                if 'right' in canGo:
                    canGo.remove('right')
            if (coord[1] - head[1] == -1) and (coord[0] - head[0] == 0):
                if 'up' in canGo:
                    canGo.remove('up')
            if (coord[0] - head[0] == -1) and (coord[1] - head[1] == 0):
                if 'left' in canGo:
                    canGo.remove('left')

    for snake in otherSnakes:
        if (snake['coords'][0][0] - head[0] == 2) and (snake['coords'][0][1] == head[1]):
            if 'right' in canGo:
                canGo.remove('right')
        if (snake['coords'][0][0] - head[0] == -2) and (snake['coords'][0][1] == head[1]):
            if 'left' in canGo:
                canGo.remove('left')
        if (snake['coords'][0][1] - head[1] == 2) and (snake['coords'][0][0] == head[0]):
            if 'down' in canGo:
                canGo.remove('down')
        if (snake['coords'][0][1] - head[1] == -2) and (snake['coords'][0][0] == head[0]):
            if 'up' in canGo:
                canGo.remove('up')
        if ((snake['coords'][0][0] - head[0] == 1) and (snake['coords'][0][1] - head[1] == -1)):
            if 'right' in canGo:
                canGo.remove('right')
            if 'up' in canGo:
                canGo.remove('up')
        if ((snake['coords'][0][0] - head[0] == 1) and (snake['coords'][0][1] - head[1] == 1)):
            if 'right' in canGo:
                canGo.remove('right')
            if 'down' in canGo:
                canGo.remove('down')
        if ((snake['coords'][0][0] - head[0] == -1) and (snake['coords'][0][1] - head[1] == -1)):
            if 'left' in canGo:
                canGo.remove('left')
            if 'up' in canGo:
                canGo.remove('up')
        if ((snake['coords'][0][0] - head[0] == -1) and (snake['coords'][0][1] - head[1] == 1)):
            if 'left' in canGo:
                canGo.remove('left')
            if 'down' in canGo:
                canGo.remove('down')
    return canGo

'''
def snakeStates():
    if there is enemy snake head near oursnake head
        if oursnake is bigger
            head attack state
        else
            avoid attack state (will take direction preference according to location of food and location of other snakes)
    else if there is enemy snake body near oursnake head
        avoid body state (change directions with preference according to location of food and location of other snakes)
    else
        look for food state
'''

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


def snakemake(snakes_given):
    for snake in snakes_given:
        temp = Snake(snake['id'], snake['name'], snake['status'], snake['message'], snake['taunt'], snake['age'],
                     snake['health'], snake['coords'], snake['kills'])
        snakes.append(temp)
        # print "Made snake coords: " + str(temp.coords)


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


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
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

    # Step one: Parse Map data

    mapWidth = data['width']
    # print data['width']
    # print data['height']

    mapHeight = data['height']
    # snakemake(data['snakes'])
    # foodmake(data['food'])


    # currTaunt = taunt.gettaunt().strip()
    currTaunt = 'meow'
    # currMove = 'up'
    # data = {'move': currMove, 'taunt': currTaunt}
    # ret = json.dumps(data)

    ourSnake = {}
    parsedMapData = []
    otherSnakes = []
    print(data)
    for snake in data['snakes']:
        if snake['name'] == ourName:
            ourSnake = snake
        else:
            otherSnakes.append(snake)
    food = data['food']
    print "ourSnakek"
    # print ourSnake
    print "others"
    print otherSnakes
    dirsCanGo = directionsCanGo(parsedMapData, ourSnake, mapHeight, mapWidth, otherSnakes, food)
    currMove = dirsCanGo[random.randint(0, len(dirsCanGo) - 1)]
    # currMove = dirsCanGo[0]
    data = {'move': currMove, 'taunt': 'meow'}
    ret = json.dumps(data)

    return ret


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))