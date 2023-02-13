import copy
import unittest
from wumpus.src.agent.Agents import BeelineAgent, NaiveAgent
from wumpus.src.agent.Misc import WumpusDiGraph
from wumpus.src.environment.Misc import Action, OrientationState, Percept, WumpusEdge, WumpusNode
from wumpus.src.environment.Agent import Agent
from wumpus.src.environment.Environments import Coords
from wumpus.src.environment.Environments import Environment
from wumpus.src.environment.Misc import Orientation
import matplotlib.pyplot as plt
import networkx as nx


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
        assert(board == '  ---------------------\n04|    |  G |    |    |\n03|    |    |    |    |\n02|    |    |    |    |\n01|A   |   W|    |    |\n  ---------------------\n    01   02   03   04')
        
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
        
class TestWumpusWorld(unittest.TestCase):
    def test_grab_gold_and_climb_out(self):
        (initial_env, initial_percept) = Environment.initialize(4, 4, 0, False)
        
        # place gold at agent location
        initial_env.gold_location = initial_env.agent.location
        # action grab gold
        next_action = Action.Grab
        # apply action
        (next_environment, next_percept) = initial_env.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())
        
        # action move 
        next_action = Action.Forward
        # apply action
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())        
        
        # action -  turn around 
        next_action = Action.TurnLeft
        # apply action
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        next_action = Action.TurnLeft
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        next_action = Action.Forward
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())      
        
        # try climb out 
        next_action = Action.Climb
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # print(next_percept.reward)
        assert(next_percept.reward == 999)

class TestNaiveAgent(unittest.TestCase):
    def test_allowed_actions(self):
        a = NaiveAgent()
        allowed_actions = [Action.Climb]
        random_action = a.random_action(allowed_actions)
        assert(random_action == Action.Climb)
        
        
class TestAction(unittest.TestCase):
    def test_get_all(self):
        all_actions = Action.get_all()
        assert(len(all_actions) == 6)

class TestWumpusNodeAndEdge(unittest.TestCase):
    n1 = WumpusNode(1, Coords(1,1), orientation_state=OrientationState.East)
    n2 = WumpusNode(2, Coords(2,1), orientation_state=OrientationState.East)
    n3 = WumpusNode(3, Coords(3,1), orientation_state=OrientationState.East)
    G = WumpusDiGraph()
    G.add_nodes_from([n1, n2, n3])
    G.add_edge(n1,n2, object=WumpusEdge(OrientationState.East))
    G.add_edge(n2,n3, object=WumpusEdge(OrientationState.East))
        
    def test_str(self):
        n = WumpusNode(1, Coords(1,1), orientation_state=OrientationState.East)
        assert(str(n) == '{id: 1, L: (x: 1, y: 1), O: East}')

    def test_node_and_edge(self):
        n1 = WumpusNode(1, Coords(1,1), orientation_state=OrientationState.East)
        n2 = WumpusNode(2, Coords(2,1), orientation_state=OrientationState.East)
        n3 = WumpusNode(3, Coords(3,1), orientation_state=OrientationState.East)
        G = nx.DiGraph()
        G.add_nodes_from([n1, n2, n3])
        G.add_edge(n1,n2, object=WumpusEdge(OrientationState.East))
        G.add_edge(n2,n3, object=WumpusEdge(OrientationState.East))
        # nx.draw(G, with_labels=True)
        # plt.show()
        
    def test_find_node(self):
        assert(self.G.find_node(Coords(1,1)) is not None)
        assert(self.G.find_node(Coords(3,3)) is None)
        


class TestBeelineAgent(unittest.TestCase):
    
    def test_init_graph(self):
        a = BeelineAgent()
        a.init_graph(Coords(1,1), orientation_state=OrientationState.East)
        subax1 = plt.subplot(121)
        # nx.draw(a.G, with_labels=True)
        # plt.show()

    # def test_next_action(self):
    #     a = BeelineAgent()
    #     a.init_graph(Coords(1,1), orientation_state=OrientationState.East)
    #     a.has_gold = True
    #     p = Percept(glitter=False)
        
    #     for i in range(0,10):
    #         next_action = a.next_action(p)
    #         assert(next_action.name != Action.Grab.name)

    def test_grab_gold_and_climb_out(self):
        (initial_env, initial_percept) = Environment.initialize(4, 4, 0, False)
        agent = BeelineAgent()
        agent.init_graph(Coords(0,0), OrientationState.East)

        
        # place gold at agent location
        initial_env.gold_location = initial_env.agent.location
        # action grab gold - ignoring what the agent decided to do
        next_action = Action.Grab
        # get next action from agent 
        next_action = agent.next_action(initial_env.agent.location, initial_percept,
                                        debug_action=next_action)

        # apply action
        (next_environment, next_percept) = initial_env.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())
        
        # # get next action from agent 
        next_action = Action.Forward
        next_action = agent.next_action(next_environment.agent.location, next_percept,
                                        debug_action=next_action)
        # action move 
        # apply action
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())        


        # action -  turn around 
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_environment.agent.location, next_percept,
                                        debug_action=next_action)        

        # apply action
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_environment.agent.location, next_percept,
                                        debug_action=next_action)
                
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        next_action = Action.Forward
        next_action = agent.next_action(next_environment.agent.location, next_percept,
                                        debug_action=next_action)
                
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())
        
        
        # # try climb out 
        next_action = Action.Climb
        next_action = agent.next_action(next_environment.agent.location, next_percept,
                                        debug_action=next_action)
                
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        # # print(next_percept.reward)
        agent.display_graph()          
        # print('sfsdfs')
        # subax1 = plt.subplot(121)
        # nx.draw(agent.graph, with_labels=True)
        # plt.show()
        
        # assert(next_percept.reward == 999)

if __name__ == '__main__':
    unittest.main()
