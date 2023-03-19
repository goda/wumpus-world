from typing import List
import networkx as nx
import matplotlib.pyplot as plt
from wumpus.src.environment.Misc import Action, Coords, OrientationState
from pomegranate import *
from pomegranate import Node


class WumpusNode:
    location: Coords
    orientation_state: OrientationState

    def __init__(self,
                 location: Coords,
                 orientation_state: OrientationState) -> None:
        self.location = location
        self.orientation_state = orientation_state

    def __str__(self) -> str:
        return "{""L:"" " + str(self.location) + ", ""O"": " + self.orientation_state.name + "}"

    def __eq__(self, __o: object) -> bool:
        if __o == None:
            return False
        return self.location == __o.location and self.orientation_state == __o.orientation_state

    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return str(self.__dict__.values())


class WumpusEdge:
    orientation_state: OrientationState
    action: Action

    def __init__(self, action: Action) -> None:
        self.action = action

    def __str__(self) -> str:
        # return self.orientation_state.name
        return self.action.name


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

    def get_locations(self) -> List[Coords]:
        """Simple helper to get a list of all locations in the graph
        in terms of `Coords`

        Returns:
            List[Coords]: list of all locations in the graph
        """
        return list(dict.fromkeys([n.location for n in self.nodes]))

    def display_graph(self) -> None:
        G = self
        pos = nx.spring_layout(G)
        plt.figure()
        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in G.nodes()}
        )
        # key is edge, pls check for your case
        edge_labels = nx.get_edge_attributes(G, 'object')
        # use this to modify the tuple keyed dict if it has > 2 elements, else ignore
        formatted_edge_labels = {
            (elem[0], elem[1]): edge_labels[elem] for elem in edge_labels}
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=formatted_edge_labels, font_color='red')
        plt.axis('off')
        plt.show()


class WumpusBayesianNetwork(BayesianNetwork):
    """Class to encapsulate `BayesianNetwork` and allow us to 
    build helper methods on top, including updating nework based on
    new evidence received, finding distribution of node by name etc.

    Args:
        BayesianNetwork (_type_): The parent class from `pomgegranate` package
    """

    def __init__(self, name: str):
        super().__init__(name)

    def get_node(self, node_name: str) -> Node:
        """Convenience method to allow us to find a node/state using 
        its name

        Args:
            node_name (str): The name of the node/state of interest

        Returns:
            Node: The node if found, else `None`
        """
        for node in self.states:
            if node.name == node_name:
                return node
        return None

    def get_node_probabilities_for_evidence(self,
                                            evidence: dict):
        """Method gets the node probability distribution given supplied `evidence`

        Args:
            evidence (dict): the evidence/facts that we know and for which we want to calculate 
            probability distributions of remaining nodes
        """
        node_probs = {}
        new_distributions = self.predict_proba(evidence)
        for state, new_distribution in zip(self.states, new_distributions):
            if type(state.distribution) == DiscreteDistribution:
                probs = new_distribution.parameters[0]
                node_probs.update({state.name: probs})
                # print(new_dist)
                # print('Updating distribution')
                # state.distribution = new_distribution
        return node_probs

    def plot(self):
        plt.figure(figsize=(14, 10))
        super().plot()
        plt.show()


class WumpusCoordsDict(dict[Coords, float]):
    """Helper class to allow for easier printing of dict

    Args:
        dict (dict[Coords, float]): `Coords` are the keys, and `float` are the values
    """

    def __str__(self) -> str:
        s = []
        for a, b in self.items():
            s.append("'{0}': {1}".format(str(a), str(b)))

        return '{' + ', '.join(s) + '}'
