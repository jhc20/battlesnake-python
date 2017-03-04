# Used around getDirectionsCanGo() function
SAFE_KILL = 1  # ToDo (cut off the other snake)
FOOD = 2  # complete
OPEN = 3  # complete
NEXT_TO_WALL = 4  # ToDo (use current position in relation to map size)
DANGER = 5  # complete (have to move head-to-head with another snake)
CERTAIN_DEATH = 6  # surrounded by walls (never pick)

tauntList = ['with', 'Jeff', 'prepare', 'for', 'death!', 'Wrestle']


def determineMovePriority(directionsCanGo, 
                          turnDictionary, 
                          mapObj, 
                          directionHeuristics, 
                          snakeObj):
    headOfOurSnake = snakeObj.headOfOurSnake
    ourSnake = snakeObj.ourSnake
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
            if (temp > maxSpaces):
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
            # Here we have multiple choices which offer the same amount 
            # of spaces
            # First look at the direction that offers the closest food
            foodDir = getClosestFood(dirsThatHaveMax,
                                     headOfOurSnake,
                                     mapObj.food,
                                     turnDictionary.copy(),
                                     generateDictionaryTuple(mapObj)
                                     )
            if foodDir == None:
                print("Chasing Tail")
                # TODO need to change to space filling algorithm
                buttFirstDir = ButtFirstSearch(dirsThatHaveMax,
                                               headOfOurSnake,
                                               ourSnake['coords'][-1],
                                               turnDictionary.copy(),
                                               generateDictionaryTuple(mapObj)
                                               )

                if buttFirstDir == None:
                    print("Using Space")
                    # currMove = dirsThatHaveMax[random.randint(0, len(dirsThatHaveMax) - 1)]
                    wallHumpDir = wallHump(dirsThatHaveMax, headOfOurSnake,
                                           turnDictionary.copy())
                    if directionHeuristics[wallHumpDir] != DANGER:
                        setHeuristicValue(directionHeuristics, wallHumpDir, FOOD)
                else:
                    if directionHeuristics[wallHumpDir] != DANGER:
                        setHeuristicValue(directionHeuristics, buttFirstDir, OPEN)
            # We are able to get to food. Change heuristic from OPEN to FOOD
            else:
                setHeuristicValue(directionHeuristics, foodDir, FOOD)
            # Remove any that are dangerous
            currMove = getMinimalHeuristicValue(directionHeuristics)
    elif len(directionsCanGo) == 1:
        currMove = directionsCanGo[0]
    else:
        currMove = 'up'
    return currMove


def removeItemFromDictionary(key, dictionary):
    if not dictionary.get(key, None) is None:
        del dictionary[key]


# gives number for co-ord, ex (0, 0) top L
def directionalCoordinate(direction, withRespectTo):
    x = withRespectTo[0]
    y = withRespectTo[1]
    if (direction == 'up'):
        return (x, y - 1)
    elif (direction == 'down'):
        return (x, y + 1)
    elif (direction == 'right'):
        return (x + 1, y)
    elif (direction == 'left'):
        return (x - 1, y)


def removeSnakeCollisions(snakeObj, turnDictionary, heuristics):
    ourSnake = snakeObj.ourSnake
    otherSnakes = snakeObj.otherSnakes
    # Our snakes head
    head = ourSnake['coords'][0]
    # ----- Other Snakes (Where head is going to go)/ Head collision detection ----
    for snake in otherSnakes:
        # Check if we're longer, if so continue
        if len(snake['coords']) < len(ourSnake['coords']):
            continue

        # Else, we have to check if we'd run into them and avoid those 
        # directions
        dirsCouldCollideIn(head, snake['coords'][0], heuristics, turnDictionary)


def dirsCouldCollideIn(ourSnakeHead, 
                       otherSnakeHead, 
                       dirHeuristic, 
                       turnDictionary):
    dirsOurSnakeCanGo = getDirectionsCanGo(ourSnakeHead, turnDictionary)
    dirsOtherSnakeCanGo = getDirectionsCanGo(otherSnakeHead, turnDictionary)
    numberOfMovesTheyHave = len(dirsOurSnakeCanGo)

    for ourDir in dirsOurSnakeCanGo:
        ourCoord = directionalCoordinate(ourDir, ourSnakeHead)
        for theirDirs in dirsOtherSnakeCanGo:
            theirCoord = directionalCoordinate(theirDirs, otherSnakeHead)
            if ourCoord == theirCoord:
                if numberOfMovesTheyHave > 1:
                    setHeuristicValue(dirHeuristic, ourDir, DANGER)
                elif numberOfMovesTheyHave == 1:
                    setHeuristicValue(dirHeuristic, ourDir, CERTAIN_DEATH)


def getDirectionsCanGo(snakeObj, turnDictionary):
    head = snakeObj.headOfOurSnake
    canGo = []
    x = head[0]
    y = head[1]
    right = (x + 1, y)
    left = (x - 1, y)
    up = (x, y - 1)
    down = (x, y + 1)
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
    right = (x + 1, y)
    left = (x - 1, y)
    up = (x, y - 1)
    down = (x, y + 1)
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
    while (getUnvisitedNeighbor(
                directionalCoordinate(dir, start), otherNodes) is not None):
        count += 1
    return count


# This can probably be cleaned up and written better, 
# but the basic idea is to get spaces with 2 edges first otherwise 1
def wallHump(dirsFromHead, head, otherNodes):
    dirMap = {}
    for dir in dirsFromHead:
        dirMap[dir] = len(
            getDirectionsCanGo(directionalCoordinate(dir, head), otherNodes))  # getSpacesAround(dir, start, otherNodes)
    for dir in dirMap:
        if dirMap[dir] == 1:  # 2:
            return dir
    for dir in dirMap:
        if dirMap[dir] == 2:  # 1:
            return dir
    for dir in dirMap:
        if dirMap[dir] == 3:  # 3:
            return dir


def generateDictionaryTuple(mapObj):
    tempDictionary = {}
    for y in xrange(mapObj.board_height):
        for x in xrange(mapObj.board_width):
            tempDictionary[(x, y)] = ()
    return tempDictionary


def generateDictionaryTF(mapObj, originalDictionary):
    for y in xrange(mapObj.board_height):
        for x in xrange(mapObj.board_width):
            originalDictionary[(x, y)] = False


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


def tauntGenerator():
    currentTaunt = tauntList.pop(0)
    tauntList.append(currentTaunt)
    return currentTaunt

