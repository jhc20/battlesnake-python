import bottle
import os
import json
import random
import copy

import uuid
import sys


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

# Safe kill = 1
# Food = 2
# Open = 3
# Next to wall = 4
# Danger = 5
# Certain Death = 6

# Used around getDirectionsCanGo() function
SAFE_KILL = 1       # ToDo (cut off the other snake)
FOOD = 2            # complete
OPEN = 3            # complete
NEXT_TO_WALL = 4    # ToDo (use current position in relation to map size)
DANGER = 5          # complete (have to move head-to-head with another snake)
CERTAIN_DEATH = 6   # surrounded by walls (never pick)

ourSnakeId = ""
ourName = "Jeff"
#ourName = str(uuid.uuid4())
originalDictionary = {}
tauntList = ['with', 'Jeff', 'prepare', 'for', 'death!', 'Wrestle']



def removeItemFromDictionary(key, dictionary):
    if not dictionary.get(key, None) is None:
        del dictionary[key]


# gives number for co-ord, ex (0, 0) top L
def directionalCoordinate(direction, withRespectTo):
    x = withRespectTo[0]
    y = withRespectTo[1]
    if(direction == 'up'):
        return (x, y-1)
    elif(direction == 'down'):
        return (x, y+1)
    elif(direction == 'right'):
        return (x+1, y)
    elif(direction == 'left'):
        return (x-1, y)


def removeSnakeCollisions(ourSnake, otherSnakes, turnDictionary, heuristics):
    # Our snakes head
    head = ourSnake['coords'][0]

    # ----- Other Snakes (Where head is going to go)/ Head collision detection ----
    for snake in otherSnakes:
        # Check if we're longer, if so continue
        if len(snake['coords']) < len(ourSnake['coords']):
            continue

        # Else, we have to check if we'd run into them and avoid those directions
        dirsCouldCollideIn(head,snake['coords'][0], heuristics, turnDictionary)


def dirsCouldCollideIn(ourSnakeHead, otherSnakeHead, dirHeuristic, turnDictionary):
    dirsOurSnakeCanGo = getDirectionsCanGo(ourSnakeHead, turnDictionary)
    dirsOtherSnakeCanGo = getDirectionsCanGo(otherSnakeHead, turnDictionary)
    numberOfMovesTheyHave = len(dirsOurSnakeCanGo)

    for ourDir in dirsOurSnakeCanGo:
        ourCoord = directionalCoordinate(ourDir, ourSnakeHead)
        for theirDirs in dirsOtherSnakeCanGo:
            theirCoord = directionalCoordinate(theirDirs, otherSnakeHead)
            if ourCoord == theirCoord:
                if numberOfMovesTheyHave > 1:
                    setHeuristicValue(dirHeuristic, ourDir, 5)
                elif numberOfMovesTheyHave == 1:
                    setHeuristicValue(dirHeuristic, ourDir, 6)


def getDirectionsCanGo(head, turnDictionary):
    canGo = []
    x = head[0]
    y = head[1]
    right = (x+1, y)
    left = (x-1, y)
    up = (x, y-1)
    down = (x, y+1)
    if right in turnDictionary.keys():
        canGo.append('right')
    if left in turnDictionary.keys():
        canGo.append('left')
    if up in turnDictionary.keys():
        canGo.append('up')
    if down in turnDictionary.keys():
        canGo.append('down')
    return canGo


def getUnvisitedNeighbor(node, otherNodes):
    x = node[0]
    y = node[1]
    right = (x+1, y)
    left = (x-1, y)
    up = (x, y-1)
    down = (x, y+1)
    if right in otherNodes.keys() and otherNodes[right] == False:
        return right
    elif left in otherNodes.keys() and otherNodes[left] == False:
        return left
    elif up in otherNodes.keys() and otherNodes[up] == False:
        return up
    elif down in otherNodes.keys() and otherNodes[down] == False:
        return down
    else:
        return None


