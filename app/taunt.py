
def __init__(self):
    print "inited taunt"
    
def gettaunt():
    f = open('taunts.txt', 'r')
    for line in f:
        print line