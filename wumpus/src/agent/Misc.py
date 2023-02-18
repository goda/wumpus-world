import networkx as nx
import matplotlib.pyplot as plt

from wumpus.src.environment.Misc import Coords, WumpusNode

class WumpusDiGraph(nx.DiGraph):
    """A Wumpus specific implementation of `DiGraph`
    """


    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
    

    def find_node_location(self, location: Coords):
        """Finds a node in the graph for the given `location`

        Args:
            location (Coords): The coordinates of the desired location

        Returns:
            _type_: The actual node if it's in the graph, else `None`
        """
        for n in self.nodes:
            if n.location == location:
                return n
        
        return None
    
    def find_node(self, node: WumpusNode) -> WumpusNode:
        """Finds a node in the graph for the given `node`

        Args:
            node (WumpusNode): The node with coordinates and orientation

        Returns:
            _type_: The actual node if it's in the graph, else `None`
        """
        for n in self.nodes:
            if n == node:
                return n
        
        return None    
    
    def display_graph(self) -> None:
        G = self
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
