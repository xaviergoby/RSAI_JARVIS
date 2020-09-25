import numpy as np
from jarvis.utils.display_viz.helpers import make_data
import matplotlib.pyplot as plt
from pandas import DataFrame
import seaborn as sns
# your implementation of slam should work with the following inputs
# feel free to change these input values and see how it responds!

# world parameters
num_landmarks      = 5        # number of landmarks
N                  = 20       # time steps
world_size         = 100.0    # size of world (square)

# robot parameters
measurement_range  = 50.0     # range at which we can sense landmarks
motion_noise       = 2.0      # noise in robot motion
measurement_noise  = 2.0      # noise in the measurements
distance           = 20.0     # distance by which robot (intends to) move each iteratation


# make_data instantiates a robot, AND generates random landmarks for a given world size and number of landmarks
data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)

# print out some stats about the data
time_step = 0

print('Example measurements: \n', data[time_step][0])
print('\n')
print('Example motion: \n', data[time_step][1])


def initialize_constraints(N, num_landmarks, world_size):
	''' This function takes in a number of time steps N, number of landmarks, and a world_size,
		and returns initialized constraint matrices, omega and xi.'''
	
	## Recommended: Define and store the size (rows/cols) of the constraint matrix in a variable
	rows = 2* (N + num_landmarks)
	cols = 2* (N + num_landmarks)
	#print(rows)
	#print(cols)
	
	## TODO: Define the constraint matrix, Omega, with two initial "strength" values
	omega = np.zeros((rows, cols))
	## for the initial x, y location of our robot
	#omega = [0,0]
	
	# omega[0][0], omega[1][1] = 1, 1
	
	## TODO: Define the constraint *vector*, xi
	## you can assume that the robot starts out in the middle of the world with 100% confidence
	
	#xi = [ rows, 1]
	xi = np.zeros((rows, 1))
	xi[0][0] = world_size / 2
	xi[1][0] = world_size / 2
	
	return omega, xi




# define a small N and world_size (small for ease of visualization)
N_test = 5
num_landmarks_test = 2
small_world = 10

# initialize the constraints
initial_omega, initial_xi = initialize_constraints(N_test, num_landmarks_test, small_world)


# define figure size
plt.rcParams["figure.figsize"] = (10,7)

# display omega
sns.heatmap(DataFrame(initial_omega), cmap='Blues', annot=True, linewidths=.5)