import copy
from src.environment.Misc import OrientationState
from src.environment.Misc import Orientation
from src.environment.Misc import Coords
from typing import Self



class Agent():
    location: Coords
    orientation: Orientation = Orientation(OrientationState.East)
    has_gold: bool = False
    has_arrow: bool = True
    is_alive: bool = True

    def __init__(self, location: Coords = Coords(0,0), 
                 orientation: Orientation = Orientation(OrientationState.East), 
                 has_gold: bool = False, has_arrow: bool = True, is_alive: bool = True):
        self.location = location
        self.orientation = orientation
        self.has_gold = has_gold
        self.has_arrow = has_arrow
        self.is_alive = is_alive
    
    
    def forward(self, grid_width: int, grid_height: int) -> Self:
        if self.orientation == OrientationState.West:
            new_location = Coords(max(0, self.location.x - 1), self.location.y)
        elif self.orientation == OrientationState.East:
            new_location = Coords(min(grid_width - 1, self.location.x + 1), self.location.y)
        elif self.orientation == OrientationState.North:
            new_location = Coords(self.location.x, min(grid_height - 1, self.location.y+1))
        elif self.orientation == OrientationState.South:
            new_location = Coords(self.location.x, max(0, self.location.y - 1))
                                
        new_agent = copy.copy(self)
        new_agent.location = new_location
        return new_agent