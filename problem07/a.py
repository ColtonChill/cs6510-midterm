from otherPlanners.astar import AStarPlanner
from otherPlanners.bfs import BreadthFirstSearchPlanner
from otherPlanners.bidir_astar import BidirectionalAStarPlanner
from otherPlanners.djikstra import Dijkstra
from otherPlanners.rrtstar import RRTStar
import datetime

'''
import otherPlanners.astar as astar
import otherPlanners.bfs as bfs import otherPlanners.bidir_astar as bidir
import otherPlanners.djikstra as dik
import otherPlanners.rrtstar as rrts '''
from astar import AStar

import matplotlib.pyplot as plt

def main(planner):
    # start and goal position
    sx = -5.0  # [m]
    sy = -5.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    grid_size = 1.0  # [m]
    robot_radius = 1.0  # [m]

    # set obstacle positions
    if planner != RRTStar:
        ox, oy = [], [] 
        for i in range(-10, 60):
            ox.append(i)
            oy.append(-10.0)
        for i in range(-10, 60):
            ox.append(60.0)
            oy.append(i)
        for i in range(-10, 61):
            ox.append(i)
            oy.append(60.0)
        for i in range(-10, 61):
            ox.append(-10.0)
            oy.append(i)
        for i in range(-10, 40):
            ox.append(20.0)
            oy.append(i)
        for i in range(0, 40):
            ox.append(40.0)
            oy.append(60.0 - i)

        pathing = planner(ox, oy, grid_size, robot_radius)
        begin = datetime.datetime.now()
        rx, ry = pathing.planning(sx, sy, gx, gy)
        end = datetime.datetime.now()

    else:
        ox, oy, size = [], [], []
        for i in range(-10, 60):
            ox.append(i)
            oy.append(-10.0)
            size.append(1)
        for i in range(-10, 60):
            ox.append(60.0)
            oy.append(i)
            size.append(1)
        for i in range(-10, 61):
            ox.append(i)
            oy.append(60.0)
            size.append(1)
        for i in range(-10, 61):
            ox.append(-10.0)
            oy.append(i)
            size.append(1)
        for i in range(-10, 40):
            ox.append(20.0)
            oy.append(i)
            size.append(1)
        for i in range(0, 40):
            ox.append(40.0)
            oy.append(60.0 - i)
            size.append(1)

        planner = RRTStar(
                start=[sx, sy],
                goal=[gx, gy],
                rand_area = [-10, 60],
                obstacle_list=[x for x in zip(ox, oy, size)],
                play_area = [-10, 60, -10, 60],
                expand_dis=1,
                robot_radius=robot_radius,
                max_iter=5000
                )
        begin = datetime.datetime.now()
        r = planner.planning(animation=False)
        end = datetime.datetime.now()
        rx = [x[0] for x in r]
        ry = [x[1] for x in r]



    return len(rx), (end - begin).microseconds/1000


if __name__ == '__main__':
    print(__file__ + " start!!")

    times = {
            "My A-Star": (None, None),
            "A-Star": (None, None),
            "BFS": (None, None),
            "Bidirectional A-Star": (None, None),
            "Djikstra's": (None, None),
            "RRTStar": (None, None)
            }
    astar = []
    for i in range(10):
        astar.append(main(AStar))
    times["My A-Star"] = (
            sum([x[0] for x in astar])/10.0,
            sum([x[1] for x in astar])/10.0
            )

    otherA = []
    for i in range(10):
        otherA.append(main(AStarPlanner))
    times["A-Star"] = (
            sum([x[0] for x in otherA])/10.0,
            sum([x[1] for x in otherA])/10.0
            )

    bfs = []
    for i in range(10):
        bfs.append(main(BreadthFirstSearchPlanner))
    times["BFS"] = (
            sum([x[0] for x in bfs])/10.0,
            sum([x[1] for x in bfs])/10.0
            )

    bi = []
    for i in range(10):
        bi.append(main(BidirectionalAStarPlanner))
    times["Bidirectional A-Star"] = (
            sum([x[0] for x in bi])/10.0,
            sum([x[1] for x in bi])/10.0
            )

    djikstra = []
    for i in range(10):
        djikstra.append(main(Dijkstra))
    times["Djikstra's"] = (
            sum([x[0] for x in djikstra])/10.0,
            sum([x[1] for x in djikstra])/10.0
            )

    rrt = []
    for i in range(10):
        rrt.append(main(RRTStar))
    times["RRTStar"] = (
            sum([x[0] for x in rrt])/10.0,
            sum([x[1] for x in rrt])/10.0
            )

    result =  "Planner|Path length|Calc. time (ms)|\n"
    result += "-|-|-\n"
    for r in times.keys():
        result += r + " | " + str(times[r][0]) + " | " + str(times[r][1]) + '\n'

    with open("results_A.md", "w") as handle:
        handle.write(result)

