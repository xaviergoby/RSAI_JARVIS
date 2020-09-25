import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.utils import to_categorical
import keras
import numpy as np


class DataGenerator(keras.utils.Sequence):
	def __init__(self, X, y, batch_size):
		self.X = X
		self.y = y
		self.num_samples = len(X)
		self.batch_size = batch_size  # number of input samples on a single batch of data generated

	def __len__(self):
		# Total number of steps (batches of samples) to yield from generator before declaring one epoch finished and starting the next epoch.
		# if unspecified, will use the len(generator) as a number of steps.
		steps_per_epoch = np.ceil(self.num_samples / self.batch_size)
		# steps_per_epoch = int(self.num_samples / self.batch_size)
		# if steps_per_epoch * self.batch_size < len(self.X):
		# 	steps_per_epoch += 1
		return steps_per_epoch

	def __getitem__(self, index):
		X = self.X[index * self.batch_size:(index + 1) * self.batch_size]
		y = self.y[index * self.batch_size:(index + 1) * self.batch_size]
		return X, y


def compute_num_samples_per_look_back_period(look_back):
	num_samples_per_look_back_period = ((look_back*(look_back+1))/2)
	return num_samples_per_look_back_period
# print(compute_num_samples_per_look_back_period(7))

def compute_num_batches(num_frame_samples, look_back):
	num_samples_per_look_back_period = compute_num_samples_per_look_back_period(look_back)
	num_look_back_periods = (num_frame_samples-look_back)+1
	num_batches = num_look_back_periods * num_samples_per_look_back_period
	return num_batches
# print(compute_num_batches(70, 7))


def data_gen(X, y, look_back):
	batches = []
	targets = []
	num_samples_per_look_back_period = compute_num_samples_per_look_back_period(look_back)
	num_frame_samples = len(X)
	num_look_back_periods = (num_frame_samples - look_back) + 1 # 70 - 7 + 1 = 64
	num_batches = compute_num_batches(num_frame_samples, look_back)
	for look_back_period_i in range(num_look_back_periods): # look_back_period_i=0, look_back_period_i=1, ...look_back_period_i=63
		print(f"look_back_period_i: {look_back_period_i}")
		for look_back_j in range(look_back): #look_back_j=0, look_back_j=1, ...look_back_j=6
			sub_batches = []
			print(f"look_back_j: {look_back_j}")
			# batch_of_samples_i_j = X[look_back_period_i : look_back_period_i + look_back_j + 1, :, :, :]
			batch_of_samples_i_j_array = X[look_back_period_i : look_back_period_i + look_back_j + 1, :, :, :]
			# batch_of_samples_i_j_array = X[0:0+0+1, :, :, :], batch_of_samples_i_j_array.shape->(1, 60, 60, 3)
			# batch_of_samples_i_j_array = X[0:0+1+1, :, :, :], batch_of_samples_i_j_array.shape->(2, 60, 60, 3)
			# print(f"batch_of_samples_i_j.shape: {batch_of_samples_i_j.shape}")
			print(f"batch_of_samples_i_j_array.shape: {batch_of_samples_i_j_array.shape}")
			# targets_i_j = y[look_back_period_i : look_back_period_i + look_back_j + 1, :]
			targets_i_j_array = y[look_back_period_i : look_back_period_i + look_back_j + 1, :]
			print(f"targets_i_j_array.shape: {targets_i_j_array.shape}")
			# batch_of_samples_i_j_array = np.array(batch_of_samples_i_j)
			# targets_i_j_array = np.array(targets_i_j)
			# batches.append(batch_of_samples_i_j)
			# targets.append(targets_i_j)
			batches.append(batch_of_samples_i_j_array)
			targets.append(targets_i_j_array)
			print(f"batch_of_samples_i_j_array.shape: {batch_of_samples_i_j_array.shape}")
			print(f"targets_i_j_array.shape: {targets_i_j_array.shape}")
	batches_array = np.array(batches)
	targets_array = np.array(targets)
	print(f"batches_array.shape: {batches_array.shape}")
	print(f"targets_array.shape: {targets_array.shape}")
	return batches_array, targets_array

X = np.random.rand(70, 60, 60, 3)
y = to_categorical(np.random.randint(0, 15*15, 70))

batches, targets = data_gen(X, y, 7)
print(f"batches.shape: {batches.shape}")
print(f"targets.shape: {targets.shape}")

print(f"batches[0].shape: {batches[0].shape}")
print(f"targets[0].shape: {targets[0].shape}")

