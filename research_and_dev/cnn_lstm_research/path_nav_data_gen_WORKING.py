import numpy as np
import settings
# import keras
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.python import keras
# from tf.layers import Sequential
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Flatten
from tensorflow.python.keras.layers import TimeDistributed


# from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import Sequential
# from keras.models import Sequential
# from keras.layers import Conv2D
# from keras.layers import MaxPooling2D
# from keras.layers import LSTM
# from keras.layers import Dense
# from keras.layers import Flatten
# from keras.layers import TimeDistributed
from research_and_dev.event_driven_system.nav_data_tools import load_nav_data
import os
import settings

# print(tf.__version__) => 1.14.0
# print(tf.keras.__version__) => 2.2.4-tf
# https://docs.floydhub.com/guides/environments/ says: TensorFlow 1.14 & TensorFlow 1.14.0 + Keras 2.2.5 on Python 3.6.
# BUT Keras 2.2.5 does not seem to exist!

nav_data_arrays_dir_path = r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\data\event_driven_sys_data\frame_traj_arrays"
nav_data_arrays = load_nav_data.load_traj_recs_dataset(nav_data_arrays_dir_path)


path_nav_1_data = nav_data_arrays[0]
path_nav_2_data = nav_data_arrays[0]
path_nav_3_data = nav_data_arrays[1]
path_nav_4_data = nav_data_arrays[2]
path_nav_5_data = nav_data_arrays[3]
path_nav_6_data = nav_data_arrays[4]


frame_height = 76
frame_width = 76
frame_channels = 3


# def gen_single_path_nav_run_data(tot_max_frames_recorded, iunique_id_shift=0):
# 	path_nav_frames_list = []
# 	for step_i in range(1, tot_max_frames_recorded + 1):
# 		# step_i_frames_list = [ for ]
# 		step_i_unique_id = step_i + iunique_id_shift
# 		step_i_frames_list = [np.ones((frame_height, frame_width, frame_channels))*step_i_unique_id for i in range(1, step_i + 1)]
# 		path_nav_frames_list.append(step_i_frames_list)
# 	return path_nav_frames_list
#
#
# path_nav_1_data = gen_single_path_nav_run_data(5)
# path_nav_2_data = gen_single_path_nav_run_data(7, iunique_id_shift=5)
# path_nav_3_data = gen_single_path_nav_run_data(6, iunique_id_shift=5+7)
# print(len(path_nav_1_data))
# print(len(path_nav_2_data))
# print(len(path_nav_3_data))


# all_path_nav_data_list = [path_nav_1_data, path_nav_2_data, path_nav_3_data]
all_path_nav_data_list = [path_nav_1_data, path_nav_2_data, path_nav_3_data, path_nav_4_data, path_nav_5_data, path_nav_6_data]

smallest_path_nav_data_size = min([len(path_nav_data_i) for path_nav_data_i in all_path_nav_data_list])
print(f"smallest_path_nav_data_size: {smallest_path_nav_data_size}")

truncated_path_nav_data_sets = [truncated_path_nav_data_i[:smallest_path_nav_data_size] for truncated_path_nav_data_i in all_path_nav_data_list]
# print(f"len(truncated_path_nav_data_sets[0]): {len(truncated_path_nav_data_sets[0])}")
# print(f"len(truncated_path_nav_data_sets[1]): {len(truncated_path_nav_data_sets[1])}")
# print(f"len(truncated_path_nav_data_sets[2]): {len(truncated_path_nav_data_sets[2])}")


flat_list = [path_nav_data_batch_frames_seq_j for path_nav_data_batch_i in
             truncated_path_nav_data_sets for path_nav_data_batch_frames_seq_j in path_nav_data_batch_i]

print(f"len(flat_list): {len(flat_list)}")


padding_img = np.zeros((frame_height, frame_width, frame_channels))
padded_imgs = []
for list_i in flat_list:
	list_i_len = len(list_i)
	num_padding_imgs_to_add = smallest_path_nav_data_size - list_i_len
	# for padding_img_i in range(num_padding_imgs_to_add):
	for _ in range(num_padding_imgs_to_add):
		list_i.append(padding_img)
	padded_imgs.append(list_i)

# print(f"len(padded_imgs): {len(padded_imgs)}")
# print(f"len(padded_imgs[0]): {len(padded_imgs[0])}")
# print(f"len(padded_imgs[1]): {len(padded_imgs[1])}")
# print(f"len(padded_imgs[2]): {len(padded_imgs[2])}")
# print(f"len(padded_imgs[3]): {len(padded_imgs[3])}")
# print(f"len(padded_imgs[8]): {len(padded_imgs[8])}")
# print(f"len(padded_imgs[12]): {len(padded_imgs[12])}")
# print(f"len(padded_imgs[13]): {len(padded_imgs[13])}")
# print(f"len(padded_imgs[14]): {len(padded_imgs[14])}")


X_train = np.stack(padded_imgs, axis=0) # X_train.shape => (15, 5, 60, 60, 3)

# dummmy_ohe_target_cls_label = [0, 0, 0, 0, 0, 0]
dummmy_ohe_target_cls_label = np.zeros((15, 6))

y_train = dummmy_ohe_target_cls_label



# configure problem
size = 60
height = 60
width = 60
channels = 3
# traj_frames_dataset = None
frames = 5
# define the model
model = Sequential()
# A Conv2D layer requires input_shape = (batch_size, width, height, channels)
# input_shape = (batch_size, # of traj_frames_dataset, height, width, channels) <=> (batch_size, samples, height, width, channels)
model.add(TimeDistributed(Conv2D(32, (2, 2), activation='relu'), input_shape=(frames, height, width, channels)))
# Where traj_frames_dataset (=samples) is  set to None, so I should be able to feed the network any slice of my long sequence.
# The shape of the output feature map of the first layer above will be: (batch_size, traj_frames_dataset, filter_height, filter_width, filters)
model.add(TimeDistributed(MaxPooling2D(pool_size=(2, 2))))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(10))
model.add(Dense(6, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
print(model.summary())

# fit model on
# 5,000 randomly generated sequences.
print("Generating X_train and y_train, and fitting model on this data with batch_size=32 and epochs=5")
# X_train, y_train = generate_examples(size, 100)
model.fit(X_train, y_train, batch_size=5, epochs=2, verbose=1)

# print(len(path_nav_1_data))
# print(len(path_nav_1_data[0]))
# print(len(path_nav_1_data[1]))
# print(len(path_nav_1_data[2]))
# print(len(path_nav_1_data[3]))
# print(len(path_nav_1_data[4]))

