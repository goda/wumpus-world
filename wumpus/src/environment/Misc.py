from enum import IntEnum

class Action(IntEnum):
    """An enum class to hold the type of action

    Args:
        Enum (_type_): For implementation of enum class
    """
    Forward = 1
    TurnLeft = 2
    TurnRight = 3
    Shoot = 4
    Grab = 5
    Climb = 6


class Percept():
    """A class to hold the percept as would be sensed by the Agent
    when it is in a given environment and position
    """
    stench: bool = False
    breeze: bool = False
    glitter: bool = False
    bump: bool = False
    scream: bool = False
    is_terminated: bool = False
    reward: bool = False

    def __init__(self, stench: bool, breeze: bool, 
                 glitter: bool, bump: bool, scream: bool, 
                 is_terminated: bool, reward: bool):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.is_terminated = is_terminated
        self.reward = reward
        return

    def show(self) -> str:
        return "| Stench: " + str(self.stench) + "| Breeze: " + str(self.breeze) \
            + "| Glitter: " + str(self.glitter) + "| Bump: " + str(self.bump) \
            + "| Scream: " + str(self.scream) + "| Terminated: " + str(self.is_terminated) \
            + "| Reward: " + str(self.reward)


class Coords():
    x: int = 0
    y: int = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __str__(self) -> str:
        return "(x: " + str(self.x) + ", y: " + str(self.y) +")"

#########################
# Orientation Classes
#########################

class OrientationState(IntEnum):
    """An enum for storing the orientation 

    Args:
        Enum (_type_): For implementation of enum class
    """
    North = 0
    East = 1
    South = 2
    West = 3


class Orientation:
    state = OrientationState.East

    def __init__(self, orientation: OrientationState) -> None:
        self.state = orientation

    def turn(self, action: Action):
        if action == Action.TurnLeft:
            self.turn_left()
        elif action == Action.TurnRight:
            self.turn_right()

    def turn_left(self):
        new_orientation_index = (self.state.value - 1) % 4
        self.state = OrientationState(new_orientation_index)

    def turn_right(self):
        new_orientation_index = (self.state.value + 1) % 4
        self.state = OrientationState(new_orientation_index)
