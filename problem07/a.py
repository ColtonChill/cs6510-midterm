from otherPlanners.astar import AStarPlanner
from otherPlanners.bfs import BreadthFirstSearchPlanner
from otherPlanners.bidir_astar import BidirectionalAStarPlanner
from otherPlanners.djikstra import Dijkstra
from otherPlanners.rrtstar import RRTStar

import datetime

'''
import otherPlanners.astar as astar
import otherPlanners.bfs as bfs
import otherPlanners.bidir_astar as bidir
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
    grid_size = 2.0  # [m]
    robot_radius = 1.0  # [m]

    # set obstacle positions
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

    begin = datetime.datetime.now()
    pathing = planner(ox, oy, grid_size, robot_radius)
    rx, ry = pathing.planning(sx, sy, gx, gy)
    end = datetime.datetime.now()

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
    times["My A-Star"] = main(AStar)
    times["A-Star"] = main(AStarPlanner)
    times["BFS"] = main(BreadthFirstSearchPlanner)
    times["Bidirectional A-Star"] = main(BidirectionalAStarPlanner)
    times["Djikstra's"] = main(Dijkstra)
    #times["RRTStar"] = main(RRTStar)

    result =  "Planner|Path length|Calc. time (ms)|\n"
    result += "-|-|-\n"
    for r in times.keys():
        result += r + " | " + str(times[r][0]) + " | " + str(times[r][1]) + '\n'

    with open("results_A.md", "w") as handle:
        handle.write(result)

