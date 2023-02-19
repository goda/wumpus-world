import random
from typing import List
from wumpus.src.agent.Misc import WumpusDiGraph
from wumpus.src.environment.Misc import Action, Coords, Orientation, OrientationState, Percept, WumpusEdge, WumpusNode
import networkx as nx
import matplotlib.pyplot as plt

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

    def next_action(self, percept: Percept) -> Action:
        return Action(random.randint(int(Action.Forward), int(Action.Climb)))
    
    
    def random_action(self, allowed_actions: List[Action]) -> Action:
        int_actions = [int(a) for a in allowed_actions]
        return Action(random.choice(int_actions))
    
class BeelineAgent(NaiveAgent):
    """A Beeline agent that is able to 'remember' the actions/steps it took
    if it survives and gets to the gold location.

    """
    graph: WumpusDiGraph = WumpusDiGraph()
    has_gold: bool = False
    percept: Percept
    current_node: WumpusNode
    current_action: Action = None
    exit_path_actions: List[Action] = None
    
    def __init__(self, 
                 init_coords: Coords = Coords(0,0),
                 init_orientation: OrientationState = OrientationState.East) -> None:
        super().__init__()
        self.has_gold = False
        self.init_graph(init_coords, init_orientation)
        
    def next_action(self, percept: Percept,
                    debug_action: Action = None) -> Action:
        # if agent has gold, it should be following its path
        # out using what it remembered from its graph
        next_action = None
        if self.current_action == Action.Grab:
            self.exit_path_actions = self.determine_exit_path()
        if self.has_gold:
            next_action = self.exit_path_actions.pop(0)
        elif percept.glitter:
            self.has_gold = True
            next_action = Action.Grab
        
        # if next_action is none - we are not on exit path yet, and no gold
        # in sight - random action ensuing
        if next_action is None:
            allowed_actions = Action.get_all()
            allowed_actions.remove(Action.Climb)
            
            # only allow grab action from random pool of actions if glitter sensed
            # or agent doesn't have the gold
            if percept.glitter == False or self.has_gold:
                allowed_actions.remove(Action.Grab)
                
            if self.current_node.location == Coords(0,0) and self.has_gold:
                allowed_actions.append(Action.Climb)
            
            
            self.percept = percept # not sure if we need this
            next_action = debug_action if debug_action is not None else self.random_action(allowed_actions)
        
        # need to update the graph based on current_action
        next_node = self.get_next_node(self.current_node,
                                       self.current_action) if percept.bump == False else None

        if next_node is not None:
            existing_node = self.graph.find_node(next_node)
            next_node = next_node if existing_node is None else existing_node
                
            self.update_graph(next_node, self.current_action)
            self.current_node = next_node
        
        # return next_Action to the game
        self.current_action = next_action
        return next_action
          
    def determine_shortest_path(self) -> list:
        """Uses builtin shortest_path method to get the 
        shortest path from the origin, to the current node where 
        the agent is
        """
        starting_node = WumpusNode(Coords(0,0), OrientationState.East)
        shortest_path = nx.shortest_path(self.graph, starting_node, self.current_node)
        return shortest_path
    
    def determine_exit_path(self) -> List[Action]:
        """Function to determine set of actions to exit game safely. 
        Let's retrace the steps back using the shortest path
        For now we will assume that we will follow the shortest path
        as found by the agent, without using x,y coordinates and connect
        physically adjacent squares unless the agent visited them directly
        """
        shortest_path = self.determine_shortest_path()
        reverse_graph = WumpusDiGraph()
        prev_reverse_node = None
        prev_node = None
        for i in range(len(shortest_path)-1, -1, -1):
            node: WumpusNode = shortest_path[i]
            reverse_node = WumpusNode(node.location,
                                      OrientationState.opposite_orientation(node.orientation_state))
            if prev_node is None:
                reverse_graph.add_node(reverse_node)
            else:
                reverse_graph.add_node(reverse_node)                
                edge_object = self.graph.get_edge_data(node, prev_node)
                edge:WumpusEdge = edge_object['object']
                reverse_graph.add_edge(prev_reverse_node, 
                                   reverse_node,
                                   object = WumpusEdge(Action.opposite_turn(edge.action)))
            
            prev_reverse_node = reverse_node
            prev_node = node
        
        exit_path_actions: List[Action] = []
        exit_path_actions.append(Action.TurnLeft)
        exit_path_actions.append(Action.TurnLeft)
        for e in reverse_graph.edges(data=True):
            edge: WumpusEdge = e[2]['object']
            exit_path_actions.append(edge.action)
        
        # last action is climb out
        exit_path_actions.append(Action.Climb)
        return exit_path_actions

    
    def get_next_node(self, 
                     current_node: WumpusNode, 
                     current_action: Action):
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
        elif current_node.orientation_state  == OrientationState.East:
            x_delta = 1
        elif current_node.orientation_state  == OrientationState.North:
            y_delta = 1
        elif current_node.orientation_state  == OrientationState.South:
            y_delta = -1
        
        return Coords(current_node.location.x + x_delta, 
                      current_node.location.y + y_delta)
    
    # GRAPH based functions
    def init_graph(self, 
                   location: Coords, 
                   orientation_state: OrientationState) -> None:
        self.graph = WumpusDiGraph()
        n = WumpusNode(location, orientation_state)
        self.graph.add_node(n)
        self.current_node = n
        
    def update_graph(self, next_node: WumpusNode, action: Action) -> None:
        # edge = WumpusEdge(next_node.orientation_state)
        edge = WumpusEdge(action)
        self.graph.add_edge(self.current_node,
                            next_node,
                            object = edge)