class Node:
    "mixin class for A*"
    heuristic = lambda self, goal: 0 #must be monotonic
    def astar(self, goal):
        close_set, open_set, parent = set(), {self}, {self: None}
        f, g = {self: self.heuristic(goal)}, {self: 0} # initialization

        while open_set:
            current = min(open_set, key=f.get)
            open_set.remove(current)
            close_set.add(current)
            if current == goal:
                return self.path_from_parent(parent, current)
            for next_, way, dist in current.neighbors():
                if next_ not in close_set:
                    g_next = g[current] + dist
                    if next_ not in open_set or g_next < g[next_]:
                        open_set.add(next_)
                        parent[next_] = current, way
                        g[next_] = g_next
                        f[next_] = next_.heuristic(goal) + g_next


    def bfs(self, goal):
        from collections import deque
        todo, parent = deque([self]), {self:None}
        while todo:
            current = todo.popleft()
            if current == goal:
                return self.path_from_parent(parent, current)
            for next_, way, _ in current.neighbors():
                if next_ not in parent:
                    parent[next_] = current, way
                    todo.append(next_)

    def path_from_parent(self, parent, endpoint):
        path = []
        while endpoint is not self:
            endpoint, way = parent[endpoint]
            path.append(way)
        path.reverse()
        return path

def checkio(house, stephan, ghost):
    from collections import namedtuple
    walls = list(map(set, house))
    for w in walls[:4]: w.add("N")
    for w in walls[12:]: w.add("S")
    for w in walls[::4]: w.add("W")
    for w in walls[3::4]: w.add("E")
    class Room(namedtuple("_", "Stefan ghost"), Node):
        def neighbors(room):
            eS, eg = ({r + d: way for way, d in zip("EWSN", (1, -1, 4, -4))
                       if way not in walls[r - 1]} for r in room)
            if room.Stefan != room.ghost:
                if room.Stefan == 1: yield Room(StopIteration, ...), "N", 1
                for escape in eS:
                    def far(pursue):
                        coor = lambda x: divmod(x - 1, 4)
                        (Sx, Sy), (gx, gy) = coor(escape), coor(pursue)
                        return (Sx - gx)**2 + (Sy - gy)**2
                    yield Room(escape, min(eg, key=far)), eS[escape], 1
        def heuristic(self, goal):
            try:
                Sx, Sy = divmod(self.Stefan - 1, 4)
            except TypeError:
                Sx = Sy = 0
            return (Sx**2 + Sy**2)**(0.5)

    return Room(stephan, ghost).astar(Room(StopIteration, ...))[0]