def bfs(rootNode, otherNodes):
    queue = []
    queue.append(rootNode)
    otherNodes[rootNode] = True
    room = 0
    while len(queue) > 0:
        node = queue.pop(0)
        child = getUnvisitedNeighbor(node, otherNodes)
        while not child == None:
            otherNodes[child] = True
            queue.append(child)
            child = getUnvisitedNeighbor(node, otherNodes)
            room = room + 1

    return room


def determineDirection(node, head):
    if list(head)[1] - list(node)[1] == 1:
        return "up"
    if list(head)[1] - list(node)[1] == -1:
        return "down"
    if list(head)[0] - list(node)[0] == 1:
        return "left"
    if list(head)[0] - list(node)[0] == -1:
        return "right"


def getClosestFood(dirsFromHead, head, foods, otherNodes, parentDictionary):
    queue = []
    queue.append(head)
    otherNodes[tuple(head)] = True
    while len(queue) > 0:
        node = queue.pop(0)
        if list(node) in foods:
            while not (parentDictionary[node] == head):
                node = parentDictionary[node]
            if determineDirection(node, head) in dirsFromHead:
                print(determineDirection(node, head))
                return determineDirection(node, head)
        childNode = getUnvisitedNeighbor(node, otherNodes)
        while not childNode == None:
            parentDictionary[childNode] = node
            otherNodes[childNode] = True
            queue.append(childNode)
            childNode = getUnvisitedNeighbor(node, otherNodes)


# our snake chases its own Tail
def ButtFirstSearch(dirsFromHead, head, tail, otherNodes, parentDictionary):
    queue = []
    queue.append(head)
    otherNodes[tuple(head)] = True
    while len(queue) > 0:
        node = queue.pop(0)
        if list(node) == tail:
            while not (parentDictionary[node] == head):
                node = parentDictionary[node]
            if determineDirection(node, head) in dirsFromHead:
                print(determineDirection(node, head))
                return determineDirection(node, head)
        childNode = getUnvisitedNeighbor(node, otherNodes)
        while not childNode == None:
            parentDictionary[childNode] = node
            otherNodes[childNode] = True
            queue.append(childNode)
            childNode = getUnvisitedNeighbor(node, otherNodes)


def getSpacesAround(dir, start, otherNodes):
    count = 0
    while getUnvisitedNeighbor(directionalCoordinate(dir, start), otherNodes) is not None:
        count += 1
    return count


#This can probably be cleaned up and written better, but the basic idea is to get spaces with 2 edges first otherwise 1
def wallHump(dirsFromHead, head, otherNodes):
    dirMap = {}
    for dir in dirsFromHead:
        dirMap[dir] = len(getDirectionsCanGo(directionalCoordinate(dir, head), otherNodes))#getSpacesAround(dir, start, otherNodes)
    for dir in dirMap:
        if dirMap[dir] == 1:#2:
            return dir
    for dir in dirMap:
        if dirMap[dir] == 2:#1:
            return dir
    for dir in dirMap:
        if dirMap[dir] == 3:#3:
            return dir


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

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
    "food": []
}
'''


def generateDictionaryTuple(board_width, board_height):
    tempDictionary = {}
    for y in xrange(board_height):
        for x in xrange(board_width):
            tempDictionary[(x,y)] = ()
    return tempDictionary


def generateDictionaryTF(board_width, board_height):
    for y in xrange(board_height):
        for x in xrange(board_width):
            originalDictionary[(x,y)] = False


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#FFA500',
        'taunt': 'Wrestle',
        'head_url': head_url,
        'name': ourName
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
    ]
}

'''
# For setting the heuristic entries, we only assign higher values
def setHeuristicValue(heuristic, key, value):
    if heuristic.get(key, None) is None:
        heuristic[key] = value
    elif heuristic[key] < value:
        heuristic[key] = value

def getMinimalHeuristicValue(heuristic):
    min = 10
    minDir = ''
    for dir in heuristic:
        if heuristic[dir] < min:
            min = heuristic[dir]
            minDir = dir
    return minDir

