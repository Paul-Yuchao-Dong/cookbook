from graph_cookbook import Edge, Graph, Node
graph = {
        1: [2, 3],
        2: [4, 5, 6],
        3: [4,6],
        4: [5,6],
        5: [6],
        6: []
    }

edges = []

for from_node, to_node_list in graph.items():
    for to_node in to_node_list:
        edges.append(Edge(Node(name=from_node), Node(name=to_node), 1))

graph = Graph(edges)
print(graph.nodes_by_level[1])
