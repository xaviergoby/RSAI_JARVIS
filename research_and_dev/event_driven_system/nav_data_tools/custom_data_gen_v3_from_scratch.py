# from keras.models import Sequential
# from keras.layers import Dense, Conv2D, Flatten
# from keras.utils import to_categorical
# import keras
import numpy as np



class DataGenerator:

	# def __init__(self, input_data, target_data, look_back, batch_size):
	def __init__(self, input_data, target_data, look_back):
		self.input_data = input_data
		self.target_data = target_data
		self.look_back = look_back
		# self.num_frame_samples = num_frame_samples
		self.num_frame_samples = len(input_data)
		self.num_samples = len(input_data)
		self.batch_size = self.compute_num_batches()  # number of input samples on a single batch of data generated
		# self.batch_size = batch_size  # number of input samples on a single batch of data generated

	def compute_num_samples_per_look_back_period(self):
		num_samples_per_look_back_period = ((self.look_back * (self.look_back + 1)) / 2)
		return num_samples_per_look_back_period

	def compute_num_batches(self):
		num_samples_per_look_back_period = self.compute_num_samples_per_look_back_period()
		num_look_back_periods = (self.num_frame_samples - self.look_back) + 1
		num_batches = num_look_back_periods * num_samples_per_look_back_period
		return num_batches

	# def data_gen(self, input_data, target_data, look_back):
	def data_gen(self):
		X = self.input_data
		y = self.target_data
		look_back = self.look_back
		batches = []
		targets = []
		num_samples_per_look_back_period = self.compute_num_samples_per_look_back_period()
		num_frame_samples = len(X)
		num_look_back_periods = (num_frame_samples - look_back) + 1  # 70 - 7 + 1 = 64
		num_batches = self.compute_num_batches()
		for look_back_period_i in range(num_look_back_periods):  # look_back_period_i=0, look_back_period_i=1, ...look_back_period_i=63
			print(f"look_back_period_i: {look_back_period_i}")
			for look_back_j in range(look_back):  # look_back_j=0, look_back_j=1, ...look_back_j=6
				sub_batches = []
				print(f"look_back_j: {look_back_j}")
				# batch_of_samples_i_j = X[look_back_period_i : look_back_period_i + look_back_j + 1, :, :, :]
				batch_of_samples_i_j_array = X[look_back_period_i: look_back_period_i + look_back_j + 1, :, :, :]
				# batch_of_samples_i_j_array = X[0:0+0+1, :, :, :], batch_of_samples_i_j_array.shape->(1, 60, 60, 3)
				# batch_of_samples_i_j_array = X[0:0+1+1, :, :, :], batch_of_samples_i_j_array.shape->(2, 60, 60, 3)
				# print(f"batch_of_samples_i_j.shape: {batch_of_samples_i_j.shape}")
				print(f"batch_of_samples_i_j_array.shape: {batch_of_samples_i_j_array.shape}")
				# targets_i_j = y[look_back_period_i : look_back_period_i + look_back_j + 1, :]
				targets_i_j_array = y[look_back_period_i: look_back_period_i + look_back_j + 1, :]
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


	def data_stream_gen(self):
		batches_array, targets_array = self.data_gen()
		for batch_i_target_i_idx in range(batches_array.shape[0]):
			yield batches_array[batch_i_target_i_idx], targets_array[batch_i_target_i_idx]


if __name__ == "__main__":
	from keras.utils import to_categorical
	num_frames = 70 # number of frames <=> number of samples
	frame_height = 60
	frame_width = 60
	frame_channels = 3
	# X = np.random.rand(200, 10, 10, 1)
	X = np.random.rand(num_frames, frame_height, frame_width, frame_channels) # (70, 60, 60, 3)
	# y = to_categorical(np.random.randint(0, 2, 200))
	y = to_categorical(np.random.randint(0, 15*15, num_frames)) # y.shape --> (480, 225) (# of samples/frames, # of ohe cls labels)
	input_data = X
	target_data = y
	look_back = 7
	# batch_size =
	data_gen = DataGenerator(X, y, look_back)
	res = data_gen.data_gen()
	frames_data = res[0]
	target_class_labels = res[1]
	print(f"X.shape: {X.shape}")  # X.shape: (200, 10, 10, 1)
	print(f"y.shape: {y.shape}")  # y.shape: (200, 2)
	# print(f"res[0].shape: {res[0].shape}")
	# print(f"res[1].shape: {res[1].shape}")
	print(f"len(res): {len(res)}")
	print(f"frames_data[0].shape: {frames_data[0].shape}")
	print(f"target_class_labels[0].shape: {target_class_labels[0].shape}")
	print(f"len(res[0]): {len(res[0])}")
	print(f"len(res[1]): {len(res[1])}")
	data_gen_streamer = data_gen.data_stream_gen()
	next_1 = next(data_gen_streamer)
	next_1_input = next_1[0]
	next_1_target = next_1[1]
	print(f"next_1_input: {next_1_input}")
	print(f"next_1_target: {next_1_target}")
	next_2 = next(data_gen_streamer)
	next_2_input = next_2[0]
	next_2_target = next_2[1]
	print(f"next_2_input: {next_2_input}")
	print(f"next_2_target: {next_2_target}")
	# print(next(data_gen_streamer)[0].shape)
	# print(next(data_gen_streamer))
	# print(next(data_gen_streamer))

	# (480, 560, 783, 1)
	# (480, 121)

	# batch #: 1
	# x1 = X[0:1,:,:,:] x1.shape: (1, 560, 783, 1)
	# y1 = y[0:1,:] y1.shape: (1, 121)

	# batch #: 2
	# x2 = X[0:2,:,:,:]  x2.shape: (2, 560, 783, 1)
	# y2 = y[0:2,:]  y2.shape: (2, 121)

	# batch #: 3
	# x3 = X[0:3,:,:,:]  x3.shape: (3, 560, 783, 1)
	# y3 = y[0:3,:]  y3.shape: (3, 121)

	# ...

	# batch #: 7
	# x7 = X[0:7,:,:,:]  x3.shape: (7, 560, 783, 1)
	# y7 = y[0:7,:]  y3.shape: (7, 121)

	# batches, targets = data_gen(X, y, 7)
	# print(f"batches.shape: {batches.shape}")
	# print(f"targets.shape: {targets.shape}")
