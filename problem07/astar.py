import math
import matplotlib.pyplot as plt

class AStar:
    def __init__(self, ox, oy, grid_size, robot_radius):
        self.obstacles = [Node(x, y, None, None, None) for x, y in zip(ox, oy)]
        self.closedls = self.obstacles
        self.openls = []

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
        goal = Node(gx, gy, None, None, None)
        start = Node(sx, sy, None, 0, goal)

        self.openls.append(start)

        next_node = None
        while len(self.openls) > 0 or goal.parent is None:
            idx = self.openls.index(min(self.openls, key=lambda x: x.H + x.G))
            next_node = self.openls.pop(idx)
            self.closedls.append(next_node)

            new_nodes = [
                Node(next_node.pos[0]+1, next_node.pos[1], next_node, next_node.G+1, goal),
                Node(next_node.pos[0]+1, next_node.pos[1]+1, next_node, next_node.G+1, goal),
                Node(next_node.pos[0], next_node.pos[1]+1, next_node, next_node.G+1, goal),
                Node(next_node.pos[0], next_node.pos[1]-1, next_node, next_node.G+1, goal),
                Node(next_node.pos[0]-1, next_node.pos[1]-1, next_node, next_node.G+1, goal),
                Node(next_node.pos[0]-1, next_node.pos[1], next_node, next_node.G+1, goal),
                Node(next_node.pos[0]+1, next_node.pos[1]-1, next_node, next_node.G+1, goal),
                Node(next_node.pos[0]-1, next_node.pos[1]+1, next_node, next_node.G+1, goal)
            ]

            for node in new_nodes:
                if goal.parent is not None:
                    break
                if node not in self.obstacles and node not in self.closedls:
                    if node in self.openls:
                        idx = self.openls.index(node)
                        if node.G < self.openls[idx].G:
                            self.openls[idx] = node
                    else:
                        self.openls.append(node)

                if node == goal:
                    print("Found goal")
                    goal.parent = node.parent


        fullPath = self._path_from_node(goal)
        rx = [x.pos[0] for x in fullPath]
        ry = [x.pos[1] for x in fullPath]

        return rx, ry
        

    def _path_from_node(self, node):
        if node.parent is None:
            return []
        return [node] + self._path_from_node(node.parent)


class Node:
    def __init__(self, x, y, parent, G, goal):
        self.parent = parent
        self.pos = (x, y)
        self.G = G
        if goal is not None:
            self.H = math.sqrt((goal.pos[0] - x)**2 + (goal.pos[1] - y)**2)

    def __repr__(self):
        return f"({self.pos[0]}, {self.pos[1]})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return other.pos[0] == self.pos[0] and other.pos[1] == self.pos[1]

def main():
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

    astar = AStar(ox, oy, grid_size, robot_radius)
    rx, ry = astar.planning(sx, sy, gx, gy)

    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()



if __name__ == '__main__':
    main()
