from utils import *
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,10))

commands = {}
path = []
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

def save_command(p,omega=0,theta=0, power=0, plot_on=True):
    global current_time
    commands[current_time] = {'x':p[0],'y':p[1],'ω':omega,'theta':theta, 'power':power}
    if plot_on: path.append(p)
    current_time+=time_step
    

#######################################################################################################################

###* 1) go up to the circle edge
# find the LCM so the robot arrives at a constant multiple of 0.1 time.
num_steps = ceil((circle_size/2-92)/(vel * time_step))
power = (circle_size/2-92)/(num_steps*vel*time_step)
save_command(pos)
# Do num_steps at 87% power to make it to perimeter
for i in range(0, num_steps):
    pos = step(pos, pi/2, power * vel *time_step)
    save_command(pos,0,0,power)


###* 2) turn into tangent position with theta = 45
focus = (-75,158)
theta=(pi-acos((107-75)/75))
arc_len = theta*75
num_steps = ceil(arc_len/(vel*time_step))
power = arc_len/(num_steps*vel*time_step)

for i in range(1,num_steps+1):
    # pos = cos/sin + focus
    pos = (focus[0]+vehicle_len*cos(theta/num_steps*i), focus[1]+vehicle_len*sin(theta/num_steps*i))
    save_command(pos,0,theta/num_steps*i,power,plot_on=False)
# pretty print the arch path rather then the dt position steps
n=20
path.extend([(focus[0]+vehicle_len*cos(theta/n*j), focus[1]+vehicle_len*sin(theta/n*j)) for j in range(n+1)])

###* 3) drive at differential speed to close arc
theta_0 = acos(pos[0]/(circle_size/2))
print(theta_0)
arc_len = pi*circle_size
num_steps = ceil(arc_len/(vel*time_step))
power = arc_len/(num_steps*vel*time_step)
for i in range(1,num_steps+1):
    # pos = cos/sin
    pos = (circle_size/2*cos(i*2*pi/num_steps+theta_0), circle_size/2*sin(i*2*pi/num_steps+theta_0))
    save_command(pos,0,2*pi/num_steps*i,power,plot_on=False)

n=100
path.extend([(circle_size/2*cos(i*2*pi/n+theta_0), circle_size/2*sin(i*2*pi/n+theta_0)) for i in range(n+1)])

#################################################################################################

f = open("b-commands.txt",'w')
for time,command in commands.items():
    f.write(f"time:{round(time,2)} x:{round(command['x'],3)}, y:{round(command['y'],3)}, ω:{round(command['ω'],3)}, theta:{format(command['theta'],'.2%')}, power:{format(command['power'],'.2%')}\n")
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
    plt.plot(command['x'],command['y'], marker=(2, 0, command['ω']*180+90), color='black',markersize=20)
plt.show()
