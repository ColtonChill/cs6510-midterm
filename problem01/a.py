from utils import *
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,10))

commands = {}
path = []
# trajectory =[] #todo: ω = Δθ/Δt
circle_size = 500
time_step = 0.1
current_time = 0

# vehicle size
vehicle_len = 75
vehicle_width = 55

# vehicle motion
vel = 800 # cm/second
pos = (0,0)
ang_vel = 0

def save_command(p,omega=0,power_l=1,power_r=1):
    global current_time
    commands[current_time] = {'x':p[0],'y':p[1],'ω':omega,'power-l':power_l,'power-r':power_r}
    path.append(p)
    current_time+=time_step
    

#######################################################################################################################

###* 1) go up to the circle edge
# find the LCM so the robot arrives at a constant multiple of 0.1 time.
num_steps = ceil((circle_size/2)/(vel * time_step))
power = (circle_size/2)/(num_steps*vel*time_step)
# initial pos
save_command(pos,0,0,0)
# Do num_steps at 87% power to make it to perimeter
for i in range(0, num_steps):
    pos = step(pos, pi/2, power * vel *time_step)
    save_command(pos,0,power,power)

###* 2) turn into tangent position
arc_len = vehicle_width*pi/4
num_steps = ceil(arc_len/(vel*time_step))
power = (arc_len)/(num_steps*vel*time_step)
save_command(pos,(pi/4)/time_step,-power,power)

###* 3) drive at differential speed to close arc;
###! % = 1-w/r
# find the proportion of power the slower track needs to maintain
proportion = 1-vehicle_width/((circle_size+vehicle_width)/2)
# find average velocity of the vehicle body
center_vel = (1+proportion)/2 * vel
# calculate the overall power throttle to do this in an even integer of steps
num_steps = ceil((circle_size*pi)/(center_vel*time_step))
power = (circle_size*pi)/(num_steps*center_vel*time_step)
# plot the individual x,y points as a result of these power settings
for i in range(num_steps):
    pos = step(pos, pi + 2*pi/num_steps*(i+0.5) , power*center_vel*time_step)
    save_command(pos,2*pi/num_steps,power*proportion,power)


#################################################################################################

f = open("a-commands.txt",'w')
for time,command in commands.items():
    f.write(f"time:{round(time,2)} x:{round(command['x'],3)}, y:{round(command['y'],3)}, ω:{round(command['ω'],3)}, power-left:{format(command['power-l'],'.2%')}, power-right:{format(command['power-r'],'.2%')}\n")
f.close()

circle_boundary_out = plt.Circle((0,0), radius=circle_size/2+vehicle_width/2, color='r', linestyle='--', fill=False)
vehicle_center = plt.Circle((0,0), radius=circle_size/2, color='g', linestyle='--', fill=False)
circle_boundary_in = plt.Circle((0,0), radius=circle_size/2-vehicle_width/2, color='r', linestyle='--', fill=False)
ax.add_patch(circle_boundary_out)
ax.add_patch(vehicle_center)
ax.add_patch(circle_boundary_in)

# (number of sides, style, rotation)
plt.plot(*zip(*path),linestyle='--')
for time,command in commands.items():
    plt.plot(command['x'],command['y'], marker=(2, 0, command['ω']*180+180), color='black',markersize=20)

plt.show()