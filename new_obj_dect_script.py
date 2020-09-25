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

# screen_tools.set_window_pos_and_size()


# sys.path.append("..")

MODEL_NAME = 'inference_graph'

# CWD_PATH = os.getcwd()

from sys_settings.obj_dect_settings_cls import CollectAndMergeSeriesFeatures
from sys_settings.obj_dect_settings_opts import OBJ_DECT_SETTINGS
import os
import sys
# sys.path.append("..")
# CWD_PATH = os.getcwd()
# print(CWD_PATH)
res = CollectAndMergeSeriesFeatures(settings = OBJ_DECT_SETTINGS["task"]["cow_slaying"])
print(f"res.CWD_PATH: {res.CWD_PATH}")
# print(f"CWD_PATH{CWD_PATH}")
#
# PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, 'frozen_inference_graph.pb')
# PATH_TO_LABELS = os.path.join(CWD_PATH, 'training', 'object-detection.pbtxt')
#
# NUM_CLASSES = 1
#
# label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
# categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
#                                                             use_display_name=True)
# category_index = label_map_util.create_category_index(categories)
#
# detection_graph = tf.Graph()
# with detection_graph.as_default():
# 	od_graph_def = tf.GraphDef()
# 	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
# 		serialized_graph = fid.read()
# 		od_graph_def.ParseFromString(serialized_graph)
# 		tf.import_graph_def(od_graph_def, name='')
#
#
# client_main_view_roi_coords = (8, 31, 791, 591)
# region = client_main_view_roi_coords
#
# min_score_thresh_val = 0.05
# frames_display_loop_delay = 0
#
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# with detection_graph.as_default():
# 	with tf.Session(graph=detection_graph, config=config) as sess:
# 		t = time.time()
# 		while True:
# 			image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# 			detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# 			detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
# 			detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# 			num_detections = detection_graph.get_tensor_by_name('num_detections:0')
# 			time.sleep(frames_display_loop_delay)
# 			image = np.array(ImageGrab.grab(bbox=region))
# 			width = region[2] - region[0]
# 			height = region[3] - region[1]
# 			image_expanded = np.expand_dims(image, axis=0)
# 			print("Start time: ", datetime.datetime.now())
# 			(boxes, obj_scores, classes, num) = sess.run(
# 				[detection_boxes, detection_scores, detection_classes, num_detections],
# 				feed_dict={image_tensor: image_expanded})
# 			print("End time: ", datetime.datetime.now())
#
# 			vis_util.visualize_boxes_and_labels_on_image_array(
# 				image,
# 				np.squeeze(boxes),
# 				np.squeeze(classes).astype(np.int32),
# 				np.squeeze(obj_scores),
# 				category_index,
# 				use_normalized_coordinates=True,
# 				line_thickness=8,
# 				min_score_thresh=min_score_thresh_val)
#
# 			cv2.imshow('window', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
# 			if time.time() - t > 10:
# 				if np.squeeze(obj_scores)[0] >= min_score_thresh_val:
# 					coords = np.squeeze(boxes)[0]
# 					hw = [591, 791, 591, 791]
# 					res = hw * coords
# 					res = res.astype(int)
# 					y_c = (res[2] - res[0]) // 2 + res[0] + 31
# 					x_c = (res[3] - res[1]) // 2 + res[1]
# 					print(x_c, y_c)
# 					pyautogui.moveTo(x_c, y_c)
# 					pyautogui.click(x=x_c, y=y_c, clicks=2)
# 					pyautogui.mouseDon(button='left')
# 					pyautogui.mouseUp()
# 					t = time.time()
# 				elif np.squeeze(obj_scores)[0] < min_score_thresh_val:
# 					y = random.randint(250, 500)
# 					x = random.randint(350, 600)
# 					pyautogui.moveTo(x, y, duration=0.2)
# 					pyautogui.click(clicks=2)
#
# 			if cv2.waitKey(1) & 0xFF == ord('q'):
# 				cv2.destroyAllWindows()
# 				break
