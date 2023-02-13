import networkx as nx

from wumpus.src.environment.Misc import Coords

class WumpusDiGraph(nx.DiGraph):
    """A Wumpus specific implementation of `DiGraph`
    """


    def __init__(self, incoming_graph_data=None, **attr):
        super().__init__(incoming_graph_data, **attr)
    

    def find_node(self, location: Coords):
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
