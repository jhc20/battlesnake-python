class SnakeState(object):
    def __init__(self):
        self.ourBodyPlacement = None
        self.curState = FoodState()
        print type(self.curState)
        return

    def runState(self):
        return


class FoodState(SnakeState):
    def __init__(self):
        return

    def runState(self):
        # Do the main action for food searching
        return


class HeadToBodyState(SnakeState):
    def __init__(self):
        return

    def runState(self):
        # Do the main action for a Head To Body Collision
        return


class HeadToHeadAvoidState(SnakeState):
    def __init__(self):
        return

    def runState(self):
        # Do the main action for a Head to Head Collision
        # that should be avoided
        return
        

class HeadToHeadAttackState(SnakeState):
    def __init__(self):
        return

    def runState(self):
        # Do the main action for a Head to Head Collision
        # that should be aimed for 
        return