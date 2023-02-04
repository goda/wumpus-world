import random
from wumpus.src.environment.Misc import Action, Percept


class Agent:
    """A class representing the Agent and its base implementation
    """

    def __init__(self) -> None:
        pass

    def next_action(percept: Percept) -> Action:
        pass


class NaiveAgent(Agent):
    def __init__(self) -> None:
        pass

    def next_action(self, percept: Percept) -> Action:
        # return Action(random.randint(int(Action.Forward), int(Action.TurnRight)))
        return Action(random.randint(int(Action.Forward), int(Action.Climb)))
