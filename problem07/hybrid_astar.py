import random
import math
import matplotlib.pyplot as plt

class HybridAStar:
    def __init__(self, ox, oy, grid_size, samplings, max_samplings):
        self.obstacles = [Node(x, y, None) for x, y in zip(ox, oy)]
        self.open = []
        self.grid_size = grid_size
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

        vehicle = SkidSteer(3.3, 4.0, sx, sy, math.pi) # make scaling in 10s of centimeters

        start = Node(sx, sy, None)
        goal = Node(gx, gy, None)

        current = start

        G = lambda x: math.sqrt((x.pos[0] - current.pos[0]) ** 2 + (x.pos[1] - current.pos[1]) **2)
        H = lambda x: math.sqrt((goal.pos[0] - x.pos[0]) ** 2 + (goal.pos[1] - x.pos[1]) **2)

        start.G = G(start)
        start.H = H(start)

        samples = self._sample(self.samples, goal)

        self.open.append(samples)

        while len(self.open) > 0 and goal.parent is None:
            if self._can_connect(current, goal, vehicle):
                goal.parent = current
                break

            if len(samples) == 0:
                if self.num_samples < self.max_samples:
                    self._sample(self.samples)
                else:
                    print(f"did not find goal within {max_samples} samples")
                    break

            for sample in samples:
                sample.G = current.G + G(sample)

            F = lambda x: x.G + x.H

            samples.sort(key=F)

            next_node = None
            while next_node is None or not self._can_connect(current, next_node, vehicle):
                next_node = samples[0]
                del samples[0]

                if len(samples) == 0:
                    if self.num_samples < self.max_samples:
                        samples = self._sample(self.samples, goal)
                    else:
                        print("reached max iterations, exiting")
                        return None, None

            next_node.parent = current

            current = next_node

        print("found goal")
        fullPath = self._path_from_node(goal)
        fullPath.reverse()
        rx = [x.pos[0] for x in fullPath]
        ry = [x.pos[1] for x in fullPath]

        return rx, ry

        
    def _path_from_node(self, node):
        if node.parent is None:
            return [node]
        return [node] + self._path_from_node(node.parent)


    def _validate_sample(self, x, y):
        oSpaceX = [x.pos[0] for x in self.obstacles]
        oSpaceY = [x.pos[1] for x in self.obstacles]

        boolX = x > 0 and x < self.grid_size
        boolY = y > 0 and y < self.grid_size

        return boolX and boolY and not \
    (x in oSpaceX and y in oSpaceY)

    def _sample(self, howMany, goal):
        samples = []
        for i in range(howMany):
            randX = -1
            randY = -1
            while not self._validate_sample(randX, randY):
                randX = random.uniform(0, self.grid_size)
                randY = random.uniform(0, self.grid_size)

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
        path, angle = vehicle.make_path(node2.pos[0], node2.pos[1])

        return vehicle.move(path, angle, self.obstacles)



class Node:
    def __init__(self, x, y, parent):
        self.parent = parent
        self.pos = x, y
        self.G = 0
        self.H = 0

    def __repr__(self):
        return f"({self.pos[0]}, {self.pos[1]})"

    def __str__(self):
        return self.__repr__()


