from pickle import NEXT_BUFFER
from time import time
from turtle import circle, st
from utils import *
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,10))

commands = []
path = []
trajectory =[] #todo: ω = Δθ/Δt
circle_size = 500
time_step = 0.1

# vehicle size
vehicle_len = 75
vehicle_width = 55

# vehicle motion
vel = 800 # cm/second
pos = (0,0)
ang_vel = 0

def save_pos():
    path.append(pos)
    trajectory.append(ang_vel)

#######################################################################################################################

###* 1) go up to the circle edge
# find the LCM
num_steps = ceil((circle_size/2-vehicle_width/2)/(vel * time_step))
power = (circle_size/2-vehicle_width/2)/(num_steps*vel*time_step)
# initial pos
path.append(pos)
# Do num_steps at 87% power to make it to perimeter
for i in range(0, num_steps):
    pos = step(pos, pi/2, power * vel *time_step)
    path.append(pos)

###* 2) turn into tangent position

# throttle = dist(pos,(0,circle_size/2))/(vel*time_step)
# pos = step(pos,pi/2,vel*time_step*throttle)
# path.append(pos)

###* 3) drive at differential speed to close arc
# % = 1-w/r
proportion = 1-vehicle_width/(circle_size/2)
center_vel = (1+proportion)/2 * vel

num_steps = ceil(((circle_size-vehicle_width)*pi)/(center_vel*time_step))
print(num_steps)
power = ((circle_size-vehicle_width)*pi)/(num_steps*center_vel*time_step)
print(power)
for i in range(num_steps):
    pos = step(pos, pi + 2*pi/num_steps*(i+0.5) , power*center_vel*time_step)
    path.append(pos)


#################################################################################################33

circle_boundary_out = plt.Circle((0,0), radius=circle_size/2, color='r', linestyle='--', fill=False)
vehicle_center = plt.Circle((0,0), radius=circle_size/2-vehicle_width/2, color='g', linestyle='--', fill=False)
circle_boundary_in = plt.Circle((0,0), radius=circle_size/2-vehicle_width, color='r', linestyle='--', fill=False)
ax.add_patch(circle_boundary_out)
ax.add_patch(vehicle_center)
ax.add_patch(circle_boundary_in)

# (number of sides, style, rotation)
plt.plot(*zip(*path),linestyle='--', marker=(3, 0, 0*180), markersize=20)

plt.show()