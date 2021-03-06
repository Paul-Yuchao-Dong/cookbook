import q
class Node:
    "mixin class for A*"
    heuristic = lambda self, goal: 0 #must be monotonic
    @q
    def astar(self, goal):
        close_set, open_set, parent = set(), {self}, {self: None}
        f, g = {self: self.heuristic(goal)}, {self: 0} # initialization

        while open_set:
            current = min(open_set, key=f.get)
            # q(current)
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

if __name__ == '__main__':
    # This part is using only for self-checking and not necessary for
    # auto-testing
    from random import choice
    DIRS = {"N": -4, "S": 4, "E": 1, "W": -1}
    def check_solution(func, house):
        stephan = 16
        ghost = 1
        for step in range(30):
            direction = func(house[:], stephan, ghost)
            if direction in house[stephan - 1]:
                print('Stefan ran into a closed door. It was hurt.')
                return False
            if stephan == 1 and direction == "N":
                print('Stefan has escaped.')
                return True
            stephan += DIRS[direction]
            if ((direction == "W" and stephan % 4 == 0) or (direction == "E" and stephan % 4 == 1) or
                    (stephan < 1) or (stephan > 16)):
                print('Stefan has gone out into the darkness.')
                return False
            sx, sy = (stephan - 1) % 4, (stephan - 1) // 4
            ghost_dirs = [ch for ch in "NWES" if ch not in house[ghost - 1]]
            if ghost % 4 == 1 and "W" in ghost_dirs:
                ghost_dirs.remove("W")
            if not ghost % 4 and "E" in ghost_dirs:
                ghost_dirs.remove("E")
            if ghost <= 4 and "N" in ghost_dirs:
                ghost_dirs.remove("N")
            if ghost > 12 and "S" in ghost_dirs:
                ghost_dirs.remove("S")

            ghost_dir, ghost_dist = "", 1000
            for d in ghost_dirs:
                new_ghost = ghost + DIRS[d]
                gx, gy = (new_ghost - 1) % 4, (new_ghost - 1) // 4
                dist = (gx - sx) ** 2 + (gy - sy) ** 2
                if ghost_dist > dist:
                    ghost_dir, ghost_dist = d, dist
                elif ghost_dist == dist:
                    ghost_dir += d
            ghost_move = choice(ghost_dir)
            ghost += DIRS[ghost_move]
            if ghost == stephan:
                print('The ghost caught Stephan.')
                return False
        print("Too many moves.")
        return False

    assert check_solution(checkio,
                          ["", "S", "S", "",
                           "E", "NW", "NS", "",
                           "E", "WS", "NS", "",
                           "", "N", "N", ""]), "1st example"
    assert check_solution(checkio,
                          ["", "", "", "",
                           "E", "ESW", "ESW", "W",
                           "E", "ENW", "ENW", "W",
                           "", "", "", ""]), "2nd example"
