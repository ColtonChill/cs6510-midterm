from math import cos
from math import sin
from math import radians as r
import numpy as np

def dh(theta, d, a, alpha):
     return [[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
             [sin(theta), cos(theta) * cos(alpha),  -cos(theta) * sin(alpha), a * sin(theta)],
             [0, sin(alpha), cos(alpha), d],
             [0, 0, 0, 1]]

A = dh(r(30), 0, 60, 0)
B = dh(r(45), 0, 40, 0)
C = dh(r(90), 14, 0, 0)

Z = np.dot(np.dot(A, B), C)
print(Z)