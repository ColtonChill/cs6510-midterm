from math import sqrt, sin, cos, acos, pi, ceil

def dist(p1, p2):
    return sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def mag(p):
    return dist((0,0),p)

def step(p,theta,mag):
    return p[0]+ mag*cos(theta),\
           p[1]+ mag*sin(theta)