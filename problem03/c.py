from doctest import script_from_examples
from math import radians as r, degrees as d
import sys
from arm import Arm
import copy

# Main variables
MOVE_COUNT = 500
INIT_TEMP = 10000000
COOLING_RATE = 0.999
STOP_TEMP = 0.001
MODS = 30

DESTINATION = (1.2, 0.8, 0.5)

# Set up the DH parameters. The secon part of each touple is to track change
thetas = {
    1: [r(-90), 0],
    4: [r(-90), 0],
    5: [r(90), 0],
    6: [r(40), 0]
}
deltas = {
    2: [0.5, 0],
    3: [1.0, 0]
}

# Create a new arms
arm = Arm(copy.deepcopy(thetas), copy.deepcopy(deltas))

# Set the initial temp
temp = INIT_TEMP

#Sets the score of an arm. TODO: Modify this based on penalty
def setScore(a):
    penalty = a.thetas[1][1] * 3
    penalty += a.thetas[4][1]
    penalty += a.thetas[5][1]
    penalty += a.thetas[6][1]
    penalty += a.deltas[2][1] * 2
    penalty += a.deltas[3][1] * 2
    a.score = a.getDistance(DESTINATION) * 10 + penalty

# Find our initial position and distance from target
arm.initMoves(MOVE_COUNT)
setScore(arm)
print("Start Position: {0}".format(arm.getPosition()))
print("Start Distance: {0:.2f}cm".format(arm.getDistance(DESTINATION) * 100))

# Loop the simulated annealing algorythm
while temp > STOP_TEMP:
    # Find an alternate solution
    alt = arm.getAlt(MODS)
    
    # Simulate alternate arm, and find its final score
    alt.simulate()
    setScore(alt)

    # Choose a solution
    if arm.choose(alt, temp):
        arm = alt
    
    # Adjust the tempurature
    temp *= COOLING_RATE
    print("\r>> Tempurature: {0:.4f}".format(temp), end = " ")
    sys.stdout.flush()

# Print the final location and distance from target
print("\nEnd Position: {0}".format(arm.getPosition()))
print("End Distance: {0:.2f}cm".format(arm.getDistance(DESTINATION) * 100))

# Print the angles changes
print("T1(Cumulative/Total): {0}° / {1}°".format(
    int(d(arm.thetas[1][1])), 
    int(d(arm.thetas[1][0] - thetas[1][0]) % 360 - (360 if (arm.thetas[1][0] - thetas[1][0]) < 0 else 0))
))
print("T4(Cumulative/Total): {0}° / {1}°".format(
    int(d(arm.thetas[4][1])), 
    int(d(arm.thetas[4][0] - thetas[4][0]) % 360 - (360 if (arm.thetas[4][0] - thetas[4][0]) < 0 else 0))
))
print("T5(Cumulative/Total): {0}° / {1}°".format(
    int(d(arm.thetas[5][1])), 
    int(d(arm.thetas[5][0] - thetas[5][0]) % 360 - (360 if (arm.thetas[5][0] - thetas[5][0]) < 0 else 0))
))
print("T6(Cumulative/Total): {0}° / {1}°".format(
    int(d(arm.thetas[6][1])), 
    int(d(arm.thetas[6][0] - thetas[6][0]) % 360 - (360 if (arm.thetas[6][0] - thetas[6][0]) < 0 else 0))
))

# Print the arm changes
print("D2(Cumulative/Total): {0:.2f}cm / {1:.2f}cm".format(
    arm.deltas[2][1] * 100,
    (arm.deltas[2][0] - deltas[2][0]) * 100
))
print("D3(Cumulative/Total): {0:.2f}cm / {1:.2f}cm".format(
    arm.deltas[3][1] * 100,
    (arm.deltas[3][0] - deltas[3][0]) * 100
))
print()