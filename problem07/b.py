from astar import AStar
from hybrid_astar import HybridAStar

import datetime
import matplotlib.pyplot as plt

def main():
    ox, oy = [], []
    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)

    sx = 5.0
    sy = 5.0
    gx = 50.0
    gy = 50.0

    result = "Planner | Path Length | Time |\n- | - | -\n"

    show_animation = True
    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    times = []
    path_length = []
    for i in range(10):
        planner = HybridAStar(ox, oy, 60, 10, 5000)
        begin = datetime.datetime.now()
        rx, ry = planner.planning(sx, sy, gx, gy)
        end = datetime.datetime.now()
        path_length.append(len(rx))
        times.append((end - begin).microseconds)

    result += f"Hybrid | {sum(path_length)/10} | {sum(times)/10/1000}\n"

    if show_animation and rx is not None:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()

    if rx is None:
        print("Hybrid A-Star returned an error")
        
    
    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    times = []
    path_length = []
    for i in range(10):
        planner = HybridAStar(ox, oy, 60, 10, 5000)
        begin = datetime.datetime.now()
        rx, ry = planner.planning(sx, sy, gx, gy)
        end = datetime.datetime.now()
        path_length.append(len(rx))
        times.append((end-begin).microseconds)

    result += f"Normal | {sum(path_length)/10} | {sum(times)/10/1000}\n"

    if show_animation and rx is not None:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.01)
        plt.show()

    with open("results_B.md", "w") as handle:
        handle.write(result)


if __name__ == '__main__':
    main()

