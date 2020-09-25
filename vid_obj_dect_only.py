import os
import datetime
import cv2
import numpy as np
import tensorflow as tf
import sys
import time
from PIL import ImageGrab
import pyautogui
import random
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util
from src.ui_automation_tools import screen_tools
import settings
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.Session(config=config)



# import tensorflow as tf
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#
#     except RuntimeError as e:
#         print(e)
#
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# tf.enable_eager_execution(config=config)

# from research.object_detection.utils import label_map_util
# from research.object_detection.utils import visualization_utils as vis_util

# This is needed since the notebook is stored in the object_detection folder.
# But is this really needed?
sys.path.append("..")

# Name of the directory containing the trained and saved inference_graph
# produced by the object detection module which was chosen, i.e. ssd_mobilenet_v1_pets
task_name = "mining"
task_inference_graph_output_dir_path = os.path.join(settings.OBJ_DECT_INFERENCE_GRAPHS_DIR, r"tasks\{0}".format(task_name))
MODEL_NAME = 'inference_graph'

# Path to my current working directory
CWD_PATH = os.getcwd()

# Path to the graph of the frozen object detection which is a .pb file which represents the model that is used
# for object detection. NOTE: the .ckpt file is the old version output of saver.save(sess), which is the equivalent of my .ckpt-data.
# A .ckpt-data file contains the values for all the variables, without the structure. To restore a model in python, I can
# either use the meta and data files or use the .pb file. This is because the .pb file can save my/the whole graph (meta + data).
# To load and use (but not train) a graph in c++ I first need to create it w/ the function freeze_graph, which creates the .pb file from the meta and data.
# PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
PATH_TO_CKPT = os.path.join(task_inference_graph_output_dir_path,'frozen_inference_graph.pb')

# Path to label map file which has the .pbtxt extension and is contained in the 'training' folder
# The purposes of the label map is that of providing indices which are linked with the names of
# each categorical label. This is because the convolution network predicts int's and not strs!
# PATH_TO_LABELS = os.path.join(CWD_PATH,'training','object-detection.pbtxt')
# C:\Users\Xavier\RSAI_JARVIS\training\label_maps\tasks\mining_label_map.pbtxt
PATH_TO_LABELS = os.path.join(settings.OBJ_DECT_TRAINING_LABEL_MAPS_DIR, r"tasks\mining_label_map.pbtxt")

# Number of classes the object detector can identify
# NUM_CLASSES = 1
NUM_CLASSES = 3

# Loading the label map (file).
# In this case I am simply using the internal utility functions available in this API, however, anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    # with the frozen detection graph .pb file as fid
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(graph=detection_graph, config=config)


##########   This section involves defining input & output tensors (i.e. data) for the object detection process   ##########
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Output tensors are the detection boxes, obj_scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represents level of confidence for each of the obj_centroids.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# Number of obj_centroids detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
##################################################################################################################################

screen_tools.set_window_pos_and_size()


##########   This section involves "live-streaming" that which is being displayed within the screen ROI, frame per frame, then       ##########
##########   performing object detection on each frame and finally taking a certain action within the game accordig to some logic    ##########
# Define the size of the screen region of interest, ROI
# region = (1, 31, 918, 689)
# client_main_view_roi_coords = (8, 31, 783, 560)
client_main_view_roi_coords = (8, 31, 791, 591)
region = client_main_view_roi_coords
# Get the time as a floating point number expressed in seconds since the epoch, in UTC.
t = time.time()

min_score_thresh_val = 0.10
# frames_display_loop_delay = 0.06
frames_display_loop_delay = 0

# Continuously stream each frame and perform the necessary in-game actions
while True:
    time.sleep(frames_display_loop_delay)
    # ImageGrab.grab(bbox=region) where bbox = (left_x, top_y, right_x, bottom_y) = (L, T, R, B)
    image = np.array(ImageGrab.grab(bbox=region))
    # width = L - R = x1 - x0
    width = region[2] - region[0]
    # height = B - T = y1 - y0
    height = region[3] - region[1]
    # Insert a new axis that will appear at the axis position in the expanded array shape.
    # I need to do this since the model expects images to have shape: [1, None, None, 3]
    image_expanded = np.expand_dims(image, axis=0)
    print("Start time: ", datetime.datetime.now())
    # Run/perform inference.All my outputs will be float32 numpy arrays, so don't forget to convert them into
    # another type of data structure if necessary!
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})
    print("End time: ", datetime.datetime.now())

    # Draw the results of the detection (aka 'visulaize the results')
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=4,
        min_score_thresh=min_score_thresh_val)


    cv2.imshow('window', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# region = (1, 31, 918, 689)

