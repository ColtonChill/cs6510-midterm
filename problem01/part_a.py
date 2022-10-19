from math import sin, cos, acos, pi
from tkinter import Y
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10,10))

##########################################################################################33

class command:
    def __init__(self,time,left_vel,right_vel,x,y,omega) -> None:
        self.time =  time
        self.l = left_vel
        self.r = right_vel
        self.x = x
        self.y = y
        self.omega = omega

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.time}|{self.l}|{self.r}|{self.x}|{self.y}|{self.omega}'


def step(v_l, v_r, x0, y0, theta0, dt=0.1):
    global robot_width, cur_time, path, commands
    x = x0 - (v_r+v_l)/2*sin(theta0)*dt
    y = y0 + (v_r+v_l)/2*cos(theta0)*dt
    omega = (v_r-v_l)/robot_width
    theta = theta0 + omega*dt
    path.append((x,y))
    commands.append(command(cur_time,v_l,v_r,x,y,omega))
    cur_time = round(dt+cur_time,2)
    return (x,y),theta

circle_size = 500
circle_radius = 250
dt = 0.1
cur_time = 0.0

# robot size
robot_len = 75
robot_width = 55

# robot motion
vel = 800 # cm/second
pos = (0,0)
theta = 0
commands = []
path = []

#######################################################################################################################
"""
Game plan:
    1) Drive up to the circle
    2) Turn
    3) Drive around the circle
"""
# initial pos
pos, theta = step(v_l=0,v_r=0,x0=pos[0],y0=pos[1],theta0=theta)

### 1) Drive up to the circle
# first, cal the time
time = round((circle_size/2) / (vel*dt))
# go that long
for i in range(time):
    pos, theta = step(v_l=vel,v_r=vel,x0=pos[0],y0=pos[1],theta0=theta)

### 2) Turn
arc_len = robot_width/2*pi/2
power = arc_len/(vel*dt)
pos, theta = step(v_l=-vel*power,v_r=vel*power,x0=pos[0],y0=pos[1],theta0=theta)

### 3) Drive around the circle
# % = 1 - w/r
ratio = (1-robot_width/(250+robot_width/3))
v_r = (2*vel)/(ratio+1)
v_l = v_r * ratio
theta += (v_r-v_l)/robot_width*dt/2
while theta < 5/2*pi:
    pos, theta = step(v_l=v_l,v_r=v_r,x0=pos[0],y0=pos[1],theta0=theta)

#######################################################################################################################

circle_boundary_out = plt.Circle((0,0), radius=circle_size/2+robot_width/2, color='r', linestyle='--', fill=False)
robot_center = plt.Circle((0,0), radius=circle_size/2, color='g', linestyle='--', fill=False)
circle_boundary_in = plt.Circle((0,0), radius=circle_size/2-robot_width/2, color='r', linestyle='--', fill=False)
ax.add_patch(circle_boundary_out)
ax.add_patch(robot_center)
ax.add_patch(circle_boundary_in)

### Print Commands ###
f = open('commands/part_a_commands.md','w')
f.write('time(sec)|left_vel(m/s)|right_vel(m/s)|x-pos(cm)|y-pos(cm)|omega(rad/sec)\n')
f.write('-|-|-|-|-|-\n')
for c in commands:
    f.write(f'{str(c)}\n')
f.close()

# X,Y Pos Plot
plt.plot(*zip(*path),linestyle='--', marker='o')
plt.title("X,Y Position Plot (skid steer)\n")
plt.xlabel("X pos (cm)")
plt.ylabel("Y pos (cm)")
plt.savefig("plots/1a-xy.png")

# omega Pos Plot
fig, ax = plt.subplots(figsize=(10,10))
plt.plot(*zip(*[(c.time,c.omega) for c in commands]),linestyle='--', marker='o')
plt.title("Trajectory Plot (skid steer)\n")
plt.xlabel("Time_step (sec)")
plt.ylabel("Omega (rad/sec)")
plt.savefig("plots/1a-omega.png")
