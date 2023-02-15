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
            self.update_graph(next_node)
            self.current_node = next_node

        self.percept = percept # not sure if we need this
        
        self.current_action = debug_action if debug_action is not None else self.random_action(allowed_actions)
        return self.current_action
          
    
    def get_next_node(self, 
                     new_location: Coords, 
                     current_node: WumpusNode, 
                     current_action: Action):
        orientation = Orientation(current_node.orientation_state)
        if current_action in [Action.TurnLeft, Action.TurnRight]:
            orientation.turn(current_action)
            return WumpusNode(current_node.id + 1, current_node.location, orientation.state)
        elif current_action == Action.Forward and new_location != current_node.location:
            return WumpusNode(current_node.id + 1, new_location, current_node.orientation_state)
        
        return None
            
                                
    def init_graph(self, location: Coords, orientation_state: OrientationState) -> None:
        self.graph = WumpusDiGraph()
        
        n = WumpusNode(1, location,orientation_state)
        self.graph.add_node(n)
        self.current_node = n
        
    
    def update_graph(self, next_node: WumpusNode) -> None:
        edge = WumpusEdge(next_node.orientation_state)
        self.graph.add_edge(self.current_node,
                            next_node,
                            object = edge)

    def display_graph(self) -> None:
        G = self.graph
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()}
        )
        edge_labels = nx.get_edge_attributes(G,'object') # key is edge, pls check for your case
        formatted_edge_labels = {(elem[0],elem[1]):edge_labels[elem] for elem in edge_labels} # use this to modify the tuple keyed dict if it has > 2 elements, else ignore
        nx.draw_networkx_edge_labels(G,pos,edge_labels=formatted_edge_labels,font_color='red')
        plt.axis('off')
        plt.show()        