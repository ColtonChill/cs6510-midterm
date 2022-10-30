import random
import math
import matplotlib.pyplot as plt

class HybridAStar:
    def __init__(self, ox, oy, samplings, max_samplings):
        self.obstacles = [Node(x, y, None) for x, y in zip(ox, oy)]
        self.open = []
        self.closed = self.obstacles
        self.samples = samplings
        self.max_samples = max_samplings
        self.num_samples = 0

    def planning(self, sx, sy, gx, gy):
        """
        a) a set of random samples is generated

        b) each sample is connected to its nearest neighbor in a straight line
            (don't connect if there is a collision)

        c) create additional samples and connect to roadmap

        d) a path from start to goal is found by connecting start and goal via roadmap


        Now, how to change this to match the A* algorithm...?

        Also, sampling from skid-steer model...?
        """
        samples = self._sample(self.samples)

        vehicle = SkidSteer(33, 40, sx, sy, 0)

        start = Node(sx, sy, None)
        goal = Node(gx, gy, None)

        current = start
        self.open.append(samples)

        while len(self.open) > 0 and goal.parent is None:
            if self._can_connect(current, goal):
                goal.parent = current
                break

            if len(self.samples) == 0:
                if self.num_samples < self.max_samples:
                    self._samples(self.samples)
                else:
                    print(f"did not find goal within {max_samples} samples")
                    break

            # sorting function to find the closest sampling
            distance = lambda x: math.sqrt((x.pos[0] - current.pos[0]) ** 2 + (x.pos[1] - current.pos[1]) **2)

            for sample in samples:
                sample.G = current.G + distance(sample)

            F = lambda x: x.G + x.H

            self.samples.sort(key=F)

            idx = 0
            next_node = None
            while next_node is None or not self._can_connect(current, next_node):
                next_node = self.samples[idx]
                idx += 1

                if idx >= len(self.samples):
                    print("No connecting paths")
                    return None, None

            current = next_node


        fullPath = self._path_from_node(goal) 
        rx = [x.pos[0] for x in fullPath]
        ry = [x.pos[1] for x in fullPath]

        return rx, ry

        
    def _path_from_node(self, node):
        if node.parent is None:
            return []
        return [node] + self._path_from_node(node.parent)


    def _validate_sample(self, x, y):
        oSpaceX = [x.pos[0] for x in self.obstacles]
        oSpaceY = [x.pos[1] for y in self.obstacles]

        boolX = x > 0 and x < grid_size
        boolY = y > 0 and y < grid_size

        return boolX and boolY and not \
    (x in oSpaceX and y in oSpaceY)

    def _sample(self, howMany, goal):
        samples = []
        for i in range(howMany):
            randX = -1
            randY = -1
            while not self._validate_sample(randX, randY):
                randX = random.uniform(0, grid_size)
                randY = random.uniform(0, grid_size)

            new_sample = Node(randX, randY, None)
            new_sample.H = math.sqrt((goal.pos[0] - new_sample.pos[0]) ** 2 + (goal.pos[1] - new_sample.pos[1]) **2)
            samples.append(Node(randX, randY, None))

        self.num_samples += howMany

        return samples


    def _can_connect(self, node1, node2, vehicle):
        obsX = [node.pos[0] for node in self.obstacles]
        obsY = [node.pos[1] for node in self.obstacles]

        # find path between both nodes

        vehicle.pos = node1.pos
        path, _ = vehicle.move(node2.pos[0], node2.pos[1])

        for pos in path:
            if vehicle.collision(Node(pos[0], pos[1], None)):
                return False
        return True



class Node:
    def __init__(self, x, y, parent):
        self.parent = parent
        self.pos = x, y
        self.G = 0
        self.H = 0


class SkidSteer:
    def __init__(self, width, length, x, y, theta_init):
        self.width = width
        self.length = length
        self.pos = x, y
        self.theta = theta_init
        self.velocity = 5 # m/s (arbitrary)

    def move(self, x, y, resolution=0.1):
        targetTheta = math.atan2((y - self.y) / (x - self.x))
        omega = 2 * self.velocity / self.width
        dt = (targetTheta - self.theta) / omega
        commands = [(self.velocity, -self.velocity, dt)]
        # now that we're pointing the right direction, go full speed to x and y
        dist = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        dt = dist / velocity

        path = []
        for i in range(int(dt/resolution)):
            path.append((distance/int(dt/resolution) * math.cos(targetTheta), distance/int(dt/resolution) * math.sin(targetTheta)))
        commands.append((self.velocity, self.velocity, dt))
        return path, commands

    def collision(self, node):
        check_width = node.pos[0] <= self.pos[0] + 0.5 * self.width or node.pos[0] >= self.pos[0] - 0.5 * self.width
        check_height = node.pos[1] <= self.pos[1] + 0.5 * self.height or node.pos[1] >= self.pos[1] - 0.5 * self.height
        return check_width or check_height




def main():
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

    sx = -5.0
    sy = -5.0
    gx = 50.0
    gy = 50.0

    show_animation = True
    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    planner = HybridAStar(ox, oy, 10, 1000)
    rx, ry = planner.planning(sx, sy, gx, gy)

    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()


if __name__ == '__main__':
    main()
