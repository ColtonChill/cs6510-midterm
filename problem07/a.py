from otherPlanners.astar import AStarPlanner
from otherPlanners.bfs import BreadthFirstSearchPlanner
from otherPlanners.bidir_astar import BidirectionalAStarPlanner
from otherPlanners.djikstra import Dijkstra
from otherPlanners.rrtstar import RRTStar

import math
import matplotlib.pyplot as plt

class HybridAStar:
    def __init__(self, ox, oy, grid_size, robot_radius):
        self.open = []
        self.closed = []
        self.obstacles = [x for x in zip(ox, oy)]

    def planning(self, sx, sy, gx, gy):
        # 1. Add starting square to open list
        # 2. Repeat:
        #   a. Look for lowest cost F square on open list
        #   b. Switch that square to closed list
        #   c. For each spot adjacent to the current square:
        #       * ignore if not walkable or on closed list
        #       * Add to open list if not there. make current square parent of this square. Record f, g, h of the square
        #       * If already on open list, check if this path is better than current path, using G (lower is better). Change parent of square to current square, recalculate G and F
        #   d. Stop when:
        #       * Add target square to closed list (PATH FOUND)
        #       * Fail to find the target, and open list is empty (NO PATH FOUND)
        # 3. Save the path (recursively)
        start = Node(sx, sy, None, (gx, gy))

        final_node = self._recursive_planning(start, [], [], 0, (gx, gy))

        return self._path_from_node(final_node)

    def _recursive_planning(self, current, openls, closedls, G, goal):
        # this is the recursive part of the planning algorithm
        if current.pos == goal:
            return current
        new_nodes = [
            Node(current.pos[0]+1, current.pos[1], current, goal),
            Node(current.pos[0]+1, current.pos[1]+1, current, goal),
            Node(current.pos[0], current.pos[1]+1, current, goal),
            Node(current.pos[0], current.pos[1]-1, current, goal),
            Node(current.pos[0]-1, current.pos[1]-1, current, goal),
            Node(current.pos[0]-1, current.pos[1], current, goal),
            Node(current.pos[0]+1, current.pos[1]-1, current, goal),
            Node(current.pos[0]-1, current.pos[1]+1, current, goal)
        ]

        for node in new_nodes:
            if node.pos in self.obstacles or node in closedls:
                if node not in closedls:
                    closedls.append(node)
                new_nodes.remove(node)

        openls.append(new_nodes)
        F = lambda x: x.H + G

        openls.sort(key=F) # sort openls with smallest to largest F value

        next_node = openls.pop(0)
        closedls.append(next_node)

        return self._recursive_planning(next_node, openls, closedls, G+1, goal)

    def _path_from_node(self, node):
        if node.parent is None:
            return []
        return [node] + self._path_from_node(node.parent)


class Node:
    def __init__(self, x, y, parent, goal):
        self.parent = parent
        self.pos = (x, y)
        self.H = int(math.sqrt((goal[0] - x)**2 + (goal[1] - y)**2))


if __name__ == '__main__':

    print(__file__ + " start!!")

    # start and goal position
    sx = -5.0  # [m]
    sy = -5.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    grid_size = 2.0  # [m]
    robot_radius = 1.0  # [m]

    # set obstacle positions
    ox, oy = [], []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10.0)
    for i in range(-10, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(-10, 61):
        ox.append(-10.0)
        oy.append(i)
    for i in range(-10, 40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)

    show_animation = True
    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    dijkstra = Dijkstra(ox, oy, grid_size, robot_radius)
    rx, ry = dijkstra.planning(sx, sy, gx, gy)

    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()

