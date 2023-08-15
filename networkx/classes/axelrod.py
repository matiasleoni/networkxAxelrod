import random

import numpy as np

import networkx as nx
from networkx.classes.graph import Graph

__all__ = ["Graph"]


# The Cultural_Network class is a "child" of the nx.Graph class (Parent) and inherits methods and attributes


class Cultural_Network(Graph):
    """
    The Cultural_Network class is a subclass of the nx.Graph class (Parent) and inherits methods and attributes.
    The class constructor, by default, has no parameters, but an object of the Parent class can be passed to it.

    Attributes:
        culturized (bool): Indicates whether the network has been cultured.

    Methods:
        __init__(self, graph=None):
            Initializes a Cultural_Network object.

        create_cultural_network(self, number_of_features, number_of_traits):
            Creates random cultures for each node in the network.

        common_features(self, pos1, pos2):
            Calculates the number of common cultural features between two nodes.

        list_cultures(self):
            Prints the list of cultures associated with each node in the cultural network.

        step(self, verbose=False):
            Performs a step of cultural interaction between two random neighboring nodes in the cultural network.

        network_cultures(self):
            Extracts the unique cultures present in the cultural network and counts their quantity.

        cultural_sizes_and_max(self):
            Calculates the sizes of cultures present in the cultural network and the maximum size among them.

        colorea_nodos(self):
            Colors the nodes in the network with a color index based on their culture.

        fixed_point(self):
            Checks if the graph is a cultural fixed point.

    Inherits from:
        nx.Graph
    """

    def __init__(self, graph=None):
        """
        If an argument is passed to the constructor it passes the Parent methods and attributes to it.
        Upon creating an object, it will not have culture initially
        """
        super().__init__(graph)
        self.culturized = False

    def create_cultural_network(self, number_of_features, number_of_traits):
        """
        Creates random cultures for each node in the network.
        Parameters:
        - number_of_features: int
            An integer representing the number of cultural features to be assigned to each node in the network.
        - number_of_traits: int
            An integer representing the maximum number of possible traits for each cultural feature.
        RETURN: The object itself.
        """
        self.number_of_features = number_of_features
        self.number_of_traits = number_of_traits
        # Generate a matrix of random cultural features for all nodes
        cultures = [
            [
                random.randint(1, self.number_of_traits)
                for feature in range(self.number_of_features)
            ]
            for node in range(len(self))
        ]

        # Assign cultural features to each node in the network
        for index, culture in zip(list(self.nodes), cultures):
            self.nodes[index]["culture"] = culture
        self.culturized = True
        return self

    def common_features(self, pos1, pos2):
        """
        Calculates the number of common cultural features between two nodes.
        Parameters:
        - pos1: An integer representing the position (index) of the first node in the network to be compared.
        - pos2: An integer representing the position (index) of the second node in the network to be compared.
        RETURN:
        - (integer) Returns the number of common cultural features between the nodes
        at positions 'pos1' and 'pos2' in the 'network'.
        """
        if self.culturized:
            com_array = np.array(self.nodes[pos1]["culture"]) == np.array(
                self.nodes[pos2]["culture"]
            )
            return sum(com_array)
        else:
            print(
                "You must add culture to the network. Use the 'create_cultural_network' method."
            )
            return None

    def list_cultures(self):
        """
        Prints the list of cultures associated with each node in the cultural network.
        """
        if self.culturized:
            for elem in list(self.nodes):
                print(elem, ": ", self.nodes[elem]["culture"])
        else:
            print(
                "You must add culture to the network. Use the 'create_cultural_network' method."
            )

    def step(self, verbose=False):
        """
        Performs a step of cultural interaction between two random neighboring nodes in the cultural network 'network'.
        RETURN: The object itself.
        """
        if self.culturized:
            # Choose a random node from the network
            agent_number = random.choice(list(self.nodes))
            # Get the neighbors of the chosen node
            neighbours = list(self.neighbors(agent_number))
            # Choose a random neighbor
            neighbour_number = random.choice(neighbours)
            # Get the cultures of the node and its neighbor
            agent_culture = self.nodes[agent_number]["culture"]
            neighbour_culture = self.nodes[neighbour_number]["culture"]
            # Find the cultural features in which the node and its neighbor differ
            disagreements = []
            for idx, disagree_bool in enumerate(
                np.array(agent_culture) != np.array(neighbour_culture)
            ):
                if disagree_bool:
                    disagreements.append(idx)
            # Calculate the probability of nodes exchanging cultural features
            probability = self.common_features(agent_number, neighbour_number) / len(
                agent_culture
            )
            # Perform the exchange of cultural features with the neighbor if the condition is met
            if len(disagreements) > 0 and np.random.binomial(
                1, p=probability, size=None
            ):
                feature_to_change_idx = random.choice(disagreements)
                if verbose:
                    print("agent_number: ", agent_number)
                    print("neighbour_number: ", neighbour_number)
                    print("feature_to_change_idx: ", feature_to_change_idx)
                self.nodes[neighbour_number]["culture"][
                    feature_to_change_idx
                ] = self.nodes[agent_number]["culture"][feature_to_change_idx]
        return self

    def network_cultures(self):
        """
        Extracts the unique cultures present in the cultural network 'network' and counts their quantity.
        RETURN: Tuple containing
            - A list of unique cultures present in the network.
            - An integer representing the quantity of unique cultures in the network.
        """
        if self.culturized:
            culture_set = set()
            for node_number in list(self.nodes):
                culture_set.add(tuple(self.nodes[node_number]["culture"]))
            culture_list = [list(elem) for elem in culture_set]
            cantidad_culturas = len(culture_set)
            return culture_list, cantidad_culturas
        else:
            return None

    def cultural_sizes_and_max(self):
        """
        Calculates the sizes of cultures present in the cultural network 'network' and the maximum size among them.
        RETURN: Tuple containing
            - A list containing the sizes of each culture present in the network.
            - An integer representing the maximum size among all cultures present in the network.
        """
        if self.culturized:
            culture_list = self.network_cultures()[0]
            culture_sizes = []
            for culture in culture_list:
                culture_size = 0
                for node_number in list(self.nodes):
                    if self.nodes[node_number]["culture"] == culture:
                        culture_size += 1
                culture_sizes.append(culture_size)
            max_culture_size = max(culture_sizes)
            return culture_sizes, max_culture_size
        else:
            return None

    def colorea_nodos(self):
        """
        Colors the nodes in the network with a color index based on their culture.
        RETURN: A list containing the color indices assigned to each node in the network based on their culture.
        """
        if self.culturized:
            color_list = []
            for node_number in list(self.nodes):
                culture = self.nodes[node_number]["culture"]
                # Find the color index corresponding to the node's culture
                index_color = self.network_cultures()[0].index(culture)
                # Assign the color index as the 'color' attribute of the node
                self.nodes[node_number]["color"] = index_color
                color_list.append(index_color)
            return color_list
        else:
            return None

    def fixed_point(self):
        """
        Checks if the graph is a cultural fixed point. A cultural fixed point is one where
        when each node is compared to a neighbor, it either has the same culture or does not share
        any cultural features. In a fixed point, the probability of evolving to another state
        through the "step" function is NULL.
        RETURN: bool. True if the graph is a cultural fixed point, False otherwise.
        """
        if self.culturized:
            # check_network will accumulate the number of nodes checked in the network
            check_network = 0
            for node_number in self:
                culture = self.nodes[node_number]["culture"]
                neighbours_numbers = list(self.neighbors(node_number))
                # check_node will accumulate the number of neighbors of a node that were checked
                check_node = 0
                for neighbour_number in neighbours_numbers:
                    neighbour_culture = self.nodes[neighbour_number]["culture"]
                    # check_node increments if the common features between the node and the neighbor are either 0 or all the features
                    check_node += self.common_features(
                        node_number, neighbour_number
                    ) in [0, self.number_of_features]
                # check_network increments if the accumulated number of all the neighbors of the node summed up in check_node
                check_network += check_node == len(list(self.neighbors(node_number)))
            # If all nodes are checked, then we are in a fixed point
            return check_network == len(self)
        else:
            return None
