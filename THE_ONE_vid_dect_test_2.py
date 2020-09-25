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
MODEL_NAME = 'inference_graph'

# Path to my current working directory
CWD_PATH = os.getcwd()

# Path to the graph of the frozen object detection which is a .pb file which represents the model that is used
# for object detection. NOTE: the .ckpt file is the old version output of saver.save(sess), which is the equivalent of my .ckpt-data.
# A .ckpt-data file contains the values for all the variables, without the structure. To restore a model in python, I can
# either use the meta and data files or use the .pb file. This is because the .pb file can save my/the whole graph (meta + data).
# To load and use (but not train) a graph in c++ I first need to create it w/ the function freeze_graph, which creates the .pb file from the meta and data.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
# Path to label map file which has the .pbtxt extension and is contained in the 'training' folder
# The purposes of the label map is that of providing indices which are linked with the names of
# each categorical label. This is because the convolution network predicts int's and not strs!
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','object-detection.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

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
    # sess = tf.Session(graph=detection_graph)


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



##########   This section involves "live-streaming" that which is being displayed within the screen ROI, frame per frame, then       ##########
##########   performing object detection on each frame and finally taking a certain action within the game accordig to some logic    ##########
# Define the size of the screen region of interest, ROI
region = (1, 31, 918, 689)
# Get the time as a floating point number expressed in seconds since the epoch, in UTC.
t = time.time()

# Continuously stream each frame and perform the necessary in-game actions
while True:
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
        line_thickness=8,
        min_score_thresh=0.15)

    # max_score_idx = np.amax(np.squeeze(obj_scores))
    # idx = np.where(np.squeeze(obj_scores) == np.amax(np.squeeze(obj_scores)))
    # print(idx)
    # print(max_score_idx)
    # print("best pred box coords: {0}".format(boxes[0]))
    # coords = np.squeeze(boxes)[0]
    # hw = [658, 917, 658, 917]
    # res = hw * coords
    # res = res.astype(int)
    # y_c = (res[2] - res[0])//2 + res[0]
    # x_c = (res[3] - res[1])//2 + res[1]
    # print(x_c, y_c)
    # pyautogui.click(local_x=x_c, local_y=y_c)
    # print("Number of boxes: {0} |  Number of obj_scores: {1}  |  Max obj_scores: {2}".
    #     format(len(np.squeeze(boxes)), len(np.squeeze(obj_scores)), max(np.squeeze(obj_scores))))



    # print("Start time: ", datetime.datetime.now())
    # results = rcnn.detect([printscreen], verbose=0)
    # print("End time: ", datetime.datetime.now())
    # boxes = results[0]["rois"]
    # for box in np.squeeze(boxes):
    #     x1 = box[1]
    #     y1 = box[0]
    #     x2 = box[3]
    #     y2 = box[2]
    #     pts1 = (x1, y1)
    #     pts2 = (x2, y2)
    #     print(pts1)
    #     print(pts2)
    #     cv2.rectangle(image, pts1, pts2,
    #                   color=(0, 255, 0), thickness=3)
    # print('loop took {} seconds'.format(time.time()-last_time))
    # last_time = time.time()
    # coords = np.squeeze(boxes)[0]
    # hw = [658, 917, 658, 917]
    # res = hw * coords
    # res = res.astype(int)
    # y_c = (res[2] - res[0]) // 2 + res[0] + 31
    # x_c = (res[3] - res[1]) // 2 + res[1]
    slaying = False
    # if np.squeeze(obj_scores)[0] > 0.3:
    if time.time() - t > 15:
        if np.squeeze(scores)[0] > 0.15:
            # if time.time() - t < 17:
        # slaying = False
        #     if time.time() - t > 17:
            coords = np.squeeze(boxes)[0]
            hw = [658, 917, 658, 917]
            res = hw * coords
            res = res.astype(int)
            y_c = (res[2] - res[0]) // 2 + res[0] + 31
            x_c = (res[3] - res[1]) // 2 + res[1]
            print(x_c, y_c)
            # command = "application"
            # os.system(command)
            pyautogui.moveTo(x_c, y_c)
            pyautogui.click(x=x_c, y=y_c, clicks=2)
            # pyautogui.click(local_x=x_c, local_y=x_c, clicks=2, interval=1)
            # pyautogui.click(local_x=x_c, local_y=x_c, button='right')
            pyautogui.mouseDown(button='left')
            time.sleep(0.01)
            pyautogui.mouseUp()
            t = time.time()
            # time.sleep()
            # if time.time() - t < 17:
            #     slaying = False
        elif np.squeeze(scores)[0] < 0.3:
            y = random.randint(250, 500)
            # local_y = random.choice([250, 500])
            # local_x = random.choice([350, 600])
            x = random.randint(350, 600)
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click(clicks=2)
            x = np.random.uniform(2, 3, 1000)
            # rand_float_sec_wait = x[random.randint(1, 3)]
            # time.sleep(rand_float_sec_wait)
            
            # time.sleep(random.randint(1, 3))
        #     time.sleep(1)


    # elif time.time() - t > 5
    # elif np.squeeze(obj_scores)[0] < 0.1:
    #     if time.time() - t > 1:
    #         pyautogui.click(600, 400)
    #         time.sleep(1)
    cv2.imshow('window', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


    # time.sleep(1)
    # time.sleep(0.5)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# region = (0, 40, 800, 640) #  OG
# region = (-7, 0, 934, 728)
# region = (-7, 0, 521, 340)
region = (1, 31, 918, 689)
# width =
# screen_record(region)

