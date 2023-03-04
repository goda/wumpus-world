import copy
import random
from typing import List

from matplotlib import pyplot as plt
from wumpus.src.agent.Misc import WumpusDiGraph
from wumpus.src.environment.Misc import Action, Coords, Orientation, OrientationState, Percept, WumpusEdge, WumpusNode
import networkx as nx
from pomegranate import Node, DiscreteDistribution, BayesianNetwork, ConditionalProbabilityTable


class Agent:
    """A class representing the Agent and its base implementation
    """

    def __init__(self) -> None:
        pass

    def next_action(percept: Percept) -> Action:
        pass


class NaiveAgent(Agent):
    """A Nāive agent that has no memory and randomly selects, an action
    without any percept information

    """

    def __init__(self) -> None:
        pass

    def next_action(self, percept: Percept, debug_action: Action = None) -> Action:
        return debug_action if debug_action is not None else Action(random.randint(int(Action.Forward), int(Action.Climb)))

    def random_action(self, allowed_actions: List[Action]) -> Action:
        int_actions = [int(a) for a in allowed_actions]
        return Action(random.choice(int_actions))


class BeelineAgent(NaiveAgent):
    """A Beeline agent that is able to 'remember' the actions/steps it took
    if it survives and gets to the gold location.

    """
    graph: WumpusDiGraph = None
    has_gold: bool = False
    percept: Percept = None
    current_node: WumpusNode = None
    current_action: Action = None
    exit_path_actions: List[Action] = None

    def __init__(self,
                 init_coords: Coords = Coords(0, 0),
                 init_orientation: OrientationState = OrientationState.East) -> None:
        super().__init__()
        self.has_gold = False
        self.init_graph(init_coords, init_orientation)

    def next_action(self, percept: Percept,
                    debug_action: Action = None) -> Action:
        # need to update the graph based on current_action
        next_node = self.get_next_node(self.current_node,
                                       self.current_action) if percept.bump == False else None

        if next_node is not None:
            existing_node = self.graph.find_node(next_node)
            next_node = next_node if existing_node is None else existing_node

            self.update_graph(next_node, self.current_action)
            self.current_node = next_node

        # if agent has gold, it should be following its path
        # out using what it remembered from its graph
        next_selected_action = None
        if self.current_action == Action.Grab:
            self.exit_path_actions = self.determine_exit_path()
        if self.current_node.location == Coords(0, 0) and self.has_gold:
            next_selected_action = Action.Climb
        elif self.has_gold:
            next_selected_action = self.exit_path_actions.pop(0)
        elif percept.glitter:
            self.has_gold = True
            next_selected_action = Action.Grab

        # if next_action is none - we are not on exit path yet, and no gold
        # in sight - random action ensuing
        if next_selected_action is None:
            allowed_actions = Action.get_all()
            allowed_actions.remove(Action.Climb)

            # only allow grab action from random pool of actions if glitter sensed
            # or agent doesn't have the gold
            if percept.glitter == False or self.has_gold:
                allowed_actions.remove(Action.Grab)

            self.percept = percept  # not sure if we need this
            next_selected_action = debug_action if debug_action is not None else self.random_action(
                allowed_actions)

        # return next_Action to the game
        self.current_action = next_selected_action
        return next_selected_action

    def determine_shortest_path(self) -> list:
        """Uses builtin shortest_path method to get the 
        shortest path from the origin, to the current node where 
        the agent is
        """
        starting_node = WumpusNode(Coords(0, 0), OrientationState.East)
        shortest_path = nx.shortest_path(
            self.graph, starting_node, self.current_node)
        return shortest_path

    def determine_exit_path(self) -> List[Action]:
        """Function to determine set of actions to exit game safely. 
        Let's retrace the steps back using the shortest path
        For now we will assume that we will follow the shortest path
        as found by the agent, without using x,y coordinates and connect
        physically adjacent squares unless the agent visited them directly
        """
        shortest_path = self.determine_shortest_path()
        first_node = None
        reverse_graph = WumpusDiGraph()
        prev_reverse_node = None
        prev_node = None
        for i in range(len(shortest_path)-1, -1, -1):
            node: WumpusNode = shortest_path[i]
            reverse_node = WumpusNode(node.location,
                                      OrientationState.opposite_orientation(node.orientation_state))
            if prev_node is None:
                first_node = reverse_node
                reverse_graph.add_node(reverse_node)
            else:
                reverse_graph.add_node(reverse_node)
                edge_object = self.graph.get_edge_data(node, prev_node)
                edge: WumpusEdge = edge_object['object']
                reverse_graph.add_edge(prev_reverse_node,
                                       reverse_node,
                                       object=WumpusEdge(Action.opposite_turn(edge.action)))

            prev_reverse_node = reverse_node
            prev_node = node

        exit_path_actions: List[Action] = []
        exit_path_actions = self.get_required_turn_actions_to_align(
            self.current_node.orientation_state,
            first_node.orientation_state
        )
        for e in reverse_graph.edges(data=True):
            edge: WumpusEdge = e[2]['object']
            exit_path_actions.append(edge.action)

        # last action is climb out
        exit_path_actions.append(Action.Climb)
        return exit_path_actions

    def get_next_node(self,
                      current_node: WumpusNode,
                      current_action: Action) -> WumpusNode:
        """Gets the next `WumpusNode` that the agent will be in,
        based on the `current_node` and `current_action`. This is to update 
        where the agent is physically in the game before it produces a next action

        Args:
            current_node (WumpusNode): The current node where the agent is before the 
            `current_action` is applied
            current_action (Action): The current action that was taken by the agent and 
            needs to be applied to the mental model of the agent's graph

        Returns:
            (WumpusNode): Where the agent is after the `current_action` is carried out
        """
        orientation = Orientation(current_node.orientation_state)
        if current_action in [Action.TurnLeft, Action.TurnRight]:
            orientation.turn(current_action)
            return WumpusNode(current_node.location, orientation.state)
        elif current_action == Action.Forward:
            new_location = self.forward(current_node)
            return WumpusNode(new_location, current_node.orientation_state)

        return None

    def forward(self, current_node: WumpusNode) -> Coords:
        """Assumes a forward move from `current_node` and that it wouldn't
        result in moving off the board, so caller would need to make sure that's true
        """
        x_delta = 0
        y_delta = 0
        if current_node.orientation_state == OrientationState.West:
            x_delta = -1
        elif current_node.orientation_state == OrientationState.East:
            x_delta = 1
        elif current_node.orientation_state == OrientationState.North:
            y_delta = 1
        elif current_node.orientation_state == OrientationState.South:
            y_delta = -1

        new_location = Coords(current_node.location.x + x_delta,
                              current_node.location.y + y_delta)
        return new_location

    def init_graph(self,
                   location: Coords,
                   orientation_state: OrientationState) -> None:
        self.graph = WumpusDiGraph()
        n = WumpusNode(location, orientation_state)
        self.graph.add_node(n)
        self.current_node = n

    def connect_adjacent_nodes(self, graph: WumpusDiGraph, from_node: WumpusNode,
                               to_node: WumpusNode):
        """Connects the `from_node` to the `to_node` provided that they're adjacent
        nodes (neighbouring) by figuring out the actions required to go `from_node` to
        `to_node`, last one being the forward. This method takes in a WumpusDiGraph object,
        along with two WumpusNode objects representing the starting and ending nodes of the path.

        This method builds up intermediate nodes to create a path from the from_node to the to_node.
        First, it determines the required turn actions to move forward from from_node to to_node. 
        Then, it iterates over those actions, adding new nodes and edges to the graph as necessary. 
        If the orientation of the last node in the path is not the same as the to_node, 
        additional actions are required to align it with the to_node orientation. 
        The method then adds these required nodes and edges to complete the rotation if necessary. 
        Finally, it returns the modified graph object.

        Args:
            graph (WumpusDiGraph): The graph object containing nodes and edges.
            from_node (WumpusNode): The starting node for the path.
            to_node (WumpusNode): The ending node for the path.
        """
        required_actions = self.get_required_turn_actions_to_move_forward(
            from_node, to_node)

        # build up the intermediate nodes
        o = Orientation(from_node.orientation_state)
        from_int_node: WumpusNode = from_node
        to_int_node: WumpusNode = from_node
        # go through all actions and add the required nodes/edges
        # to complete the path from_node to to_node
        for a in required_actions:
            o.turn(a)
            to_int_node = WumpusNode(from_node.location, o.state)
            graph.add_node(to_int_node)
            graph.add_edge(from_int_node,
                           to_int_node,
                           object=WumpusEdge(a))
            # move along the node pointers
            from_int_node = to_int_node

        # now check if orientation of last node isn't the same as the to_node
        # more actions required before we can connect to it finally
        required_actions_to_align = self.get_required_turn_actions_to_align(
            to_int_node.orientation_state,
            to_node.orientation_state)
        # go through all actions and add the required nodes/edges
        # to complete the rotation if necessary
        o = Orientation(to_int_node.orientation_state)
        from_int_node: WumpusNode = to_int_node
        to_int_node: WumpusNode = WumpusNode(to_node.location, o.state)
        graph.add_edge(from_int_node,
                       to_int_node,
                       object=WumpusEdge(Action.Forward))
        from_int_node = to_int_node
        for a in required_actions_to_align:
            o.turn(a)
            to_int_node = WumpusNode(to_node.location, o.state)
            graph.add_node(to_int_node)
            graph.add_edge(from_int_node,
                           to_int_node,
                           object=WumpusEdge(a))
            from_int_node = to_int_node

    def get_required_turn_actions_to_move_forward(self, from_node: WumpusNode,
                                                  to_node: WumpusNode):
        orientation_required = OrientationState.East
        if from_node.location.x == to_node.location.x:
            if from_node.location.y > to_node.location.y:
                orientation_required = OrientationState.South
            else:
                orientation_required = OrientationState.North
        else:
            if from_node.location.x > to_node.location.x:
                orientation_required = OrientationState.West
            else:
                orientation_required = OrientationState.East

        return self.get_required_turn_actions_to_align(from_node.orientation_state,
                                                       orientation_required)

    def get_required_turn_actions_to_align(self,
                                           from_orientation: OrientationState,
                                           orientation_required: OrientationState) -> List[Action]:
        required_turns = from_orientation.value - orientation_required.value
        if abs(required_turns) == 2:
            required_actions = [Action.TurnLeft, Action.TurnLeft]
        elif required_turns == -1:
            required_actions = [Action.TurnRight]
        elif required_turns == 1:
            required_actions = [Action.TurnLeft]
        elif required_turns == 3:
            required_actions = [Action.TurnRight]
        elif required_turns == -3:
            required_actions = [Action.TurnLeft]
        else:
            required_actions = []
        return required_actions

    def update_graph(self, next_node: WumpusNode, action: Action) -> None:
        """Updates the agent's view of the world and path traveled so far by 
        linking the `next_node` to the `current_node` since that was where the agent
        was last.

        Second part of this is to try and link the `next_node` to all the other nodes
        that are not current_node (location wise) that might be able to take us 
        to the `next_node`

        Args:
            next_node (WumpusNode): The next location of the agent
            action (Action): The action that will take the agent from `current_node`
            to `next_node`
        """
        neighbors = self.adjacent_cells(next_node.location)
        new_graph: WumpusDiGraph = copy.deepcopy(self.graph)
        for n in neighbors:
            node: WumpusNode
            for node in self.graph.nodes:
                if node.location == n and node != self.current_node:
                    # nodes_to_connect.append(node)
                    self.connect_adjacent_nodes(new_graph, node, next_node)

        self.graph = new_graph

        edge = WumpusEdge(action)
        self.graph.add_edge(self.current_node,
                            next_node,
                            object=edge)

    def adjacent_cells(self, coords: Coords) -> List[Coords]:
        """Return a list of neighboring cells to the given coordinates.

        Args:
            coords (Coords): The coordinates of the cell to find neighbors for.

        Returns:
            List[Coords]: A list of neighboring cells as Coords objects. A cell is
            considered a neighbor if it is located immediately adjacent to the
            given coordinates (in a 3x3 grid), but not if it is the same as the
            given coordinates. Diagonal neighbors are not included.

        Example:
            >>> adjacent_cells(Coords(1, 1))
            [Coords(0, 1), Coords(1, 0), Coords(1, 2), Coords(2, 1)]
        """
        def neighbors(x, y): return [Coords(x2, y2) for x2 in range(x-1, x+2)
                                     for y2 in range(y-1, y+2)
                                     if (
            (x != x2 or y != y2) and
            (x == x2 or y == y2)
        )]
        return neighbors(coords.x, coords.y)


