import bottle
import os

from Snake import Snake
from Map import Map
from utils import generateDictionaryTF, getDirectionsCanGo, \
    removeSnakeCollisions, determineMovePriority, tauntGenerator


'''
Example Received Snake Object

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
ourName = "Jeff"
originalDictionary = {}
mapObj = Map()


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(
        path,
        root='static/'
    )


@bottle.post('/start')
def start():
    data = bottle.request.json
    mapObj.game_id = data['game_id']
    mapObj.board_width = data['width']
    mapObj.board_height = data['height']

    head_url = '%s://%s/static/head.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#FFA500',
        'taunt': 'Wrestle with Jeff, prepare for death!',
        'head_url': head_url,
        'name': ourName
    }

@bottle.post('/move')
def move():
    snakeObj = Snake() 
    data = bottle.request.json
    mapObj.setData(data)
    # True/False for every spot on the board for visited nodes in BFS
    if (len(originalDictionary) < 1):
        generateDictionaryTF(mapObj, originalDictionary)
    turnDictionary = originalDictionary.copy()
    # Remove spots that are completely unavailable
    # Makes list for other snakes by looking at all snakes with name != ours
    for snake in data['snakes']:
        if snake['name'] == ourName:
            ourSnake = snake
            snakeObj.ourSnake = ourSnake
            snakeObj.headOfOurSnake = ourSnake['coords'][0]
        else:
            snakeObj.otherSnakes.append(snake)
        # removes all snake bodies/tail (not head) from list of
        # possible co-ordinates
        for coord in snake['coords'][:-1]:
            x = coord[0]
            y = coord[1]
            if not turnDictionary.get((x, y), None) is None:
                del turnDictionary[(x, y)]
    # dictionary of all 4 directions
    directionsCanGo = getDirectionsCanGo(snakeObj, turnDictionary)
    # dictionary holding all possible directions in form:
    # [direction, heuristicValue]
    directionHeuristics = {}
    # set collision directions == 5 (Danger)
    currMove = determineMovePriority(directionsCanGo, 
                                     turnDictionary,  
                                     mapObj, 
                                     directionHeuristics, 
                                     snakeObj)
    removeSnakeCollisions(snakeObj, turnDictionary, directionHeuristics)
    # ToDo -- Callum
    # danger check should happen after food evaluation
    # send determined move to server

    return {
        'move': currMove,
        'taunt': tauntGenerator()
    }

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), 
            port=os.getenv('PORT', '8080'))