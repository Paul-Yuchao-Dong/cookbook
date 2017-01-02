import sys

class Vertex:
    def __init__(self, subproblem, id):
        self.id = id
        self.subproblem = subproblem
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def __repr__(self):
        return repr(self.id)

    def __eq__(self, other):
        try:
            return self.id == other.id
        except:
            return False

    def __hash__(self):
        return hash(repr(self))

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def __len__(self):
        return self.num_vertices

    def __getitem__(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def __contains__(self, vertex):
        return (vertex.id in self.vert_dict)

    def add_vertex(self, node):
        new_vertex = Vertex(node, self.num_vertices)
        self.num_vertices += 1
        self.vert_dict[node] = new_vertex
        return new_vertex

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return list(self.vert_dict.keys())

    def show(self):
        print('Graph data:')
        for v in self:
            for w in v.adjacent.keys():
                # import pudb; pudb.set_trace()
                print('( %s , %s, %3d)'  % ( v.id, w.id, v.adjacent[w]))

    def dijkstra(self, start):
        import heapq
        print('''Dijkstra's shortest path''')
        # Set the distance for the start node to zero
        start.distance = 0

        # Put tuple pair into the priority queue
        unvisited_queue = [(v.distance, i, v) for i, v in enumerate(self)]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue):
            # Pops a vertex with the smallest distance
            uv = heapq.heappop(unvisited_queue)
            current = uv[2]
            current.visited = True

            #for next in v.adjacent:
            for next in current.adjacent:
                # if visited, skip
                if next.visited:
                    continue
                new_dist = current.distance + current.adjacent[next]

                if new_dist < next.distance:
                    next.distance = new_dist
                    next.previous = current
                    print('updated : current = %s next = %s new_dist = %s' \
                            %(current.id, next.id, next.distance))
                else:
                    print('not updated : current = %s next = %s new_dist = %s' \
                            %(current.id, next.id, next.distance))

            # Rebuild heap
            # 1. Pop every item
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            # 2. Put all vertices not visited into the queue
            unvisited_queue = [(v.distance,i, v) for i, v in enumerate(self) if not v.visited]
            heapq.heapify(unvisited_queue)

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.id)
        shortest(v.previous, path)
    return

if __name__ == '__main__':
    from collections import namedtuple
    node = namedtuple('node', 'symbol')
    g = Graph()

    g.add_edge(node('a'), 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    g.show()
    g.dijkstra(g['a'])

    target = g['e']
    path = [target.id]
    shortest(target, path)
    print(('The shortest path : %s' %(path[::-1])))
