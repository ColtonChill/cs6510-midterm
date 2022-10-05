from math import cos
from math import sin
from math import radians as r
import numpy as np

a = [[cos(r(30)), -sin(r(30)), 0, 60*cos(r(30))],
     [sin(r(30)), cos(r(30)), 0, 60*sin(r(30))],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]

b = [[cos(r(45)), -sin(r(45)), 0, 40*cos(r(45))],
     [sin(r(45)), cos(r(45)), 0, 40*sin(r(45))],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]

c = [[cos(r(90)), -sin(r(90)), 0, 0],
     [sin(r(90)), cos(r(90)), 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]

d = [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 14],
     [0, 0, 0, 1]]

z = np.dot(a, b)
print(z)
z = np.dot(z, c)
print(z)
z = np.dot(z, d)
print(z)

a = 60 * sin(r(30))
b = 60 * cos(r(30))
print(a)
print(b)
c = 40 * sin(r(75))
d = 40 * cos(r(75))
print(c)
print(d)
print()
print("X: ", b+d)
print("Y: ", a+c)
print("Z: ", 14)