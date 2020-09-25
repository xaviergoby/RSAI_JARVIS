from keras.layers import Dropout
from keras.layers import TimeDistributed
from keras import backend as K
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.layers import Input, LSTM, Dense
from keras.models import Model
import keras


frames_per_seq = 10
img_width = 4101
img_height = 247
train_data_dir = '/training'
validation_data_dir = 'validation'


multiplier = 1
num_classes = 9
nb_train_samples = multiplier*num_classes*70
nb_validation_samples = multiplier*num_classes*20
epochs = 50
batch_size = 10


if K.image_data_format() == 'channels_first':
	print('channels_first')
	# input_shape = (batch_size, n_channels, image_height, image_width)
	# input_shape = (frames_per_seq, 3, img_width, img_height)
	# input_shape = (None, 3, img_width, img_height)
	# input_shape = (3, img_width, img_height)
	input_shape = (1, img_width, img_height)
	# input_shape = (1, 1, img_width, img_height)
	# input_shape = (1, img_width, img_height, None)
else:
	print('channels_last')
	# (batch_size, image_height, image_width, n_channels)
	# input_shape = (frames_per_seq, img_width, img_height, 3)
	# input_shape = (None, img_width, img_height, 3)
	# input_shape = (img_width, img_height, 3)
	input_shape = (img_width, img_height, 1)
	# input_shape = (1, img_width, img_height, 1)
	# input_shape = (None, img_width, img_height, 1)

input_tensor = Input(shape=input_shape, name="CONV_Input_Tensor")

conv1 = Conv2D(8, kernel_size=(3, 3), activation="relu")(input_tensor)
mp1 = MaxPooling2D((2, 2), padding='same')(conv1)
do1 = Dropout(0.5)(mp1)

conv2 = Conv2D(16, kernel_size=(3, 3), activation="relu")(do1)
mp2 = MaxPooling2D((2, 2), padding='same')(conv2)
do2 = Dropout(0.5)(mp2)

flat = Flatten()(do2)

d1 = Dense(128, activation="relu")(flat)
do4 = Dropout(0.5)(d1)
d2 = Dense(64, activation="relu")(do4)
do5 = Dropout(0.5)(d2)
d3 = Dense(32, activation="softmax")(do5)




input_tensor2 = Input(shape=(4,), name="FCMLP_Input_Tensor")

d1nn2 = Dense(16, activation="relu")(input_tensor2)
do1nn2 = Dropout(0.5)(d1nn2)
d2nn2 = Dense(8, activation="relu")(do1nn2)
# do2nn2 = Dropout(0.5)(d2nn2)
# d3nn2 = Dense(num_classes, activation="softmax")(do2nn2)


concatenated = keras.layers.concatenate([d3, d2nn2], axis=-1)


label_pred_res = Dense(num_classes, activation="softmax")(concatenated)

model = Model(inputs=[input_tensor, input_tensor2], outputs=label_pred_res)

model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer="adam")

print(model.summary)
from keras.utils import plot_model
model_graph_file_name_extra_info = "multi_input_conv2d_fcmlp"
plot_model(model, to_file='model_{0}.png'.format(model_graph_file_name_extra_info), show_shapes=True)

