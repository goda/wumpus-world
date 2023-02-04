from environment.gent import Agent
from environment.Misc import Coords


class Environment():
    """A class to hold the environment configuration including methods for simulating 
    Agent actions etc.
    """
    grid_width: int = 4
    grid_height: int = 4
    pit_prob: float = 0.2
    allow_climb_without_gold: bool = False
    agent: Agent = Agent()
    pit_locations = []
    terminated: bool = False
    wumpus_location: Coords
    wumpus_alive: bool = True
    gold_location: Coords

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

    def kill_attempt_successful