class SkidSteer:
    def __init__(self, width, length, x, y, theta_init):
        self.width = width
        self.length = length
        self.pos = x, y
        self.theta = theta_init
        self.velocity = 5 # m/s (arbitrary)

    def make_path(self, x, y, resolution=0.1):
        targetTheta = math.atan2((y - self.pos[1]), (x - self.pos[0]))
        omega = 2 * self.velocity / self.width
        dt = (targetTheta - self.theta) / omega

        dist = math.sqrt((x - self.pos[0]) ** 2 + (y - self.pos[1]) ** 2)
        dt = dist / self.velocity


        path = []
        for i in range(int(dt/resolution)):
            path.append((dist/int(dt/resolution) * math.cos(targetTheta) * i, dist/int(dt/resolution) * math.sin(targetTheta) * i))
        return path, targetTheta

    def move(self, path, theta, obstacles):
        tempPos = self.pos
        tempTheta = self.theta

        self.theta = theta

        for p in path:
            self.pos = (tempPos[0] + p[0], tempPos[1] + p[1])
            
            for o in obstacles:
                if self.collision(o):
                    self.pos = tempPos
                    self.theta = tempTheta
                    return False

        return True

    @property
    def coordinates(self):
        # grabbed from https://stackoverflow.com/questions/41898990/find-corners-of-a-rotated-rectangle-given-its-center-point-and-rotation
        tr_x = self.pos[0] + ((self.width /2) * math.cos(self.theta)) - ((self.length / 2) * math.sin(self.theta))
        tr_y = self.pos[1] + ((self.width /2) * math.sin(self.theta)) + ((self.length / 2) * math.cos(self.theta))

        tl_x = self.pos[0] - ((self.width /2) * math.cos(self.theta)) - ((self.length / 2) * math.sin(self.theta))
        tl_y = self.pos[1] - ((self.width /2) * math.sin(self.theta)) + ((self.length / 2) * math.cos(self.theta))

        bl_x = self.pos[0] - ((self.width /2) * math.cos(self.theta)) + ((self.length / 2) * math.sin(self.theta))
        bl_y = self.pos[1] - ((self.width /2) * math.sin(self.theta)) - ((self.length / 2) * math.cos(self.theta))

        br_x = self.pos[0] + ((self.width /2) * math.cos(self.theta)) + ((self.length / 2) * math.sin(self.theta))
        br_y = self.pos[1] + ((self.width /2) * math.sin(self.theta)) - ((self.length / 2) * math.cos(self.theta))

        return ((tr_x, tr_y), (tl_x, tl_y), (bl_x, bl_y), (br_x, br_y))


    def collision(self, node):
        # grabbed from https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
        tr, tl, bl, br = self.coordinates

        distance = lambda x1, x2: math.sqrt((x2[0] - x1[0]) ** 2 + (x2[1] - x1[1]) ** 2)

        # area of rectangle
        v_area = distance(bl, br) * distance(bl, tl)

        # areas for each triangle; if the sum is greater than size of rectangle, P(x, y) is outside the rectangle
        apd = abs((tr[0] * (node.pos[1] - br[1]) + node.pos[0] * (br[1] - tr[1]) + br[0] * (tr[1] - node.pos[1]))/2)
        dpc = abs((br[0] * (node.pos[1] - bl[1]) + node.pos[0] * (bl[1] - br[1]) + bl[0] * (br[1] - node.pos[1]))/2)
        cpb = abs((bl[0] * (node.pos[1] - tl[1]) + node.pos[0] * (tl[1] - bl[1]) + tl[0] * (bl[1] - node.pos[1]))/2)
        pba = abs((node.pos[0] * (tl[1] - tr[1]) + tl[0] * (tr[1] - node.pos[1]) + tr[0] * (node.pos[1] - tl[1]))/2)

        return sum([apd, dpc, cpb, pba]) <= v_area



        
        '''
        intercept_lmin = (self.pos[1] - self.width / (2 * math.cos(self.theta))) - math.tan(self.theta) * self.pos[0]                   # y-intercept for min lengthwise functions
        intercept_lmax = (self.pos[1] - self.width / (2 * math.cos(self.theta))) - math.tan(self.theta) * self.pos[0]                   # y-intercept for max lengthwise functions
        intercept_wmin = (self.pos[1] - self.length / (2 * math.cos(self.theta))) - math.tan(self.theta) * self.pos[0]                   # y-intercept for min widthwise functions
        intercept_wmax = (self.pos[1] - self.length / (2 * math.cos(self.theta))) - math.tan(self.theta) * self.pos[0]                   # y-intercept for max widthwise functions

        if self.theta == math.pi/2 or self.theta == -math.pi/2:
            blmin = lambda x: self.pos[1] - 1/2 * self.length
            blmax = lambda x: self.pos[1] + 1/2 * self.length
            bwmin = lambda x: self.pos[0] - 1/2 * self.width
            bwmax = lambda x: self.pos[0] + 1/2 * self.width

        else:
            blmin = lambda x: math.tan(self.theta) * x + intercept_lmin     # function for lower bound lengthwise
            blmax = lambda x: math.tan(self.theta) * x + intercept_lmax     # function for upper bound lengthwise
            bwmin = lambda x: math.tan(self.theta) * x + intercept_wmin     # function for lower bound widthwise
            bwmax = lambda x: math.tan(self.theta) * x + intercept_wmax     # function for upper bound widthwise

        check_lengthwise = blmin(node.pos[0]) < node.pos[0] < blmax(node.pos[0])
        check_widthwise = bwmin(node.pos[0]) < node.pos[1] < bwmax(node.pos[0])

        return self.pos[0] - 1/2 * self.length < node.pos[0] < self.pos[0] + 1/2 * self.length and self.pos[1] - 1/2 * self.width < node.pos[1] < self.pos[1] + 1/2 * self.width
        '''
    #return check_widthwise and check_lengthwise



def main():
    ox, oy = [], []
    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)

    sx = 5.0
    sy = 5.0
    gx = 50.0
    gy = 50.0

    show_animation = True
    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    planner = HybridAStar(ox, oy, 60, 10, 5000)
    rx, ry = planner.planning(sx, sy, gx, gy)

    if show_animation and rx is not None:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()

    if rx is None:
        print("Hybrid A-Star returned an error")



if __name__ == '__main__':
    main()
