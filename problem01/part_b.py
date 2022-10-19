from math import sin, cos, tan, atan, pi
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10,10))

##########################################################################################33

class command:
    def __init__(self,time,v_r,alpha,x,y,omega) -> None:
        self.time =  time
        self.v_r = v_r
        self.alpha = alpha
        self.x = x
        self.y = y
        self.omega = omega

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.time}|{self.v_r}|{self.alpha}|{self.x}|{self.y}|{self.omega}'


def step(v_r, alpha, x0, y0, theta0, dt=0.1):
    global robot_len, cur_time, path, commands
    x = x0 - v_r*sin(theta0)*dt
    y = y0 + v_r*cos(theta0)*dt
    omega = v_r/robot_len*tan(alpha)
    theta = theta0 + omega*dt
    # logging
    path.append((x,y))
    commands.append(command(cur_time,v_r,alpha,x,y,omega))
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
pos, theta = step(v_r=0,alpha=0,x0=pos[0],y0=pos[1],theta0=theta)

### 1) Drive up to the circle
# first, cal the time
time = round((circle_size/2) / (vel*dt))
# go that long
for i in range(time-1):
    pos, theta = step(v_r=vel,alpha=0,x0=pos[0],y0=pos[1],theta0=theta)


### 2) Turn
arc_len = robot_width/2*pi/2
power = arc_len/(vel*dt)
pos, theta = step(v_r=vel,alpha=pi/(3.085),x0=pos[0],y0=pos[1],theta0=theta)


### 3) Drive around the circle
alpha = atan(robot_len/circle_radius)
while theta < 5/2*pi:
    pos, theta = step(v_r=vel,alpha=alpha,x0=pos[0],y0=pos[1],theta0=theta)

#######################################################################################################################

circle_boundary_out = plt.Circle((0,0), radius=circle_size/2+robot_width/2, color='r', linestyle='--', fill=False)
robot_center = plt.Circle((0,0), radius=circle_size/2, color='g', linestyle='--', fill=False)
circle_boundary_in = plt.Circle((0,0), radius=circle_size/2-robot_width/2, color='r', linestyle='--', fill=False)
ax.add_patch(circle_boundary_out)
ax.add_patch(robot_center)
ax.add_patch(circle_boundary_in)


### Print Commands ###
f = open('commands/part_b_commands.md','w')
f.write('time(sec)|avg_vel(m/s)|alpha(rad)|x-pos(cm)|y-pos(cm)|omega(rad/sec)\n')
f.write('-|-|-|-|-|-\n')
for c in commands:
    f.write(f'{str(c)}\n')
f.close()


# (number of sides, style, rotation)
plt.plot(*zip(*path),linestyle='--', marker='o')
plt.title("Trajectory Plot (Ackermann)\n")
plt.xlabel("X pos (cm)")
plt.ylabel("Y pos (cm)")
plt.savefig("plots/1b-xy.png")


fig, ax = plt.subplots(figsize=(10,10))
plt.plot(*zip(*[(c.time,c.omega) for c in commands]),linestyle='--', marker='o')
plt.title("Trajectory Plot (Ackermann)\n")
plt.xlabel("Time_step (sec)")
plt.ylabel("Omega (rad/sec)")
plt.savefig("plots/1b-omega.png")