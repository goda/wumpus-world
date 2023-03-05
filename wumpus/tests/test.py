import copy
from typing import List
import unittest
from wumpus.src.agent.Agents import BeelineAgent, NaiveAgent, ProbAgent
from wumpus.src.agent.Misc import WumpusBayesianNetwork, WumpusDiGraph, WumpusEdge, WumpusNode
from wumpus.src.environment.Misc import Action, OrientationState, Percept
from wumpus.src.environment.Agent import Agent
from wumpus.src.environment.Environments import Coords
from wumpus.src.environment.Environments import Environment
from wumpus.src.environment.Misc import Orientation
import matplotlib.pyplot as plt
import networkx as nx
from pomegranate import Node, BayesianNetwork, ConditionalProbabilityTable
from pomegranate.distributions import DiscreteDistribution


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
        e.wumpus_location = Coords(1, 2)
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
        assert(Coords(0, 1) in adjacent_cells)
        assert(Coords(1, 0) in adjacent_cells)

        c = Coords(2, 1)
        adjacent_cells = e.adjacent_cells(c)
        assert(Coords(2, 2) in adjacent_cells)
        assert(Coords(1, 1) in adjacent_cells)
        assert(Coords(3, 1) in adjacent_cells)
        assert(Coords(1, 1) in adjacent_cells)

    def test_is_pit_adjacent(self):
        e = Environment()
        c = Coords(0, 0)

        # add pits next to c
        e.pit_locations = [Coords(1, 0)]
        assert(e.is_pit_adjacent(c))

        # move c
        c = Coords(3, 2)
        assert(e.is_pit_adjacent(c) == False)

    def test_is_wumpus_adjacent(self):
        e = Environment()
        c = Coords(0, 0)

        # add wumpus next to c
        e.wumpus_location = Coords(1, 0)
        assert(e.is_wumpus_adjacent(c))

        # move c
        c = Coords(3, 2)
        assert(e.is_wumpus_adjacent(c) == False)

    def test_is_breeze(self):
        e = Environment()
        e.agent.location = Coords(0, 0)

        # add wumpus next to agent
        e.pit_locations = [Coords(1, 0)]
        assert(e.is_breeze())

        # move agent
        e.agent.location = Coords(3, 2)
        assert(e.is_breeze() == False)

    def test_is_stench(self):
        e = Environment()
        e.agent.location = Coords(1, 2)

        # add wumpus next to agent
        e.wumpus_location = Coords(1, 3)
        assert(e.is_stench())

        # move agent
        e.agent.location = Coords(3, 2)
        assert(e.is_stench() == False)

    def test_visualize(self):
        e = Environment()
        e.agent.location = Coords(0, 0)
        e.gold_location = Coords(1, 3)
        e.pit_locations = []

        # add wumpus next to agent
        e.wumpus_location = Coords(1, 0)
        board = e.visualize()
        assert(board == '  ---------------------\n04|    |  G |    |    |\n03|    |    |    |    |\n02|    |    |    |    |\n01|A   |   W|    |    |\n  ---------------------\n    01   02   03   04')

    def test_init_environment(self):
        e = Environment(4, 4, 0.2, False)

        assert(Coords(0, 0) not in e.pit_locations)

    def test_init_environments_multiple(self):
        (e, p) = Environment.initialize()
        next_action = Action.TurnLeft
        (next_environment, next_percept) = e.apply_action(next_action)
        assert(next_environment.agent.orientation.state == OrientationState.North)

        (new_e, p) = Environment.initialize()
        assert(new_e.agent.orientation.state == OrientationState.East)


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

    def test_reverse_orientation(self):
        o = OrientationState.East
        assert(OrientationState.opposite_orientation(
            o).name == OrientationState.West.name)


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

    def test_opposite_turn(self):
        a = Action.TurnRight
        assert(Action.opposite_turn(a) == Action.TurnLeft)
        a = Action.TurnLeft
        assert(Action.opposite_turn(a) == Action.TurnRight)


