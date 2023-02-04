import random
from environment.Misc import Action, Percept


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

    def next_action(percept: Percept) -> Action:
        return Action(random.randint(Action.Forward, Action.Climb))
