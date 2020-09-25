import numpy as np
import os
import datetime
import cv2
import sys
import time
from PIL import ImageGrab
import pyautogui
import random
from research_and_dev.rsai_cv_navigability_mapping.world_maps.world_map import WorldMap
from research_and_dev.rsai_cv_navigability_mapping.navigation.navigator import Navigator
from src.utils.time_tools import delay_timer
from src.ui_automation_tools import screen_tools

top_left_origin_world_coords = (3136, 3519)
world_obstacles_array = np.load("world_array.npy")
world_map = WorldMap(world_obstacles_array, top_left_origin_world_coords)
navigator = Navigator(world_map)

world_map_start_pos_world_coords = (3235, 3218)  # (99, 301)
# world_map_end_pos_world_coords = (3251, 3266) # (115, 253)
world_map_end_pos_world_coords = (3257, 3285)  # (115, 253)

# world_map_end_pos_world_coords = (3235, 3218) # (99, 301)
# world_map_start_pos_world_coords = (3251, 3266) # (115, 253)

full_path = navigator.get_full_path(world_map_start_pos_world_coords, world_map_end_pos_world_coords)
shortened_path = navigator.shorten_path(full_path, path_pos_skip_len=10)
path_lmc_actions = navigator.gen_nav_path_lmc_actions(world_map_start_pos_world_coords, shortened_path)
#
screen_tools.set_window_pos_and_size()
delay_timer(5)
navigator.navigate(path_lmc_actions)

import tensorflow as tf
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
# config.gpu_options.per_process_gpu_memory_fraction = 0.8
# sess = tf.Session(config=config)

sys.path.append("..")

MODEL_NAME = 'inference_graph'
CWD_PATH = os.getcwd()
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'object-detection.pbtxt')

NUM_CLASSES = 1

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.Session(graph=detection_graph, config=config)

client_main_view_roi_coords = (8, 31, 791, 591)
region = client_main_view_roi_coords

min_score_thresh_val = 0.05
frames_display_loop_delay = 0

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
with detection_graph.as_default():
	with tf.Session(graph=detection_graph, config=config) as sess:
		t = time.time()
		while True:
			image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
			detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
			detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
			detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
			# Number of obj_centroids detected
			num_detections = detection_graph.get_tensor_by_name('num_detections:0')
			time.sleep(frames_display_loop_delay)
			image = np.array(ImageGrab.grab(bbox=region))
			width = region[2] - region[0]
			height = region[3] - region[1]
			image_expanded = np.expand_dims(image, axis=0)
			print("Start time: ", datetime.datetime.now())
			(boxes, scores, classes, num) = sess.run(
				[detection_boxes, detection_scores, detection_classes, num_detections],
				feed_dict={image_tensor: image_expanded})
			print("End time: ", datetime.datetime.now())
			
			vis_util.visualize_boxes_and_labels_on_image_array(
				image,
				np.squeeze(boxes),
				np.squeeze(classes).astype(np.int32),
				np.squeeze(scores),
				category_index,
				use_normalized_coordinates=True,
				line_thickness=8,
				min_score_thresh=min_score_thresh_val)
			
			cv2.imshow('window', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
			
			if time.time() - t > 10:
				if np.squeeze(scores)[0] >= min_score_thresh_val:
					coords = np.squeeze(boxes)[0]
					hw = [591, 791, 591, 791]
					res = hw * coords
					res = res.astype(int)
					y_c = (res[2] - res[0]) // 2 + res[0] + 31
					x_c = (res[3] - res[1]) // 2 + res[1]
					print(x_c, y_c)
					pyautogui.moveTo(x_c, y_c)
					pyautogui.click(x=x_c, y=y_c, clicks=2)
					pyautogui.mouseDown(button='left')
					time.sleep(0.01)
					pyautogui.mouseUp()
					t = time.time()
				elif np.squeeze(scores)[0] < min_score_thresh_val:
					y = random.randint(250, 500)
					x = random.randint(350, 600)
					pyautogui.moveTo(x, y, duration=0.2)
					pyautogui.click(clicks=2)
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break
