# from wumpus.src.environments import Environment
import copy
import random
from wumpus.src.agent.Agents import NaiveAgent
from wumpus.src.environment.Misc import Action, OrientationState, Percept
from wumpus.src.environment.Agent import Agent
from wumpus.src.environment.Environments import Coords
from wumpus.src.environment.Environments import Environment
from wumpus.src.environment.Misc import Orientation
import unittest


class TestEnvironment(unittest.TestCase):
    """Class for testing `src.environment.environments.Environment`

    Args:
        unittest (_type_): _description_
    """

    def test_cords_eq(self):
        c = Coords(1, 2)
        d = Coords(1, 2)
        assert (c == d)

        d = Coords(2, 2)
        assert (c != d)

    def test_environment_pit_locations(self):
        e = Environment()
        p1 = Coords(4, 2)
        p2 = Coords(3, 2)
        e.pit_locations = []
        e.pit_locations.append(p1)
        e.pit_locations.append(p2)

        false_potential_loc = Coords(3, 3)
        true_potential_loc = Coords(3, 2)

        assert (e.is_pit_at(false_potential_loc) == False)
        assert (e.is_pit_at(true_potential_loc) == True)

    def test_environment_wumpus_location(self):
        e = Environment()
        wumpus_location = Coords(4, 2)
        e.wumpus_location = wumpus_location

        false_potential_loc = Coords(3, 3)
        true_potential_loc = Coords(4, 2)

        assert (e.is_wumpus_at(false_potential_loc) == False)
        assert (e.is_wumpus_at(true_potential_loc) == True)

    def test_environment_agent_location(self):
        e = Environment()
        e.agent = Agent()
        e.agent.location = Coords(4, 2)

        false_potential_loc = Coords(3, 3)
        true_potential_loc = Coords(4, 2)

        assert (e.is_agent_at(false_potential_loc) == False)
        assert (e.is_agent_at(true_potential_loc) == True)

    def test_environment_glitter(self):
        e = Environment()
        e.gold_location = Coords(4, 2)
        e.agent.location = Coords(4, 2)
        assert (e.is_glitter() == True)
        e.agent.location = Coords(4, 3)
        assert (e.is_glitter() == False)

    def test_environment_gold_location(self):
        e = Environment()
        e.gold_location = Coords(4, 2)
        false_potential_loc = Coords(3, 3)
        true_potential_loc = Coords(4, 2)

        assert (e.is_gold_at(false_potential_loc) == False)
        assert (e.is_gold_at(true_potential_loc) == True)
        
    def test_environment_terminated(self):
        e = Environment()
        e.agent.location = e.wumpus_location
        print(e.visualize())
        assert(e.agent.location == e.wumpus_location)

    def test_environment_kill_attempt_successful(self):
        e = Environment()
        e.wumpus_location = Coords(1,2)
        e.agent.location = Coords(1, 1)
        
        # in line of sight TRUE
        e.agent.orientation.state = OrientationState.North
        assert(e.wumpus_in_line_of_fire())
        # not in line of sight FALSE
        e.agent.orientation.state = OrientationState.South
        assert(e.wumpus_in_line_of_fire() == False)
        # no arrow - can't kill
        e.agent.has_arrow = False
        e.agent.orientation.state = OrientationState.North
        assert(e.kill_attempt_successful() == False)
        # arrow and in line of sight 
        e.agent.has_arrow = True
        e.agent.orientation.state = OrientationState.North
        assert(e.kill_attempt_successful())    
        
    def test_adjacent_cells(self):
        e = Environment()
        c = Coords(0, 0)
        adjacent_cells = e.adjacent_cells(c)
        assert(Coords(0,1) in adjacent_cells)  
        assert(Coords(1,0) in adjacent_cells)  
        
        c = Coords(2, 1)
        adjacent_cells = e.adjacent_cells(c)
        assert(Coords(2,2) in adjacent_cells)  
        assert(Coords(1,1) in adjacent_cells)  
        assert(Coords(3,1) in adjacent_cells)  
        assert(Coords(1,1) in adjacent_cells)     
        
    def test_is_pit_adjacent(self):
        e = Environment()
        c = Coords(0, 0)

        # add pits next to c
        e.pit_locations = [Coords(1,0)]
        assert(e.is_pit_adjacent(c))
        
        # move c 
        c = Coords(3,2)
        assert(e.is_pit_adjacent(c) == False)   
        
    def test_is_wumpus_adjacent(self):
        e = Environment()
        c = Coords(0, 0)

        # add wumpus next to c
        e.wumpus_location = Coords(1,0)
        assert(e.is_wumpus_adjacent(c))
        
        # move c 
        c = Coords(3,2)
        assert(e.is_wumpus_adjacent(c) == False)         
        
    def test_is_breeze(self):
        e = Environment()
        e.agent.location = Coords(0, 0)

        # add wumpus next to agent
        e.pit_locations = [Coords(1,0)]
        assert(e.is_breeze())
        
        # move agent
        e.agent.location = Coords(3,2)
        assert(e.is_breeze() == False)  

    def test_is_stench(self):
        e = Environment()
        e.agent.location = Coords(1, 2)

        # add wumpus next to agent
        e.wumpus_location = Coords(1,3)
        assert(e.is_stench())
        
        # move agent
        e.agent.location = Coords(3,2)
        assert(e.is_stench() == False)             
        
        
    def test_visualize(self):
        e = Environment()     
        e.agent.location = Coords(0, 0)
        e.gold_location = Coords(1,3)
        e.pit_locations = []

        # add wumpus next to agent
        e.wumpus_location = Coords(1,0)
        board = e.visualize()
        # print('\n*888888')
        # print(board)        
        # print('\n')
        assert(board == '|    |  G |    |    |\n|    |    |    |    |\n|    |    |    |    |\n|A   |   W|    |    |\n')
        
    def test_init_environment(self):
        e = Environment(4, 4, 0.2, False)
        
        assert(Coords(0,0) not in e.pit_locations)

