from math import cos
from math import sin
from math import radians as r
import numpy as np

a = [[1, 0, 0, 60], 
     [0, cos(r(30)), -sin(r(30)), 0],
     [0, sin(r(30)), cos(r(30)), 0],
     [0, 0, 0, 1]]

b = [[1, 0, 0, 40], 
     [0, cos(r(45)), -sin(r(45)), 0],
     [0, sin(r(45)), cos(r(45)), 0],
     [0, 0, 0, 1]]

c = [[1, 0, 0, 0], 
     [0, cos(r(90)), -sin(r(90)), 0],
     [0, sin(r(90)), cos(r(90)), 0],
     [0, 0, 0, 1]]

z = np.dot(a, b)
print(z)
z = np.dot(z, c)
print(z)
