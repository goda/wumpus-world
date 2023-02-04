# from Environments import Environment
from src.environment.Agent import Agent
from src.environment.Environments import Coords
from src.environment.Environments import Environment


def test_cords_eq():
    c = Coords(1, 2)
    d = Coords(1, 2)
    assert (c == d)

    d = Coords(2, 2)
    assert (c != d)


def test_environment_pit_locations():
    e = Environment()
    p1 = Coords(4, 2)
    p2 = Coords(3, 2)
    e.pit_locations.append(p1)
    e.pit_locations.append(p2)

    false_potential_loc = Coords(3, 3)
    true_potential_loc = Coords(3, 2)

    assert (e.is_pit_at(false_potential_loc) == False)
    assert (e.is_pit_at(true_potential_loc) == True)


def test_environment_wumpus_location():
    e = Environment()
    wumpus_location = Coords(4, 2)
    e.wumpus_location = wumpus_location

    false_potential_loc = Coords(3, 3)
    true_potential_loc = Coords(4, 2)

    assert (e.is_wumpus_at(false_potential_loc) == False)
    assert (e.is_wumpus_at(true_potential_loc) == True)


def test_environment_agent_location():
    e = Environment()
    e.agent = Agent()
    e.agent.location = Coords(4, 2)

    false_potential_loc = Coords(3, 3)
    true_potential_loc = Coords(4, 2)

    assert (e.is_agent_at(false_potential_loc) == False)
    assert (e.is_agent_at(true_potential_loc) == True)


def test_environment_glitter():
    e = Environment()
    e.gold_location = Coords(4, 2)
    e.agent.location = Coords(4, 2)
    assert (e.is_glitter() == True)
    e.agent.location = Coords(4, 3)
    assert (e.is_glitter() == False)


def test_environment_gold_location():
    e = Environment()
    e.gold_location = Coords(4, 2)
    false_potential_loc = Coords(3, 3)
    true_potential_loc = Coords(4, 2)

    assert (e.is_gold_at(false_potential_loc) == False)
    assert (e.is_gold_at(true_potential_loc) == True)


test_cords_eq()
test_environment_pit_locations()
test_environment_wumpus_location()
test_environment_agent_location()
test_environment_glitter()
test_environment_gold_location()
