import numpy as np
import matplotlib.pyplot as plt
from random import random
from random import randint
from numpy import array
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import TimeDistributed

# generate the next frame in the sequence
def next_frame(last_step, last_frame, column):
	# define the scope of the next step
	lower = max(0, last_step - 1)
	upper = min(last_frame.shape[0] - 1, last_step + 1)
	# choose the row index for the next step
	step = randint(lower, upper)
	# copy the prior frame
	frame = last_frame.copy()
	# add the new step
	frame[step, column] = 1
	return frame, step


# generate a sequence of traj_frames_dataset of a dot moving across an image
def build_frames(frames_size_and_seq_len):
	# Create an empty list which will contain
	# ;en(frames_size_and_seq_len) number of traj_frames_dataset as elements.
	frames_list = []
	# Create an initial (frames_size_and_seq_len x frames_size_and_seq_len) frame
	# filled with 0's. This is essentially just an (frames_size_and_seq_len x frames_size_and_seq_len)
	# 2D numpy array!
	frame = np.zeros((frames_size_and_seq_len, frames_size_and_seq_len))
	# Pick some random integer between 0 and frames_size_and_seq_len - 1 to
	# determine which row to begin drawing the line at.
	line_init_row_idx = randint(0, frames_size_and_seq_len - 1)
	# Set a threshold for the direction in which the line will be
	# drawn, so left-2-right or right-2-left
	direction_threshold = 0.5
	# Createa a threshold for the probability drawing the line in a
	rightwards_direction_threshold = random()
	# Now use direction_threshold to determine whether the line is drawn
	# towards the right (so line is drawn from left-to-right)
	if rightwards_direction_threshold > direction_threshold:
		rightwards_direction = True
		direction = 1 # rightwards
	else:
		rightwards_direction = False
		direction = 0 # leftwards
	# Pick the correct index of the starting column for the direction in which
	# the arrow will be drawn!
	if rightwards_direction is True:
		line_init_col_idx = 0
	else:
		line_init_col_idx = frames_size_and_seq_len - 1
	# Assign the init cell of the frame of the grid of zeros with the value 1!
	frame[line_init_row_idx, line_init_col_idx] = 1
	# Append this 1st frame of the sequence of traj_frames_dataset to frames_list
	frames_list.append(frame)
	# Create all the remaining traj_frames_dataset (of grids) by drawing the line longer and loger
	# for each new frame!
	for frame_i in range(1, frames_size_and_seq_len):
		line_init_col_idx = frame_i if rightwards_direction else frames_size_and_seq_len - 1 - frame_i
		frame, line_init_row_idx = next_frame(line_init_row_idx, frame, line_init_col_idx)
		frames_list.append(frame)
	return frames_list, direction


# # generate sequence of traj_frames_dataset
# size = 5
# traj_frames_dataset, direction = build_frames(size)
# # plot all traj_frames_dataset
# plt.figure()
# for i in range(size):
# 	# create a gray scale subplot for each frame
# 	plt.subplot(1, size, i + 1)
# 	plt.imshow(traj_frames_dataset[i], cmap='Greys')
# 	# turn of the scale to make it clearer
# 	ax = plt.gca()
# 	ax.get_xaxis().set_visible(False)
# 	ax.get_yaxis().set_visible(False)
# # show the plot
# plt.show()
#
#


# generate multiple sequences of traj_frames_dataset and reshape for network input
def generate_examples(size, num_rand_gen_seqs):
	X, y = list(), list()
	for _ in range(num_rand_gen_seqs):
		frames, right = build_frames(size)
		X.append(frames)
		y.append(right)
	# resize as [samples, timesteps, width, height, channels]
	X = array(X).reshape(num_rand_gen_seqs, size, size, size, 1)
	y = array(y).reshape(num_rand_gen_seqs, 1)
	return X, y

# configure problem
size = 10
height = size
width = size
frames = None

# define the model
model = Sequential()
# A Conv2D layer requires input_shape = (batch_size, width, height, channels)
# input_shape = (batch_size, # of traj_frames_dataset, height, width, channels) <=> (batch_size, samples, height, width, channels)
model.add(TimeDistributed(Conv2D(2, (2,2), activation='relu'), input_shape=(frames, size, size, 1)))
# Where traj_frames_dataset (=samples) is  set to None, so I should be able to feed the network any slice of my long sequence.
# The shape of the output feature map of the first layer above will be: (batch_size, traj_frames_dataset, filter_height, filter_width, filters)
model.add(TimeDistributed(MaxPooling2D(pool_size=(2, 2))))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(10))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
print(model.summary())

# fit model on
# 5,000 randomly generated sequences.
print("Generating X_train and y_train, and fitting model on this data with batch_size=32 and epochs=5")
X_train, y_train = generate_examples(size, 100)
model.fit(X_train, y_train, batch_size=32, epochs=5, verbose=1)


#################### EVALUATION ####################

# evaluate model on
# 100 randomly generated sequences.
print("\nEvalating on 10 randomly generated sequences of traj_frames_dataset")
X_eval, y_eval = generate_examples(size, 10)
loss, acc = model.evaluate(X_eval, y_eval, verbose=1)
print('loss: %f, acc: %f' % (loss, acc*100))

#################### TESTING PREDICTION ####################

# prediction on new data on
# 1 randomly generated sequence.
print("\nPredicting on 1 randomly generated sequence of traj_frames_dataset")
X_test, y_test = generate_examples(size, 1)
yhat = model.predict_classes(X_test, verbose=1)
expected = "Right" if y_test[0]==1 else "Left"
predicted = "Right" if yhat[0]==1 else "Left"
print('Expected: %s, Predicted: %s' % (expected, predicted))