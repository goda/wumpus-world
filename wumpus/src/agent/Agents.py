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
    
    def __init__(self) -> None:
        super().__init__()
        
    def next_action(self, location: Coords, percept: Percept,
                    debug_action: Action = None) -> Action:
        # if agent has gold, it should be following its path
        # out using what it remembered from its graph
        
        
        allowed_actions = Action.get_all()
        allowed_actions.remove(Action.Climb)
        
        # only allow grab action from random pool of actions if glitter sensed
        # or agent doesn't have the gold
        if percept.glitter == False or self.has_gold:
            allowed_actions.remove(Action.Grab)
            
        if self.current_node.location == Coords(0,0) and self.has_gold:
            allowed_actions.append(Action.Climb)
        
        # need to add the move/action to the graph
        next_node = self.get_next_node(location, self.current_node,
                                            self.current_action)

        if next_node is not None:
            existing_node = self.graph.find_node(next_node)
            next_node = next_node if existing_node is None else existing_node
                
            self.update_graph(next_node, self.current_action)
            self.current_node = next_node

        self.percept = percept # not sure if we need this
        
        self.current_action = debug_action if debug_action is not None else self.random_action(allowed_actions)
        return self.current_action
          
    # assuming 
    def determine_shortest_path(self) -> dict:
        starting_node = WumpusNode(Coords(0,0), OrientationState.East)
        shortest_path = nx.shortest_path(self.graph, starting_node, self.current_node)
        for n in shortest_path:
            print('___ ', n)
        return shortest_path
    
    def determine_exit_path(self):
        shortest_path = self.determine_shortest_path()
        # print(shortest_path[-1])
        new_graph = WumpusDiGraph()
        prev_reverse_node = None
        prev_node = None
        print('dtermening')
        for i in range(len(shortest_path)-1, -1, -1):
            print(shortest_path[i])
            node: WumpusNode = shortest_path[i]
            reverse_node = WumpusNode(node.location,
                                      OrientationState.opposite_orientation(node.orientation_state))
            if prev_node is None:
                print('preve_node is none')
                new_graph.add_node(reverse_node)
                prev_node = node
                prev_reverse_node = reverse_node
            else:
                new_graph.add_node(reverse_node)                
                edge_object = self.graph.get_edge_data(node, prev_node)
                print(edge_object['object'])
                edge:WumpusEdge = edge_object['object']
                new_graph.add_edge(prev_reverse_node, 
                                   reverse_node,
                                   object = WumpusEdge(Action.opposite_turn(edge.action)))
                prev_reverse_node = reverse_node
                prev_node = node
        
        new_graph.display_graph()
    
    def get_next_node(self, 
                     new_location: Coords, 
                     current_node: WumpusNode, 
                     current_action: Action):
        orientation = Orientation(current_node.orientation_state)
        if current_action in [Action.TurnLeft, Action.TurnRight]:
            orientation.turn(current_action)
            return WumpusNode(current_node.location, orientation.state)
        elif current_action == Action.Forward and new_location != current_node.location:
            return WumpusNode(new_location, current_node.orientation_state)
        
        return None
            
                                
    def init_graph(self, location: Coords, orientation_state: OrientationState) -> None:
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