@bottle.post('/move')
def move():
    data = bottle.request.json

    # Actual board that snakes play on
    mapWidth = data['width']
    mapHeight = data['height']

    currTaunt = 'meow'

    # True/False for every spot on the board for visited nodes in BFS
    if(len(originalDictionary) < 1):
        generateDictionaryTF(mapWidth, mapHeight)

    turnDictionary = originalDictionary.copy()

    ourSnake = {}
    otherSnakes = []

    # Remove spots that are completely unavailable
    # Makes list for other snakes by looking at all snakes with name != ours
    for snake in data['snakes']:
        if snake['name'] == ourName:
            ourSnake = snake
        else:
            otherSnakes.append(snake)
        # removes all snake bodies/tail (not head) from list of 
        # possible co-ordinates 
        for coord in snake['coords'][:-1]:
            x = coord[0]
            y = coord[1]
            if not turnDictionary.get((x, y), None) is None:
                del turnDictionary[(x, y)]

    headOfOurSnake = ourSnake['coords'][0]
    # dictionary of all 4 directions
    directionsCanGo = getDirectionsCanGo(headOfOurSnake, turnDictionary)
    # dictionary holding all possible directions in form:
    # [direction, heuristicValue]
    directionHeuristics = {}
    # set collision directions == 5 (Danger)
    removeSnakeCollisions(ourSnake, otherSnakes, turnDictionary, 
                          directionHeuristics)

    currMove = "up"
    # Set heuristic values if they need to be found
    # sets collisions to == CERTAIN_DEATH
    if len(directionsCanGo) >= 2:
        maxSpaces = 0
        maxSpacesDir = 'up'
        dirsAndValues = {}
        # find direction that gives largest/most open area
        for dir in directionsCanGo:
            availableSpotNodes = turnDictionary.copy()
            rootNode = directionalCoordinate(dir, headOfOurSnake)
            temp = bfs(rootNode, availableSpotNodes)
            dirsAndValues[dir] = temp
            if(temp > maxSpaces):
                maxSpaces = temp
                maxSpacesDir = dir
        dirsThatHaveMax = []
        for dir in dirsAndValues:
            if dirsAndValues[dir] == maxSpaces:
                dirsThatHaveMax.append(dir)
        # multiple directions have the best heuristic value
        if len(dirsThatHaveMax) == 1:
            currMove = maxSpacesDir
        # check for nearest food since we have established there is open space
        else:
            # Here we have multiple choices which offer the same amount of spaces
            # First look at the direction that offers the closest food
            foodDir = getClosestFood(dirsThatHaveMax, 
                                     headOfOurSnake, 
                                     data['food'], 
                                     turnDictionary.copy(), 
                                     generateDictionaryTuple(
                                            mapHeight, mapWidth))
            if foodDir == None:
                print("Chasing Tail")
                #TODO need to change to space filling algorithm
                buttFirstDir = ButtFirstSearch(dirsThatHaveMax, 
                                               headOfOurSnake, 
                                               ourSnake['coords'][-1], 
                                               turnDictionary.copy(), 
                                               generateDictionaryTuple(
                                                        mapHeight, mapWidth))
                if buttFirstDir == None:
                    print("Using Space")
                    # currMove = dirsThatHaveMax[random.randint(0, len(dirsThatHaveMax) - 1)]
                    wallHumpDir = wallHump(dirsThatHaveMax, headOfOurSnake, 
                                           turnDictionary.copy())
                    setHeuristicValue(directionHeuristics, wallHumpDir, FOOD)
                else:
                    setHeuristicValue(directionHeuristics, buttFirstDir, OPEN)
            # We are able to get to food. Change heuristic from OPEN to FOOD
            else:
                setHeuristicValue(directionHeuristics, foodDir, FOOD)
            currMove = getMinimalHeuristicValue(directionHeuristics)
    elif len(directionsCanGo) == 1:
        currMove = directionsCanGo[0]
    else:
        currMove = 'up'
    # ToDo -- Callum
    # danger check should happen after food evaluation 
    # send determined move to server
    data = {'move': currMove, 'taunt': currTaunt}
    ret = json.dumps(data)

    return {
        'move': currMove,
        'taunt': tauntGenerator()
    }

def tauntGenerator():
    currentTaunt = tauntList.pop(0)
    tauntList.append(currentTaunt)
    return currentTaunt


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))