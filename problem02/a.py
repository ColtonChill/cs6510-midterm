from math import cos
from math import sin
import numpy as np

a = [[1, 0, 0, 60], 
     [0, cos(30), -sin(30), 0],
     [0, sin(30), cos(30), 0],
     [0, 0, 0, 1]]

b = [[1, 0, 0, 40], 
     [0, cos(45), -sin(45), 0],
     [0, sin(45), cos(45), 0],
     [0, 0, 0, 1]]

c = [[1, 0, 0, 0], 
     [0, cos(90), -sin(90), 0],
     [0, sin(90), cos(90), 0],
     [0, 0, 0, 1]]

z = np.dot(a, b)
print(z)
