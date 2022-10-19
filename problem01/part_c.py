from math import sin, cos, pi, sqrt
import matplotlib.pyplot as plt

def step(v_l, v_r, pos0, theta0, dt=0.1):
    import time
    global robot_width, cur_time, path, opp_time
    start = time.time()

    x = pos0[0]- (v_r+v_l)/2*sin(theta0)*dt
    y = pos0[1]+ (v_r+v_l)/2*cos(theta0)*dt
    theta = theta0 + (v_r-v_l)/robot_width*dt

    opp_time.append(time.time()-start)
    path.append((x,y))
    cur_time = round(dt+cur_time,2)
    return (x,y),theta

circle_size = 500
circle_radius = circle_size/2
cur_time = 0.0

# robot size
robot_len = 75
robot_width = 55

# robot motion
vel = 800 # cm/second
pos0 = (0,circle_radius)
theta = 0
dt_s = [0.01, 0.1, 1]

##########################################################################################
for dt in dt_s:
    path = []
    actual_path = []
    opp_time = []
    # initial position
    pos, theta = step(v_l=0,v_r=0,pos0=pos0,theta0=pi/2,dt=0.1)
    # % = 1 - w/r
    ratio = (1-robot_width/(circle_radius+robot_width/2))
    v_r = (2*vel)/(ratio+1)
    v_l = v_r * ratio

    # drive around
    time = 10  # sec
    for i in range(int(time/dt)):
        pos, theta = step(v_l=v_l,v_r=v_r,pos0=pos,theta0=theta,dt=dt)

    ### Actual ###
    # Calculate the radius the vehicle with circle around (r = w/(1-%))
    r = robot_width/(1-(v_l/v_r if v_l/v_r < 1 else v_r/v_l )) - robot_width/2
    vel = (v_l+v_r)/2    # average vel
    arc_len = vel*dt
    phi = arc_len/r     # portion of the circle it can travel in this dt
    for i in range(int(time/dt)+1):
        pos_truth = (r*cos(phi*i+pi/2),r*sin(phi*i+pi/2))
        actual_path.append(pos_truth)

    error_dist = [(i*dt, sqrt((x1-x2)**2 + (y1-y2)**2)) for i,((x1,y1),(x2,y2)) in enumerate(zip(path, actual_path))]
    compute_time = [ (i*dt,sum(opp_time[:i])) for i in range(len(opp_time))]

    ##########################################################################################
    fig, (ax1,ax2,ax3) = plt.subplots(1,3, figsize=(20,6))

    # plot ideal tire boundaries
    circle_boundary_out = plt.Circle((0,0), radius=circle_radius+robot_width/2, color='r', linestyle='--', fill=False)
    robot_center = plt.Circle((0,0), radius=circle_radius, color='g', linestyle='--', fill=False)
    circle_boundary_in = plt.Circle((0,0), radius=circle_radius-robot_width/2, color='r', linestyle='--', fill=False)
    ax1.add_patch(circle_boundary_out)
    ax1.add_patch(robot_center)
    ax1.add_patch(circle_boundary_in)

    # Plot xy path
    ax1.plot(*zip(*path),linestyle='--', markersize=0, marker='o',label = "predicted")
    ax1.plot(*zip(*actual_path),linestyle='--', markersize=0, marker='o', color='green', label='actual')
    ax1.set_title(f"XY Plot for dt={dt}\n")
    ax1.set_xlabel("x pos (cm)")
    ax1.set_ylabel("y pos (cm)")
    ax1.legend()

    # plot error
    ax2.plot(*zip(*error_dist),linestyle='--',color='r')
    ax2.set_title(f"Error Plot for dt={dt}\n")
    ax2.set_xlabel("time (sec)")
    ax2.set_ylabel("Abs Pos Error (cm)")

    # computer time
    ax3.plot(*zip(*compute_time),linestyle='--')
    ax3.set_title(f"Computer Time for dt={dt}\n")
    ax3.set_xlabel("Time (sec)")
    ax3.set_ylabel("Computational Time (sec)")

    plt.savefig(f'plots/1c-dt={dt}.png')