class TestWumpusNodeAndEdge(unittest.TestCase):
    n1 = WumpusNode(Coords(1, 1), orientation_state=OrientationState.East)
    n2 = WumpusNode(Coords(2, 1), orientation_state=OrientationState.East)
    n3 = WumpusNode(Coords(3, 1), orientation_state=OrientationState.East)
    G = WumpusDiGraph()
    G.add_nodes_from([n1, n2, n3])
    G.add_edge(n1, n2, object=WumpusEdge(Action.Forward))
    G.add_edge(n2, n3, object=WumpusEdge(Action.Forward))

    def test_str(self):
        n = WumpusNode(Coords(1, 1), orientation_state=OrientationState.East)
        assert(str(n) == '{L: (x: 1, y: 1), O: East}')

    def test_node_and_edge(self):
        n1 = WumpusNode(Coords(1, 1), orientation_state=OrientationState.East)
        n2 = WumpusNode(Coords(2, 1), orientation_state=OrientationState.East)
        n3 = WumpusNode(Coords(3, 1), orientation_state=OrientationState.East)
        G = nx.DiGraph()
        G.add_nodes_from([n1, n2, n3])
        G.add_edge(n1, n2, object=WumpusEdge(Action.Forward))
        G.add_edge(n2, n3, object=WumpusEdge(Action.Forward))
        # nx.draw(G, with_labels=True)
        # plt.show()

    def test_find_node(self):
        assert(self.G.find_node_location(Coords(1, 1)) is not None)
        assert(self.G.find_node_location(Coords(3, 3)) is None)


