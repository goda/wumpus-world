import copy
import random
from typing import Self, Tuple
from typing import List
from wumpus.src.environment.Misc import Percept
from wumpus.src.environment.Misc import Action
from wumpus.src.environment.Misc import OrientationState
from wumpus.src.environment.Agent import Agent
from wumpus.src.environment.Misc import Coords

class Environment():
    """A class to hold the environment configuration including methods for simulating 
    Agent actions etc.
    """
    grid_width: int = 4
    grid_height: int = 4
    pit_prob: float = 0.2
    allow_climb_without_gold: bool = False
    agent: Agent = Agent()
    pit_locations: List[Coords] = []
    terminated: bool = False
    wumpus_location: Coords
    wumpus_alive: bool = True
    gold_location: Coords
    
    @classmethod
    def initialize(self, grid_width: int = 4, grid_height: int = 4, 
                 pit_prob: float = 0.2, allow_climb_without_gold: bool = False) -> Tuple[Self, Percept]:
        e = Environment(grid_width, grid_height, pit_prob, allow_climb_without_gold)
        percept = Percept(e.is_stench(), e.is_breeze(),
                          False, False, False, False, 0)
        return (e,percept)
    
    def __init__(self, grid_width: int = 4, grid_height: int = 4, 
                 pit_prob: float = 0.2, allow_climb_without_gold: bool = False) -> None:
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.pit_prob = pit_prob
        self.allow_climb_without_gold = allow_climb_without_gold
        
        def random_location_except_origin() -> Coords:
            x = random.randint(1, self.grid_width - 1)
            y = random.randint(1, self.grid_height - 1)
            return Coords(x, y)
        
        generate_pit_locations = lambda w, h : [Coords(x, y) for x in range(0, w)
                            for y in range(0, h) if (x != 0 or y != 0)
                            and random.random() < self.pit_prob]
        self.pit_locations = generate_pit_locations(self.grid_width, self.grid_height)
        
        self.agent = Agent()
        self.wumpus_location = random_location_except_origin()
        self.gold_location = random_location_except_origin()

    def is_pit_at(self, coords: Coords) -> bool:
        return coords in self.pit_locations

    def is_wumpus_at(self, coords: Coords) -> bool:
        return coords == self.wumpus_location

    def is_agent_at(self, coords: Coords) -> bool:
        return coords == self.agent.location

    def is_glitter(self) -> bool:
        return self.agent.location == self.gold_location

    def is_gold_at(self, coords: Coords) -> bool:
        return coords == self.gold_location

    def wumpus_in_line_of_fire(self):
        if self.agent.orientation.state == OrientationState.West:
            return self.agent.location.x > self.wumpus_location.x and self.agent.location.y == self.wumpus_location.y
        elif self.agent.orientation.state == OrientationState.East:
            return self.agent.location.x < self.wumpus_location.x and self.agent.location.y == self.wumpus_location.y
        elif self.agent.orientation.state == OrientationState.North:
            return self.agent.location.x == self.wumpus_location.x and self.agent.location.y < self.wumpus_location.y
        elif self.agent.orientation.state == OrientationState.South:
            return self.agent.location.x == self.wumpus_location.x and self.agent.location.y > self.wumpus_location.y                                                
    
    def kill_attempt_successful(self) -> bool:        
        return self.agent.has_arrow and self.wumpus_alive and self.wumpus_in_line_of_fire()
    
    def adjacent_cells(self, coords: Coords) -> List[Coords]:
        neighbors = lambda x, y : [Coords(x2, y2) for x2 in range(x-1, x+2)
                                    for y2 in range(y-1, y+2)
                                    if (-1 < x < self.grid_width and
                                        -1 < y < self.grid_height and
                                        (x != x2 or y != y2) and
                                        (x == x2 or y == y2) and
                                        (0 <= x2 < self.grid_width) and
                                        (0 <= y2 < self.grid_height))]
        return neighbors(coords.x, coords.y)
    
    def is_pit_adjacent(self, coords: Coords) -> bool:
        for p in self.pit_locations:
            if p in self.adjacent_cells(coords):
                return True
        return False
    
    def is_wumpus_adjacent(self, coords: Coords) -> bool:
        if self.wumpus_location in self.adjacent_cells(coords):
            return True
        return False
    
    def is_breeze(self) -> bool:
        return self.is_pit_adjacent(self.agent.location)
    
    def is_stench(self) -> bool:
        return self.is_wumpus_adjacent(self.agent.location)    
    
    def apply_action(self, action: Action) -> Tuple[Self, Percept]:
        if self.terminated:
            return (
                self,
                Percept(False, False, False, False, False, True, 0)
            )
        
        if action == Action.Forward:
            new_agent = self.agent.forward(self.grid_width, self.grid_height)
            death = (self.is_wumpus_at(new_agent.location) and self.wumpus_alive) \
                    or self.is_pit_at(new_agent.location) 
            # update environment/ agent
            new_agent.is_alive = not death
            new_agent.has_gold = self.agent.has_gold or self.gold_location == new_agent.location
            
            new_environment = copy.deepcopy(self)
            new_environment.agent = new_agent
            new_environment.gold_location = new_agent.location if new_agent.has_gold else new_environment.gold_location
            
            return (
                new_environment,
                Percept(new_environment.is_stench(), new_environment.is_breeze(), 
                        new_environment.is_glitter(), new_agent.location == self.agent.location, 
                        False, not new_agent.is_alive, 
                        -1 if new_agent.is_alive else -1001)
            )
        elif action == Action.TurnLeft or action == Action.TurnRight:
            self.agent.orientation.turn(action)
            return (
                self,
                Percept(self.is_stench(), self.is_breeze(), 
                           self.is_glitter(), False, 
                           False, False, 
                           -1)
            )
        elif action == Action.Grab:
            new_agent = copy.copy(self.agent)
            new_agent.has_gold = self.is_glitter()
            new_environment = copy.deepcopy(self)
            new_environment.gold_location = new_agent.location if new_agent.has_gold else self.gold_location
            new_environment.agent = new_agent
            return (
                new_environment,
                Percept(self.is_stench(), self.is_breeze(), 
                           self.is_glitter(), False, 
                           False, False, 
                           -1)                
            )
        elif action == Action.Climb:
            at_start_location = self.agent.location == Coords(0,0)
            success = self.agent.has_gold and at_start_location
            is_terminated = success or (self.allow_climb_without_gold and at_start_location)
            return(
                self,
                Percept(self.is_stench(), self.is_breeze(), self.is_glitter(), False, False, is_terminated, 
                        999 if success else -1)
            )
        elif action == Action.Shoot:
            had_arrow = self.agent.has_arrow
            wumpus_killed = self.kill_attempt_successful()
            new_agent = copy.copy(self.agent)
            new_agent.has_arrow = False
            
            new_environment = copy.deepcopy(self)
            new_environment.agent = new_agent
            new_environment.wumpus_alive = new_environment.wumpus_alive and not wumpus_killed
            return(
                new_environment,
                Percept(self.is_stench(), self.is_breeze(), self.is_glitter(), False,
                        wumpus_killed, False, -11 if had_arrow else -1)
            )
    
    def visualize(self) -> str:
        wumpus_symbol = "W" if self.wumpus_alive else "w"
        
        board = ""
        board += '  ---------------------\n'
        for y in range(self.grid_height-1 , -1, -1):
            board += str(y + 1).zfill(2) + "|"
            for x in range(0, self.grid_width):
                posn = Coords(x, y)
                isA = "A" if self.is_agent_at(posn) else " "
                isP = "P" if self.is_pit_at(posn) else " "
                isG = "G" if self.is_gold_at(posn) else " "
                isW = wumpus_symbol if self.is_wumpus_at(posn) else " "
                sym =  isA + isP + isG + isW
                board += sym
                board += "|"
            board += "\n" #if y > 0  else "" 
        board += '  ---------------------'
        colsIdx = [str(x+1).zfill(2) for x in range(0, self.grid_width)]
        board += '\n    ' + '   '.join(colsIdx)
        return board