class ProbAgent(BeelineAgent):
    """An agent that uses conditional probability when searching for the gold 
    based on the received percept at each action of the game. Its based on the 
    BeelineAgent as it will keep track of the visited nodes and plan optimal route 
    back
    """
    pits_breeze_graph: BayesianNetwork = None
    wumpus_stench_graph: BayesianNetwork = None
    grid_width: int = None
    grid_height: int = None

    def __init__(self, grid_width: int = 4,
                 grid_height: int = 4,
                 pit_location_prob: float = 0.2,
                 wumpus_stench_prb: float = 0.1):
        self.pits_breeze_graph = BayesianNetwork('Pits Breeze')
        self.wumpus_stench_graph = BayesianNetwork('Wumpus Stench')
        self.grid_height = grid_height
        self.grid_width = grid_width

    def prepare_prob_graph(self,
                           grid_width: int,
                           grid_height: int,
                           independent_prob: float,
                           indepndent_prob_node_label: str,
                           dependent_prob_node_label: str) -> BayesianNetwork:
        ##########################################
        ##########################################
        one_location_dist = [
            ['F', 'F', 1.],
            ['F', 'T', 0.],
            ['T', 'F', 0.],
            ['T', 'T', 1.]
        ]

        corner_location_dist = [
            ['F', 'F', 'F', 1.],
            ['F', 'F', 'T', 0.],
            ['F', 'T', 'F', 0.],
            ['F', 'T', 'T', 1.],
            ['T', 'F', 'T', 1.],
            ['T', 'F', 'F', 0.],
            ['T', 'T', 'F', 0.],
            ['T', 'T', 'T', 1.],
        ]

        edge_location_dist = [
            ['F', 'F', 'F', 'F', 1.],
            ['F', 'F', 'F', 'T', 0.],
            ['F', 'F', 'T', 'F', 0.],
            ['F', 'F', 'T', 'T', 1.],
            ['F', 'T', 'F', 'F', 0.],
            ['F', 'T', 'F', 'T', 1.],
            ['F', 'T', 'T', 'F', 0.],
            ['F', 'T', 'T', 'T', 1.],
            ['T', 'F', 'F', 'F', 0.],
            ['T', 'F', 'F', 'T', 1.],
            ['T', 'F', 'T', 'F', 0.],
            ['T', 'F', 'T', 'T', 1.],
            ['T', 'T', 'F', 'F', 0.],
            ['T', 'T', 'F', 'T', 1.],
            ['T', 'T', 'T', 'F', 0.],
            ['T', 'T', 'T', 'T', 1.],
        ]

        middle_location_dist = [
            ['T', 'T', 'T', 'T', 'T', 1.],
            ['T', 'T', 'T', 'T', 'F', 0.],
            ['T', 'T', 'T', 'F', 'T', 1.],
            ['T', 'T', 'T', 'F', 'F', 0.],
            ['T', 'T', 'F', 'T', 'T', 1.],
            ['T', 'T', 'F', 'T', 'F', 0.],
            ['T', 'T', 'F', 'F', 'T', 1.],
            ['T', 'T', 'F', 'F', 'F', 0.],
            ['T', 'F', 'T', 'T', 'T', 1.],
            ['T', 'F', 'T', 'T', 'F', 0.],
            ['T', 'F', 'T', 'F', 'T', 1.],
            ['T', 'F', 'T', 'F', 'F', 0.],
            ['T', 'F', 'F', 'T', 'T', 1.],
            ['T', 'F', 'F', 'T', 'F', 0.],
            ['T', 'F', 'F', 'F', 'T', 1.],
            ['T', 'F', 'F', 'F', 'F', 0.],
            ['F', 'T', 'T', 'T', 'T', 1.],
            ['F', 'T', 'T', 'T', 'F', 0.],
            ['F', 'T', 'T', 'F', 'T', 1.],
            ['F', 'T', 'T', 'F', 'F', 0.],
            ['F', 'T', 'F', 'T', 'T', 1.],
            ['F', 'T', 'F', 'T', 'F', 0.],
            ['F', 'T', 'F', 'F', 'T', 1.],
            ['F', 'T', 'F', 'F', 'F', 0.],
            ['F', 'F', 'T', 'T', 'T', 1.],
            ['F', 'F', 'T', 'T', 'F', 0.],
            ['F', 'F', 'T', 'F', 'T', 1.],
            ['F', 'F', 'T', 'F', 'F', 0.],
            ['F', 'F', 'F', 'T', 'T', 1.],
            ['F', 'F', 'F', 'T', 'F', 0.],
            ['F', 'F', 'F', 'F', 'T', 0.],
            ['F', 'F', 'F', 'F', 'F', 1]
        ]
        ##########################################
        ##########################################

        uniform_prob = independent_prob
        all_indp_loc = [Coords(x, y)
                        for x in range(0, grid_width)
                        for y in range(0, grid_height) if (x != 0 or y != 0)]
        indp_uniform_prob = {'T': uniform_prob, 'F': 1-uniform_prob}

        model: BayesianNetwork = BayesianNetwork("Pit/Breeze")
        indp_nodes = {}
        for indp_loc in all_indp_loc:
            indp_loc_dist = DiscreteDistribution(indp_uniform_prob)
            indp_node = Node(indp_loc_dist,
                             name=indepndent_prob_node_label+'@'+str(indp_loc))
            indp_nodes.update({indp_loc: indp_node})
            model.add_node(indp_node)

        # go through all locations, grabbing the physically adjacent locations
        # and use that as key look up to extract the distribution pit nodes
        # so that we can link them to the current location using the appropriate
        # conditional probability table
        all_dep_loc = [Coords(0, 0)] + all_indp_loc
        dep_loc = None
        for dep_loc in all_dep_loc:
            adjacent_indp_locs = self.adjacent_cells(dep_loc)
            # remove 0,0 since can't have pit/stench there
            try:
                adjacent_indp_locs.remove(Coords(0, 0))
            except:
                pass
            adj_indp_loc_nodes = []
            for adj_indp_loc in adjacent_indp_locs:
                adj_indp_loc_nodes.append(indp_nodes[adj_indp_loc])

            if len(adj_indp_loc_nodes) == 0:
                continue

            # get the right conditional probability table based on
            # where the dependent prob node is located at (x,y)
            cond_loc_dist = []
            if len(adjacent_indp_locs) == 1:
                cond_loc_dist = one_location_dist
            elif ((dep_loc.x == 0 and dep_loc.y == 1) or (dep_loc.x == 1 and dep_loc.y == 0)) or\
                (dep_loc.x == grid_width - 1 and (dep_loc.y == 0 or dep_loc.y == grid_height - 1)) \
                    or (dep_loc.x == 0 and (dep_loc.y == grid_height - 1 or dep_loc.y == 0)):
                cond_loc_dist = corner_location_dist
            elif (dep_loc.x == 0 and 0 < dep_loc.y < grid_height - 1) or (dep_loc.x == grid_width - 1 and 0 < dep_loc.y < grid_height - 1) \
                    or (dep_loc.y == 0 and 0 < dep_loc.x < grid_width - 1) or (dep_loc.y == grid_height - 1 and 0 < dep_loc.x < grid_width - 1):
                cond_loc_dist = edge_location_dist
            else:
                cond_loc_dist = middle_location_dist

            cond_prob_node = ConditionalProbabilityTable(
                cond_loc_dist,
                list(map(lambda n: n.distribution, adj_indp_loc_nodes))
            )

            dep_node = Node(
                cond_prob_node, name=dependent_prob_node_label+"@"+str(dep_loc))
            model.add_node(dep_node)
            # now add the edges between each of the adjacent pit probabilities
            # and the current location breeze conditional probability table node
            for a_indp_node in adj_indp_loc_nodes:
                model.add_edge(a_indp_node, dep_node)

        model.bake()
        return model

    def get_node_probabilities_for_evidence(self,
                                            model: BayesianNetwork,
                                            evidence: dict) -> dict[str, DiscreteDistribution]:
        """Method gets the node probability distribution given supplied `evidence`, for
        the provided `model`

        Args:
            model (BayesianNetwork): The model/network that we want to calculate the node
            probabilities for 
            evidence (dict): the evidence/facts that we know and for which we want to calculate 
            probability distributions of remaining nodes

        Returns:
            dict[str, DiscreteDistribution]: A `dict` mapping between node/state names and the 
            `DiscreteDistribution` based on the `evidence` and `model`
        """
        beliefs = model.predict_proba(evidence)
        probs = {}
        for state, belief in zip(model.states, beliefs):
            probs.update({state.name: belief})
        return probs

    def adjacent_cells(self, coords: Coords) -> List[Coords]:
        """Helper method that lets the agent figure out what locations, 
        are adjacent to the currently passed `coords` locations.

        Args:
            coords (Coords): The location for which we want to identify adjacent cells/
            locations.

        Returns:
            List[Coords]: A list of all the locations that are adjacent
        """
        def neighbors(x, y): return [Coords(x2, y2) for x2 in range(x-1, x+2)
                                     for y2 in range(y-1, y+2)
                                     if (-1 < x < self.grid_width and
                                         -1 < y < self.grid_height and
                                         (x != x2 or y != y2) and
                                         (x == x2 or y == y2) and
                                         (0 <= x2 < self.grid_width) and
                                         (0 <= y2 < self.grid_height))]
        return neighbors(coords.x, coords.y)