class TestBeelineAgent(unittest.TestCase):

    def test_init_graph(self):
        a = BeelineAgent()
        a.init_graph(Coords(1, 1), orientation_state=OrientationState.East)
        assert(a.current_node.location == Coords(1, 1))
        # subax1 = plt.subplot(121)
        # nx.draw(a.G, with_labels=True)
        # plt.show()

    def test_next_action(self):
        a = BeelineAgent()
        a.init_graph(Coords(1, 1), orientation_state=OrientationState.East)
        a.has_gold = False
        p = Percept(glitter=False)

        for i in range(0, 10):
            next_action = a.next_action(p)
            assert(next_action.name != Action.Grab.name)

    def test_forward(self):
        agent = BeelineAgent()

        new_coords = agent.forward(agent.current_node)
        assert(new_coords == Coords(1, 0))
        new_coords = agent.forward(WumpusNode(
            new_coords, OrientationState.East))
        assert(new_coords == Coords(2, 0))
        new_coords = agent.forward(WumpusNode(
            new_coords, OrientationState.East))
        assert(new_coords == Coords(3, 0))

    def test_grab_gold_and_climb_out(self):
        # 1. Setup environment
        (initial_env, initial_percept) = Environment.initialize(4, 4, 0, False)
        agent = BeelineAgent()  # NaiveAgent()
        # agent.init_graph(Coords(0,0), OrientationState.East)
        # place gold at 2,0
        initial_env.gold_location = Coords(2, 0)

        # 2.START AGENT ACTIONS
        # 2. move forward
        next_action = Action.Forward
        next_action = agent.next_action(initial_percept,
                                        debug_action=next_action)

        # action move
        # apply action
        (next_environment, next_percept) = initial_env.apply_action(
            next_action)        # print('---------------------')

        # action -  turn around
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_percept,
                                        debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # apply action
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_percept,
                                        debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # apply action
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_percept,
                                        debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # apply action
        next_action = Action.TurnLeft
        next_action = agent.next_action(next_percept,
                                        debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = Action.Forward
        next_action = agent.next_action(next_percept,
                                        debug_action=next_action)

        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # # try next action yourself
        next_action = agent.next_action(next_percept)
        assert(next_action == Action.Grab)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # # SHOULD BE EXITING NOW
        next_action = agent.next_action(next_percept)
        assert(next_action == Action.TurnLeft)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = agent.next_action(next_percept)
        assert(next_action == Action.TurnLeft)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = agent.next_action(next_percept)
        assert(next_action == Action.Forward)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = agent.next_action(next_percept)
        assert(next_action == Action.Forward)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = agent.next_action(next_percept)
        assert(next_action == Action.Climb)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        # print('---------------------')
        # print(next_environment.visualize())
        # print('---------------------')
        # print(next_percept.show())

    def test_walk_into_wall(self):
        # 1. Setup environment
        (initial_env_bee, initial_percept_bee) = Environment.initialize(4, 4, 0, False)
        beeAgent = BeelineAgent()
        beeAgent.init_graph(Coords(0, 0), OrientationState.East)
        # place gold at 2,0
        initial_env_bee.gold_location = Coords(2, 1)

        # 2.START AGENT ACTIONS
        # 2. move forward
        next_action_bee = Action.Forward
        next_action_bee = beeAgent.next_action(initial_percept_bee,
                                               debug_action=next_action_bee)
        (next_environment_bee, next_percept_bee) = initial_env_bee.apply_action(
            next_action_bee)        # print('---------------------')

        next_action_bee = Action.Forward
        next_action_bee = beeAgent.next_action(next_percept_bee,
                                               debug_action=next_action_bee)
        (next_environment_bee, next_percept_bee) = next_environment_bee.apply_action(
            next_action_bee)

        next_action_bee = Action.Forward
        next_action_bee = beeAgent.next_action(next_percept_bee,
                                               debug_action=next_action_bee)
        (next_environment_bee, next_percept_bee) = next_environment_bee.apply_action(
            next_action_bee)
        assert(next_environment_bee.agent.location == Coords(3, 0))

        next_action_bee = Action.Forward
        next_action_bee = beeAgent.next_action(next_percept_bee,
                                               debug_action=next_action_bee)
        (next_environment_bee, next_percept_bee) = next_environment_bee.apply_action(
            next_action_bee)
        assert(next_environment_bee.agent.location == Coords(3, 0))

    def test_zig_zag_route(self):
        """Tests zig-zag walk and whether the agent
        will connect adjacent nodes that it didn't traverse directly
        """

        # 1. Setup environment
        (initial_env_bee, initial_percept_bee) = Environment.initialize(4, 4, 0, False)
        beeAgent = BeelineAgent()
        beeAgent.init_graph(Coords(0, 0), OrientationState.East)
        # place gold at 2,0
        initial_env_bee.gold_location = Coords(0, 2)

        # 2.START AGENT ACTIONS
        # 2. move forward
        next_action = Action.Forward
        next_action = beeAgent.next_action(initial_percept_bee,
                                           debug_action=next_action)
        (next_environment, next_percept) = initial_env_bee.apply_action(
            next_action)        # print('---------------------')

        next_action = Action.TurnLeft
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = Action.Forward
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(1, 1))

        next_action = Action.TurnLeft
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = Action.Forward
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(0, 1))
        # beeAgent.graph.display_graph()

        next_action = Action.Forward
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(0, 1))
        # beeAgent.graph.display_graph()

        # turn north so we can grab gold in next cell
        next_action = Action.TurnRight
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(0, 1))
        # beeAgent.graph.display_graph()

        next_action = Action.Forward
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(0, 2))

        # beeAgent.graph.display_graph()

        # agent should grab now
        next_action = beeAgent.next_action(next_percept,
                                           debug_action=next_action)
        (next_environment, next_percept) = next_environment.apply_action(next_action)
        assert(next_environment.agent.location == Coords(0, 2))
        assert(next_action == Action.Grab)

        # beeAgent.graph.display_graph()

        # SHOULD BE EXITING NOW
        next_action = beeAgent.next_action(next_percept)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = beeAgent.next_action(next_percept)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = beeAgent.next_action(next_percept)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = beeAgent.next_action(next_percept)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

        next_action = beeAgent.next_action(next_percept)
        (next_environment, next_percept) = next_environment.apply_action(next_action)

    def test_failing_route(self):
        """Tests scenario where gold is at 1,1 and agent goes to it from 1,2 and
        is not able to go back to starting point via 0,1 which it also traversed
        """

        # 1. Setup environment
        (env, percept) = Environment.initialize(4, 4, 0, False)
        beeAgent = BeelineAgent()
        beeAgent.init_graph(Coords(0, 0), OrientationState.East)
        # place gold at 2,0
        env.gold_location = Coords(1, 1)
        env.wumpus_location = Coords(3, 3)

        actions_to_gold = [
            Action.Forward,
            Action.Forward,
            Action.Shoot,
            Action.TurnLeft,
            Action.TurnRight,
            Action.TurnLeft,
            Action.Shoot,
            Action.TurnRight,
            Action.TurnRight,
            Action.Forward,
            Action.Shoot,
            Action.TurnRight,
            Action.TurnRight,
            Action.TurnLeft,
            Action.Forward,
            Action.Forward,
            Action.Forward,
            Action.TurnRight,
            Action.Shoot,
            Action.Forward,
            Action.TurnLeft,
            Action.Forward,
            Action.TurnLeft,
            Action.TurnRight,
            Action.Forward,
            Action.Shoot,
            Action.TurnLeft,
            Action.Shoot,
            Action.Shoot,
            Action.Shoot,
            Action.Forward,
            Action.TurnLeft,
            Action.Shoot,
            Action.TurnLeft,
            Action.TurnLeft,
            Action.TurnRight,
            Action.TurnRight,
            Action.Forward,
            Action.Shoot,
            Action.Forward,
            Action.TurnLeft,
            Action.Shoot,
            Action.TurnRight,
            Action.TurnRight,
            Action.TurnRight,
            Action.TurnRight,
            Action.TurnRight,
            Action.Shoot,
            Action.Shoot,
            Action.TurnLeft,
            Action.Forward,
            Action.Forward,
            Action.Shoot,
            Action.TurnRight,
            Action.TurnRight,
            Action.TurnRight,
            Action.Forward,
            Action.TurnLeft,
            Action.Shoot,
            Action.Forward,
            Action.Grab
        ]
        # 2.START AGENT ACTIONS
        for a in actions_to_gold:
            next_action = a
            next_action = beeAgent.next_action(percept,
                                               debug_action=next_action)
            # print('---------------------')
            (env, percept) = env.apply_action(next_action)
            # print("Action: ", str(next_action.name), "| Agent Orientation: ", env.agent.orientation.state.name)
            # print(env.visualize())
            # print(percept.show())

        # agent should grab now
        next_action = beeAgent.next_action(percept,
                                           debug_action=next_action)
        (env, percept) = env.apply_action(next_action)

        next_action = beeAgent.next_action(percept,
                                           debug_action=next_action)
        (env, percept) = env.apply_action(next_action)
        # SHOULD BE EXITING NOW
        for _ in range(0, len(beeAgent.exit_path_actions)):
            next_action = beeAgent.next_action(percept)
            (env, percept) = env.apply_action(next_action)
            # print(env.visualize())
            # print(percept.show())

        assert(percept.reward == 999)


