from pudb import set_trace
class Node(object):
    """
    this is the container for state
    """
    def __init__(self, name):
        self.name = name # need to adapt to implementations
        self.parent = set() #parent pointers
        self.children = set() #children pointers

    def __repr__(self):
        return "Node("+repr(self.name)+")" # need to adapt to implementations

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(self.__repr__()) # need to adapt to implementations


class Edge(object):
    """
    this contains a record of from to relationship between nodes,
    and the cost of travelling between states
    """
    def __init__(self, from_node, to_node, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

    def __repr__(self):
        return "Edge("+repr(self.from_node)+", "+repr(self.to_node)+")"

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __hash__(self):
        return hash(self.__repr__())

class Graph(object):
    """
    this manages the all the edges and nodes within the graph, define pathfinding algos here
    """
    def __init__(self, edges):
        from itertools import takewhile, count
        self.edges = edges
        self.nodes = set()
        for edge in self.edges:
            self.nodes.add(edge.from_node)
            self.nodes.add(edge.to_node)
            #these bits are puzzling
            self.locate(edge.from_node).children.add(self.locate(edge.to_node))
            self.locate(edge.to_node).parent.add(self.locate(edge.from_node))
        self.topo_sort()

        print(node.name for node in self.nodes_by_level.get(0, None))
    def __iter__(self):
        for node in self.nodes:
            yield node

    def locate(self, node):
        """
        return a pointer to the instance located in the nodes set
        """
        for n in self.nodes:
            if n==node:
                return n

    def topo_sort(self):
        from collections import defaultdict

        levels_by_node = {}
        nodes_by_level = defaultdict(set)

        def walk_depth_first(node):
            if node in levels_by_node:
                return levels_by_node[node]
            children = node.children
            level = 0 if not children else (1 + max(walk_depth_first(child) for child in children))
            levels_by_node[node] = level
            nodes_by_level[level].add(node)
            return level

        for node in self:
            walk_depth_first(node)

        self.levels_by_node = levels_by_node
        self.nodes_by_level = nodes_by_level
