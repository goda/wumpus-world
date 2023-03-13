from enum import IntEnum
from typing import List
from typing import TypeVar
TAction = TypeVar("TAction", bound="Action")
TCoords = TypeVar("TCoords", bound="Coords")
TOrientationState = TypeVar("TOrientationState", bound="OrientationState")


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

    @staticmethod
    def get_all() -> List[TAction]:
        allowed_actions = [Action(x) for x in range(1, 7)]
        return allowed_actions

    @staticmethod
    def opposite_turn(action: TAction) -> TAction:
        if action == Action.TurnRight:
            return Action.TurnLeft
        elif action == Action.TurnLeft:
            return Action.TurnRight

        return action

    def __str__(self) -> str:
        return self.name


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
    reward: int = 0

    def __init__(self,
                 stench: bool = False,
                 breeze: bool = False,
                 glitter: bool = False,
                 bump: bool = False,
                 scream: bool = False,
                 is_terminated: bool = False,
                 reward: int = 0):
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
        if __o == None:
            return False        
        return self.x == __o.x and self.y == __o.y

    def __str__(self) -> str:
        return "(x: " + str(self.x) + ", y: " + str(self.y) + ")"

    def __hash__(self):
        return hash(self.__str__())

    @staticmethod
    def from_string(s: str) -> TCoords:
        """Expected format `(x: 0, y: 0)` which translates
        to Coords(0,0)

        Args:
            s (str): formatted string representing `Coords`
        """
        expr = s.replace(":", "=")
        return eval("Coords" + expr + "")

    def is_adjacent(self, coord_b: TCoords) -> bool:
        """Returns true if provided coord is adjacent (not diagnoally)
        """
        if(abs(self.x-coord_b.x) + abs(self.y-coord_b.y) == 1):
            return True
        return False

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

    @staticmethod
    def opposite_orientation(orientation: TOrientationState) -> TOrientationState:
        return OrientationState((orientation.value + 2) % 4)


class Orientation:
    state: OrientationState = OrientationState.East

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