class TestProbAgent(unittest.TestCase):
    def test_init_prob_agent(self):
        probAgent: ProbAgent = ProbAgent()
        assert(probAgent.pits_breeze_graph is not None)
        assert(probAgent.wumpus_stench_graph is not None)

    def test_prepare_prob_graphs(self):
        probAgent: ProbAgent = ProbAgent()
        probAgent.pits_breeze_graph = probAgent.prepare_prob_graph(
            grid_width=4,
            grid_height=4,
            independent_prob=0.2,
            indepndent_prob_node_label='pit',
            dependent_prob_node_label='breeze'
        )

        probAgent.wumpus_stench_graph = probAgent.prepare_prob_graph(
            grid_width=4,
            grid_height=4,
            independent_prob=1./4/4,
            indepndent_prob_node_label='wumpus',
            dependent_prob_node_label='stench'
        )

    def test_update_graph_based(self):
        grid_width = 3
        grid_height = 3
        model: BayesianNetwork = None
        probAgent: ProbAgent = ProbAgent(
            grid_width=grid_width,
            grid_height=grid_height
        )
        probAgent.pits_breeze_graph = probAgent.prepare_prob_graph(
            grid_height=grid_height,
            grid_width=grid_width,
            independent_prob=0.2,
            indepndent_prob_node_label='pit',
            dependent_prob_node_label='breeze'
        )

        probAgent.wumpus_stench_graph = probAgent.prepare_prob_graph_wumpus(
            grid_width=grid_width,
            grid_height=grid_height,
            independent_prob=1./(grid_height*grid_height-1),
            indepndent_prob_node_label='wumpus',
            dependent_prob_node_label='stench'
        )
        probAgent.wumpus_stench_graph.plot()
        print('Done updating')

        model: WumpusBayesianNetwork = probAgent.wumpus_stench_graph
        updated_probs = model.get_node_probabilities_for_evidence(
            {'stench@(x: 0, y: 0)': 'F'})
        assert(updated_probs['wumpus@(x: 1, y: 0)']['T'] == 0)

        updated_probs = model.get_node_probabilities_for_evidence(
            {
                'stench@(x: 0, y: 0)': 'F',
                'stench@(x: 0, y: 1)': 'T',
                'stench@(x: 1, y: 1)': 'F',
                'stench@(x: 1, y: 2)': 'T',
                'stench@(x: 2, y: 1)': 'F',
                'stench@(x: 2, y: 2)': 'F',
            })
        # print(updated_probs)
        model.plot()
        # assert(updated_probs['wumpus@(x: 0, y: 2)'][''] = 0)

    def test_dynamic_wumpus_stench_same_loc(self):
        grid_width = 3
        grid_height = 3

        def wumpus_stench_same_loc_dist_one_location(x): return [
            # since no wumpus at this loc, the prob no stench, is
            # the revised generic wumpus prob 1/(num wumpus loc - 1) to the
            # power of locations (x) that could give off stench
            ['F', 'F', (1 - 1./(grid_height*grid_height-2))**x],
            ['F', 'T', (1./(grid_height*grid_height-2))*x],
            ['T', 'F', 0.],
            ['T', 'T', 1.]
        ]
        print(wumpus_stench_same_loc_dist_one_location(2))

    # def test_wumpus_network(self):
    #     grid_width = 3
    #     grid_height = 3
    #     model: BayesianNetwork = None
    #     probAgent: ProbAgent = ProbAgent(
    #         grid_width=grid_width,
    #         grid_height=grid_height
    #     )
    #     probAgent.pits_breeze_graph = probAgent.prepare_prob_graph(
    #         grid_height=grid_height,
    #         grid_width=grid_width,
    #         independent_prob=0.2,
    #         indepndent_prob_node_label='pit',
    #         dependent_prob_node_label='breeze'
    #     )

    #     probAgent.wumpus_stench_graph = probAgent.prepare_prob_graph_wumpus(
    #         grid_width=grid_width,
    #         grid_height=grid_height,
    #         independent_prob=1./(grid_height*grid_height-1),
    #         indepndent_prob_node_label='wumpus',
    #         dependent_prob_node_label='stench'
    #     )
        # probAgent.wumpus_stench_graph.plot()


