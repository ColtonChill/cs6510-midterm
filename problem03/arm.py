from math import cos, exp, sin, dist, radians as r
import random
import copy
import time

D6 = 0.2

class Arm:
    def __init__(self, thetas, deltas):
        self.thetas = thetas
        self.deltas = deltas
        self.moves = []
        self.score = 0

    # This generates a random move
    def generateMove(self):
        # Pick a random key
        keys = list(self.thetas.keys()) + list(self.deltas.keys())
        key = random.choice(keys)
        # If this key coresponds to a joint then move -1, 0 or 1 degrees
        if self.thetas.get(key, '*') != '*':
            return (key, r(random.randint(-1, 1)))
        # Ohterwise this is a telescoping connection, so move -1cm to +c1m
        return (key, random.uniform(-0.01, 0.01))

    # This initialises the system with a set of random moves
    def generateMoves(self, count):
        random.seed(time.time())
        for i in range(count): 
            self.moves.append(self.generateMove())

    # Move the arm, and add the position
    def simulate(self):
        for i in range(len(self.moves)):
            key = self.moves[i][0]
            if self.thetas.get(key, '*') != '*':
                self.thetas[key][0] += self.moves[i][1]
                self.thetas[key][1] += abs(self.moves[i][1])
            else:
                if self.deltas[key][0] + self.moves[i][1] >= 0:
                    self.deltas[key][0] += self.moves[i][1]
                    self.deltas[key][1] += abs(self.moves[i][1])

    # Calculate the position of the endfactor
    def getPosition(self):
        t = self.thetas
        d = self.deltas
        x = (cos(t[1][0]) * cos(t[4][0]) * sin(t[5][0] * D6) - (sin(t[1][0]) * cos([5][0]) * D6) - (sin(t[1][0]) * d[3][0]))
        y = (sin(t[1][0]) * cos(t[4][0]) * sin(t[5][0] * D6) + (cos(t[1][0]) * cos([5][0]) * D6) + (cos(t[1][0]) * d[3][0]))
        z = d[2][0] - (sin(t[4][0]) * sin(t[5][0]) * D6)
        return (x, y, z)

    # Calculate the distance to some point
    def getDistance(self, pointA):
        pointB = self.getPosition()
        return dist(pointA, pointB)

    # Get an alternate solution
    def getAlt(self, mods):
        # Find alternatives
        alt = copy.deepcopy(self)
        for i in range(mods):
            altPos = random.randint(0, len(self.moves) - 1)
            alt.moves[altPos] = self.generateMove()
        return alt

    # Chose between two solutions
    def choose(self, alt, temp):
        dif = self.score - alt.score
        if dif < 0:
            p = 1/exp(-(dif/temp))
            r = random.random()
            if r < p:
                return True
            return False
        return True