class TestOrientation(unittest.TestCase):
    """Class for testing `src.environment.misc.Orientation`

    Args:
        unittest (_type_): _description_
    """

    def test_orientation_turn_left(self):
        o = Orientation(OrientationState.North)

        o.turn_left()
        assert (o.state == OrientationState.West)
        o.turn_left()
        assert (o.state == OrientationState.South)
        o.turn_left()
        assert (o.state == OrientationState.East)
        o.turn_left()
        assert (o.state == OrientationState.North)

    def test_orientation_turn_right(self):
        o = Orientation(OrientationState.North)

        o.turn_right()
        assert (o.state == OrientationState.East)
        o.turn_right()
        assert (o.state == OrientationState.South)
        o.turn_right()
        assert (o.state == OrientationState.West)
        o.turn_right()
        assert (o.state == OrientationState.North)

    def test_environment_copy(self):
        (e, p) = Environment.initialize()
        a = Agent()
        e.agent = a
        
        new_env = copy.deepcopy(e)
        a.is_alive = not a.is_alive
        assert(new_env.agent.is_alive != e.agent.is_alive)

class TestAgent(unittest.TestCase):
    """Class for testing agent methods

    Args:
        unittest (_type_): _description_
    """

    def test_copy_agent(self):
        a = Agent()
        a.orientation = Orientation(OrientationState.West)
        a.has_arrow = True
        
        b = copy.copy(a)
        assert(a.orientation == b.orientation)
        a.orientation = Orientation(OrientationState.East)
        assert(a.orientation != b.orientation)
        

    # def test_action(self):
    #     a = NaiveAgent()
    #     next_action = a.next_action(Percept(
    #         False,
    #         False,
    #         False,
    #         False,
    #         False,
    #         False,
    #         False
    #     ))
    #     print(next_action)
    #     # print(str(int(Action.Forward)))
    #     # print(random.randint(int(Action.Forward), int(Action.Climb)))
        
        
# class TestWumpusWorld(unittest.TestCase):
#     def test_init(self):
#         (initial_env, initial_percept) = Environment.initialize(4, 4, 0, False)
#         print(initial_env.visualize())


if __name__ == '__main__':
    unittest.main()
