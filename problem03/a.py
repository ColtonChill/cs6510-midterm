from doctest import script_from_examples
from math import radians as r, degrees as d
from arm import Arm
import copy

# Main variables
MOVE_COUNT = 800
INIT_TEMP = 10000000
COOLING_RATE = 0.99
STOP_TEMP = 0.001
MODS = 80

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

# Generate a set of random moves
arm.generateMoves(MOVE_COUNT)

#Sets the score of an arm. TODO: Modify this based on penalty
def setScore(a):
    a.score = a.getDistance(DESTINATION)

# Find our initial score
setScore(arm)
print("Start Distance: {0:.2f}cm".format(arm.score * 100))

# Loop the simulated annealing algorythm
while temp > STOP_TEMP:
    # Find an alternate solution
    alt = arm.getAlt(MODS)
    
    # Simulate alternate arm, and find its current score
    alt.simulate()
    setScore(alt)

    # Choose a solution
    if arm.choose(alt, temp):
        arm = alt
    
    # Adjust the tempurature
    temp *= COOLING_RATE

# Print the final score
print("End distance: {0:.2f}cm".format(arm.score * 100))

# Print the angles changes
delta_t1 = int(d(thetas[1][0] - arm.thetas[1][0]))
delta_t4 = int(d(thetas[4][0] - arm.thetas[4][0]))
delta_t5 = int(d(thetas[5][0] - arm.thetas[5][0]))
delta_t6 = int(d(thetas[6][0] - arm.thetas[6][0]))
print("Delta t1: {0}°".format(delta_t1))
print("Delta t4: {0}°".format(delta_t4))
print("Delta t5: {0}°".format(delta_t5))
print("Delta t6: {0}°".format(delta_t6))

# Print the arm changes
delta_d2 = (deltas[2][0] - arm.deltas[2][0]) * 100
delta_d3 = (deltas[3][0] - arm.deltas[2][0]) * 100
print("Delta d2: {0:.2f}cm".format(delta_d2))
print("Delts d3: {0:.2f}cm".format(delta_d3))
print()