import copy
import random
from typing import List

from matplotlib import pyplot as plt
from wumpus.src.agent.Misc import WumpusCoordsDict, WumpusDiGraph, WumpusEdge, WumpusNode, WumpusBayesianNetwork
from wumpus.src.environment.Misc import Action, Coords, Orientation, OrientationState, Percept
import networkx as nx
from pomegranate import Node, DiscreteDistribution, ConditionalProbabilityTable


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
                 init_orientation: OrientationState = OrientationState.East):
        """Initializes the agent by initializing the graph that will allow
        the agent to keep track of where it's been and how to get out fast
        after it finds the gold

        Args:
            init_coords (Coords, optional): _description_. Defaults to Coords(0, 0).
            init_orientation (OrientationState, optional): _description_. Defaults to OrientationState.East.
        """
        super().__init__()
        self.has_gold = False
        self.init_graph(init_coords, init_orientation)

    def next_action(self, percept: Percept, debug_action: Action = None) -> Action:
        """Method determines the next action based on the `percept` experienced from
        the environment. It first updates the agent's position in the game using the current
        node and current (previous) action, before determening whether it needs to pick
        next action or follow exit path if it has found the gold

        Args:
            percept (Percept): The percept passed from the environment
            debug_action (Action, optional): Used for debuggin in test mode. Defaults to None.

        Returns:
            Action: The next action to take
        """

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
                                                  to_node: WumpusNode) -> List[Action]:
        """Gets the required turn actions so that agent can move
        `from_node`, including its orientation, to the `to_node`. The orientation
        of the `to_node` isn't considered, just to get there is enough with the turns

        Args:
            from_node (WumpusNode): Current agent location, coords as `WumpusNode`
            to_node (WumpusNode): Destination agent location, coords as `WumpusNode`

        Returns:
            List[Action]: list of turn actions required 
        """
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
        """The required turns to ensure one can get `from_orientation` orientation, to 
        `orientation_required`

        Args:
            from_orientation (OrientationState): The starting orientation
            orientation_required (OrientationState): The final orientation

        Returns:
            List[Action]: The list of turn actions required to accomplish alignment
        """
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
    pits_breeze_graph: WumpusBayesianNetwork = None
    wumpus_stench_graph: WumpusBayesianNetwork = None
    grid_width: int = None
    grid_height: int = None
    # percepts/evidence tracking, e.g {'stench@(x: 0, y: 0)': 'F'}
    breeze_percepts: dict[str, str]
    stench_percepts: dict[str, str]
    # probabilities tracking
    pits_probs: WumpusCoordsDict
    wumpus_probs: WumpusCoordsDict
    combined_probs: WumpusCoordsDict
    wumpus_dead: bool = False
    #
    queue_turn_actions: List[Action] = []
    quit_and_exit: bool = False
    # to store unvisited locations that were adjacent along the path we've taken
    # so that we can go back and explore if we've hit a high risk node
    adjacent_unvisited_locs: List[Coords] = []
    # max probability we alllow of dying in a new location in deciding whether
    # to go there
    max_prob_dying_new_loc: float = 0.4
    # stores num of visits to each location by the agent
    visited_locs: WumpusCoordsDict
    max_number_visits_allowed: int = 4

    def __init__(self, grid_width: int = 4,
                 grid_height: int = 4,
                 init_coords: Coords = Coords(0, 0),
                 init_orientation: OrientationState = OrientationState.East,
                 pit_location_prob: float = 0.2,
                 max_prob_dying_new_loc: float = 0.4,
                 max_number_visits_allowed: int = 4):
        super().__init__(init_coords=init_coords, init_orientation=init_orientation)
        self.pits_breeze_graph = WumpusBayesianNetwork('Pits Breeze')
        self.wumpus_stench_graph = WumpusBayesianNetwork('Wumpus Stench')
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.pits_breeze_graph = self.prepare_prob_graph_pits_breeze(
            grid_width=grid_width,
            grid_height=grid_height,
            independent_prob=pit_location_prob,
            indepndent_prob_node_label="pit",
            dependent_prob_node_label="breeze"
        )
        self.wumpus_stench_graph = self.prepare_prob_graph_wumpus_stench(
            grid_width=grid_width,
            grid_height=grid_height
        )
        self.breeze_percepts = {}
        self.stench_percepts = {}
        self.pits_probs = WumpusCoordsDict()
        self.wumpus_probs = WumpusCoordsDict()
        self.combined_probs = WumpusCoordsDict()
        self.visited_locs = WumpusCoordsDict()
        self.pits_probs[Coords(0, 0)] = 0
        self.wumpus_probs[Coords(0, 0)] = 0

        self.max_prob_dying_new_loc = max_prob_dying_new_loc
        self.max_number_visits_allowed = max_number_visits_allowed

    def prepare_prob_graph_pits_breeze(self,
                                       grid_width: int,
                                       grid_height: int,
                                       independent_prob: float,
                                       indepndent_prob_node_label: str,
                                       dependent_prob_node_label: str) -> WumpusBayesianNetwork:
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

        model: WumpusBayesianNetwork = WumpusBayesianNetwork("Pit/Breeze")
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

    def prepare_prob_graph_wumpus_stench(self,
                                         grid_width: int,
                                         grid_height: int) -> WumpusBayesianNetwork:
        model: WumpusBayesianNetwork = WumpusBayesianNetwork("Wumpus/Stench")

        uniform_wumpus_prob = 1./(grid_height*grid_width-1)
        wumpus_possible_loc = [(Coords(x, y))
                               for x in range(0, grid_width)
                               for y in range(0, grid_height) if (x != 0 or y != 0)]
        stench_possible_loc = [(Coords(x, y))
                               for x in range(0, grid_width)
                               for y in range(0, grid_height)]
        wumpus_dict_prob = {
            str(wumpus_loc): uniform_wumpus_prob for wumpus_loc in wumpus_possible_loc}

        wumpus_node = Node(
            DiscreteDistribution(wumpus_dict_prob),
            name="wumpus"
        )
        model.add_node(wumpus_node)
        # go through all of the stench possible loc
        # and for each calculate the conditional probability table
        # for each possible wumpus location based on adjacency. Also
        # for the same location stench/wumpus add probability of 1.
        for s_loc in stench_possible_loc:
            cond_table_dist = []
            for wumpus_loc in wumpus_possible_loc:
                prob_value = 1. if s_loc.is_adjacent(wumpus_loc) else 0.
                prob_adjacent = [
                    [str(wumpus_loc), 'T', prob_value],
                    [str(wumpus_loc), 'F', 1 - prob_value]
                ]
                cond_table_dist.extend(prob_adjacent)
                # for same location as wumpus, stench is always true
                if s_loc in wumpus_possible_loc:
                    prob_same_loc = [
                        [str(s_loc), 'T', 1.],
                        [str(s_loc), 'F', 0.]
                    ]
                    cond_table_dist.extend(prob_same_loc)

            cond_prob_table = ConditionalProbabilityTable(
                cond_table_dist,
                [wumpus_node.distribution]
            )
            stench_node = Node(
                cond_prob_table,
                name="stench@"+str(s_loc)
            )
            model.add_node(stench_node)
            model.add_edge(wumpus_node, stench_node)

        model.bake()
        return model

    def update_probs(self):
        """Updates the probabilities for the wumpus and pit at each 
        of the possible location using `wumpus_prob` and `pits_probs`
        """
        pits_updated_probs = self.pits_breeze_graph.get_node_probabilities_for_evidence(
            evidence=self.breeze_percepts
        )
        for loc_str, prob_table in pits_updated_probs.items():
            loc = Coords.from_string(loc_str[4:])
            prob = float(prob_table['T'])
            self.pits_probs[loc] = prob
            # print('p', loc, prob)

        wumpus_updated_probs = self.wumpus_stench_graph.get_node_probabilities_for_evidence(
            evidence=self.stench_percepts
        )
        for loc_str, prob in wumpus_updated_probs['wumpus'].items():
            loc = Coords.from_string(loc_str)
            self.wumpus_probs[loc] = float(prob)
            # print('w', loc, prob)

        # update the combined probabilities so we have them handy for the whole
        # grid
        visited_locs = self.graph.get_locations()
        all_locs = [Coords(x, y)
                    for x in range(0, self.grid_width)
                    for y in range(0, self.grid_height)]
        self.calculate_combined_probs(
            pits_probs=self.pits_probs,
            wumpus_probs=self.wumpus_probs,
            combined_probs=self.combined_probs,
            visited_locs=visited_locs,
            locs_to_update=all_locs)

    def update_evidence(self, loc: Coords, percept: Percept):
        breeze_loc_label = "breeze@"+str(loc)
        self.breeze_percepts[breeze_loc_label] = 'T' if percept.breeze else 'F'

        stench_loc_label = "stench@"+str(loc)
        self.stench_percepts[stench_loc_label] = 'T' if percept.stench else 'F'

        # if scream then wumpus is dead!
        if percept.scream:
            wumpus_possible_loc = [(Coords(x, y))
                                   for x in range(0, self.grid_width)
                                   for y in range(0, self.grid_height) if (x != 0 or y != 0)]

            # update these once
            for l in wumpus_possible_loc:
                stench_loc_label = "stench@"+str(l)
                self.stench_percepts[stench_loc_label] = 'F'

            self.wumpus_dead = True

    def next_action(self, percept: Percept, debug_action: Action = None) -> Action:
        """Method determines the next action based on the `percept` experienced from
        the environment. It first updates the agent's position in the game using the current
        node and current (previous) action, before determening whether it needs to pick
        next action or follow exit path if it has found the gold

        Args:
            percept (Percept): The percept passed from the environment
            debug_action (Action, optional): Used for debuggin in test mode. Defaults to None.

        Returns:
            Action: The next action to take
        """

        # Step 1 - need to update the graph based on current_action
        next_node = self.get_next_node(self.current_node,
                                       self.current_action) if percept.bump == False else None

        if next_node is not None:
            existing_node = self.graph.find_node(next_node)
            next_node = next_node if existing_node is None else existing_node

            self.update_graph(next_node, self.current_action)
            # print
            if next_node.location != self.current_node.location:
                cur_loc = self.current_node.location
                print('Updating visit locations')
                if cur_loc in self.visited_locs.keys():
                    self.visited_locs[cur_loc] += 1
                else:
                    self.visited_locs[cur_loc] = 1

            if next_node.location in self.adjacent_unvisited_locs:
                print('Removing', next_node.location,
                      ' from adj unvisited loc')
                print('Before remove ', len(self.adjacent_unvisited_locs))
                for l in self.adjacent_unvisited_locs:
                    print(l)
                self.adjacent_unvisited_locs.remove(next_node.location)
                print('After remove ', len(self.adjacent_unvisited_locs))

            self.current_node = next_node

        # Step 2 - update state variables tracking where wumpus/pit
        # could be based on percepts experienced (only if not game over in sense
        # that we are leaving or have gold already)
        if self.quit_and_exit == False or self.has_gold:
            self.update_evidence(loc=self.current_node.location,
                                 percept=percept)
            self.update_probs()

        # Step 3 - determening action
        # if agent has gold, it should be following its path
        # out using what it remembered from its graph
        next_selected_action = None
        if self.current_action == Action.Grab:
            self.exit_path_actions = self.determine_exit_path()

        if self.current_node.location == Coords(0, 0) and self.has_gold:
            next_selected_action = Action.Climb
        elif self.has_gold or self.quit_and_exit:
            next_selected_action = self.exit_path_actions.pop(0)
        elif percept.glitter:
            self.has_gold = True
            next_selected_action = Action.Grab

        # if next_action is none - we are not on exit path yet, and no gold
        # in sight - random action ensuing
        if next_selected_action is None and self.queue_turn_actions == []:
            self.percept = percept  # not sure if we need this

            # Determening next action based on probs and percepts
            next_selected_action = debug_action if debug_action is not None \
                else self.determine_next_action(self.max_prob_dying_new_loc,
                                                self.max_number_visits_allowed)
            if next_selected_action == None and (self.queue_turn_actions == None
                                                 or self.queue_turn_actions == []):
                print('Need to exit Im scared')
                # need to exit!!!
                self.exit_path_actions = self.determine_exit_path()
                self.quit_and_exit = True
                next_selected_action = self.exit_path_actions.pop(0)
            elif self.queue_turn_actions != None and self.queue_turn_actions != []:
                print('Not exiting exploring still!')
                next_selected_action = self.queue_turn_actions.pop(0)
        elif self.queue_turn_actions != []:
            next_selected_action = self.queue_turn_actions.pop(0)
            print('Executing turn actions', next_selected_action)

        # return next_Action to the game
        self.current_action = next_selected_action
        return next_selected_action

    def determine_next_action(self,
                              max_prob_dying_new_loc: float,
                              max_number_visits_allowed: int) -> Action:
        """Method determines best next action to take for 
        Agent based on evidence and updated probabilities of 
        wumpus and stench surrounding it. 

        Returns:
            [Action]: The action to take next, returns 
        """
        print('Determening next action....', self.current_node)
        next_possible_locs = self.adjacent_cells(self.current_node.location)
        # get the probs of pit in all possible locs
        adjacent_combined_probs = {}
        adjacent_combined_probs = WumpusCoordsDict(
            filter(lambda pair: True if pair[0] in next_possible_locs else False,
                   self.combined_probs.items())
        )
        print(self.combined_probs)

        # min location with combined probability but also preferring new locations
        # over visited ones
        sorted_adjacent_combined_probs = sorted(adjacent_combined_probs.items(),
                                                key=lambda x: x[1], reverse=False)
        # dict_sorted_adjacent_combined_probs = dict(
        #     sorted_adjacent_combined_probs)
        print('((((()))))')
        for s in sorted_adjacent_combined_probs:
            print(s[0], s[1])
        print('((((()))))')

        # Step 2.
        # Let's calculate the possible probability of dying by exploring
        # new adjacent locations
        new_loc_combined_probs = [x for x in sorted_adjacent_combined_probs
                                  if self.graph.find_node_location(x[0]) == None]
        num_new_loc = len(new_loc_combined_probs)
        print('New loca', num_new_loc)
        # prob_dying_new_loc_move = 0.
        # # if we randomly picked one of the new locations, what is the chance
        # # of dying
        # for _, prob in new_loc_combined_probs:
        #     prob_dying_new_loc_move += 1./num_new_loc * (prob)
        # print('Cumulative Prob of dying,', prob_dying_new_loc_move)

        # lowest probability of dying by moving to a new location
        lowest_prob_dying_new_loc = 0
        if new_loc_combined_probs != []:
            lowest_prob_dying_new_loc = new_loc_combined_probs[0][1]
            print('lowest prob dying is...', lowest_prob_dying_new_loc, 'at',
                  new_loc_combined_probs[0][0])

        # we might need to put a cap on how many times we will visit same locations
        # maybe not more than 3-4 times? before giving up if probab dying new location
        # is also very high??

        # make sure that no other adjacent node to the safe path taken so far
        # has lower probability than lowest_prob_dying_new_loc, and if so then
        # we want to go back through the safe path rather than explore this higher
        # probability
        # AMENDMENT: only check for other adjacent node probabilities in other path areas
        # if the lowest_prob_dying_new_loc is above our threshold
        acceptable_prob_path_adj_loc_exists = False
        quit_and_exit = False
        if lowest_prob_dying_new_loc > max_prob_dying_new_loc:
            print('Going through other adjacent locations to see their probs')
            for adj_unvisited_loc in self.adjacent_unvisited_locs:
                print('Checking ADJACENT UNVISITED ', adj_unvisited_loc,
                      ' to see its probability', self.combined_probs[adj_unvisited_loc],
                      ' < ', lowest_prob_dying_new_loc, '< ', max_prob_dying_new_loc)
                if self.combined_probs[adj_unvisited_loc] < lowest_prob_dying_new_loc and \
                        self.combined_probs[adj_unvisited_loc] < max_prob_dying_new_loc:
                    # let's not explore to new location
                    acceptable_prob_path_adj_loc_exists = True
                    quit_and_exit = False
                    break
                if acceptable_prob_path_adj_loc_exists == False:
                    print('Could not find acceptable adj loc...')
                    quit_and_exit = True

        # Step 2b. if no adjacent location exists anywhere near the path
        # that has probability less than maximum threshold then we panic and exit
        if quit_and_exit:
            self.queue_turn_actions = []
            return None

        # Step 3. init next loc to lowest prob one for now. Try
        # and pick a new location with the minimum prob of dying
        # such that it's less than our threshold
        chosen_next_loc: Coords = None  # sorted_adjacent_combined_probs[0][0]
        for pot_loc, prob in sorted_adjacent_combined_probs:
            print('Checking next loc', pot_loc, 'with prob', prob)
            print('It is already visited ',
                  self.graph.find_node_location(pot_loc) != None)
            # if self.graph.find_node_location(pot_loc) and \
            #         lowest_prob_dying_new_loc < max_prob_dying_new_loc and \
            # acceptable_prob_path_adj_loc_exists == False:
            #     # we've visited this node before, so don't consider
            #     # taking it for now, as we don't fear dying in
            #     # new locations (< 0.5)
            #     continue
            # chosen_next_loc = pot_loc
            # break
            if (not self.graph.find_node_location(pot_loc)
                # or lowest_prob_dying_new_loc >= max_prob_dying_new_loc
                    or acceptable_prob_path_adj_loc_exists):
                chosen_next_loc = pot_loc
                break

        # if haven't chosen next_loc then need to pick from
        # adjacent based on frequency of visit
        if chosen_next_loc == None:
            print('No chosen new loc')
            sorted_visited_locs_list = sorted(self.visited_locs.items(),
                                              key=lambda x: x[1], reverse=False)
            sorted_visited_locs = dict(sorted_visited_locs_list)
            # if we have exceeded number of visits without eclipsing risk probability
            # let's just leave
            if len(sorted_visited_locs_list) > 0 \
                    and sorted_visited_locs_list[0][1] > max_number_visits_allowed:
                return None
            for loc, _ in sorted_visited_locs.items():
                if loc in next_possible_locs:
                    print('Going to prefer this visited loc', loc,
                          'with visit count ', sorted_visited_locs[loc])
                    chosen_next_loc = loc
                    break

        print('Chosen next loc', chosen_next_loc)

        # any unvisited adjacent nodes let's keep them for later
        print('Need to update list of adj unvisited locations')
        for pot_loc, _ in sorted_adjacent_combined_probs:
            print('Candidate ', pot_loc)
            if self.graph.find_node_location(pot_loc) == None and \
                    pot_loc != chosen_next_loc and pot_loc not in self.adjacent_unvisited_locs:
                print(pot_loc, ' is unvisited')
                self.adjacent_unvisited_locs.append(pot_loc)

        # Step 4. figure out how to record the actions required,
        # to get to the adjacent location? Maybe have a stack of actions
        # and if not empty in next_action we pop off from those (i.e. turn left,
        # turn left, forward) until we get to the chosen_next_loc?
        get_required_turn_actions = self.get_required_turn_actions_to_move_forward(
            from_node=self.current_node,
            to_node=WumpusNode(chosen_next_loc,
                               orientation_state=self.current_node.orientation_state)
        )
        # next actions consist of the required turns, and forward as last action
        self.queue_turn_actions = get_required_turn_actions + [Action.Forward]
        return None

    # NEED TO FINISH THIS - GET A CLASS VARIABLE TO HOLD THE COMBINED PROBABILITY
    # AND USE THAT
    def calculate_combined_probs(self,
                                 pits_probs: WumpusCoordsDict,
                                 wumpus_probs: WumpusCoordsDict,
                                 combined_probs: WumpusCoordsDict,
                                 visited_locs: List[Coords],
                                 locs_to_update: List[Coords]):
        for loc in locs_to_update:
            if loc in visited_locs or loc == Coords(0, 0):
                pit_prob = wumpus_prob = 0
            else:
                pit_prob = self.pits_probs[loc]
                wumpus_prob = self.wumpus_probs[loc]

            pits_probs[loc] = pit_prob
            wumpus_probs[loc] = wumpus_prob
            # combined probability of either wumpus/pits being T
            # P_c = 1 - (1-P_w)(1-P_p) = P_p + P_w - P_p*P_w
            combined_probs[loc] = wumpus_probs[loc] +\
                pits_probs[loc] - \
                wumpus_probs[loc]*pits_probs[loc]

        # Optional step?. if we have arrow, figure out threshold prob, to fire
        # it so that all in a given row/column could contain the wumpus and kill
        # or at least rule out probability of wumpus?? no scream
    # Helpers
    # def calculate

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
                                     if (-1 < x < self.grid_width and
                                         -1 < y < self.grid_height and
                                         (x != x2 or y != y2) and
                                         (x == x2 or y == y2) and
                                         (0 <= x2 < self.grid_width) and
                                         (0 <= y2 < self.grid_height))]
        return neighbors(coords.x, coords.y)
