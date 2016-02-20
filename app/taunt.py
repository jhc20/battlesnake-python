import random
def __init__(self):
    print "inited taunt"
    
def gettaunt():
    random.seed(None)
    taunts = []
    f = open('taunts.txt', 'r')
    for line in f:
        taunts.append(line)
    return taunts[random.randint(0, len(taunts)-1)]