class TestWumpusBayesianNetwork(unittest.TestCase):
    def get_monty_game_network(self) -> WumpusBayesianNetwork:
        # Initially the door selected by the guest is completely random
        guest = DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})

        # The door containing the prize is also a random process
        prize = DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})

        # The door Monty picks, depends on the choice of the guest and the prize door
        monty = ConditionalProbabilityTable(
            [
                ['A', 'A', 'A', 0.0],
                ['A', 'A', 'B', 0.5],
                ['A', 'A', 'C', 0.5],
                ['A', 'B', 'A', 0.0],
                ['A', 'B', 'B', 0.0],
                ['A', 'B', 'C', 1.0],
                ['A', 'C', 'A', 0.0],
                ['A', 'C', 'B', 1.0],
                ['A', 'C', 'C', 0.0],
                ['B', 'A', 'A', 0.0],
                ['B', 'A', 'B', 0.0],
                ['B', 'A', 'C', 1.0],
                ['B', 'B', 'A', 0.5],
                ['B', 'B', 'B', 0.0],
                ['B', 'B', 'C', 0.5],
                ['B', 'C', 'A', 1.0],
                ['B', 'C', 'B', 0.0],
                ['B', 'C', 'C', 0.0],
                ['C', 'A', 'A', 0.0],
                ['C', 'A', 'B', 1.0],
                ['C', 'A', 'C', 0.0],
                ['C', 'B', 'A', 1.0],
                ['C', 'B', 'B', 0.0],
                ['C', 'B', 'C', 0.0],
                ['C', 'C', 'A', 0.5],
                ['C', 'C', 'B', 0.5],
                ['C', 'C', 'C', 0.0]], [guest, prize])

        d1 = Node(guest, name="guest")
        d2 = Node(prize, name="prize")
        d3 = Node(monty, name="monty")

        # Building the Bayesian Network
        network = WumpusBayesianNetwork(
            "Solving the Monty Hall Problem With Bayesian Networks")
        network.add_states(d1, d2, d3)
        network.add_edge(d1, d3)
        network.add_edge(d2, d3)
        network.bake()
        return network

    def test_init(self):
        w = WumpusBayesianNetwork('Test')
        print(w)

    def test_get_node(self):
        network = self.get_monty_game_network()

        guest_node = network.get_node(node_name='guest')
        assert(guest_node is not None)

        guest_node = network.get_node(node_name='not there')
        assert(guest_node is None)


if __name__ == '__main__':
    unittest.main()
