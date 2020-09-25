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
import read_labels_map_file
import random
from pyclick import HumanClicker


class ObjDectInferenceGenerator:
	
	def __init__(self, task_name):
		sys.path.append("..")
		self.task_name = task_name
		self.model_frozen_inference_graph_file_path = os.path.join(settings.OBJ_DECT_INFERENCE_GRAPHS_DIR,
																   r"tasks\{0}\frozen_inference_graph.pb".format(
																	   self.task_name))
		self.label_map_file_path = os.path.join(settings.OBJ_DECT_TRAINING_LABEL_MAPS_DIR,
												r"tasks\{0}_label_map.pbtxt".format(self.task_name))
		self.label_map_dict = read_labels_map_file.read_label_map(self.label_map_file_path)
		self.num_class_labels = len(list(self.label_map_dict.keys()))
		self.load_model()
		self.generate_gpu_config()
		self.prepare_infer_sess()
	
	def load_model(self):
		label_map = label_map_util.load_labelmap(self.label_map_file_path)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.num_class_labels,
																	use_display_name=True)
		category_index = label_map_util.create_category_index(categories)
		detection_graph = tf.Graph()
		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(self.model_frozen_inference_graph_file_path, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
		self.detection_graph, self.category_index = detection_graph, category_index
	
	# return detection_graph, category_index
	
	def generate_gpu_config(self):
		gpu_config = tf.ConfigProto()
		gpu_config.gpu_options.allow_growth = True
		# config.gpu_options.per_process_gpu_memory_fraction = memory_fraction
		self.gpu_config = gpu_config
	
	# return gpu_config
	
	def prepare_infer_sess(self):
		self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
		self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
		with self.detection_graph.as_default():
			inference_sess = tf.Session(graph=self.detection_graph, config=self.gpu_config)
			# with tf.Session(graph=self.detection_graph, config=self.gpu_config) as inference_sess:
				# self.inference_sess = inference_sess
				# return inference_sess
			self.inference_sess = inference_sess
			# return inference_sess
	
	def infer_from_img(self, img, return_img=False):
		"""
		:param img: numpy.ndarray of RGB image
		:return: 4-tuple consisting of (boxes, obj_scores, classes, num_detections)
		Where:
		boxes:
			type(boxes) => numpy.ndarray
			type(boxes[i]) => numpy.ndarray
			boxes[i] => ymin, xmin, ymax, xmax
		obj_scores:
			type(obj_scores) => numnpy.ndarray
		classes:
			type(classes) => numnpy.ndarray
		num_detection:
			type(num_detections) => numnpy.ndarray
		"""
		image_np = img
		height, width, _ = image_np.shape
		image_np_expanded = np.expand_dims(image_np, axis=0)
		(boxes, scores, classes, num_detections) = self.inference_sess.run([self.detection_boxes, self.detection_scores,
																			self.detection_classes,
																			self.num_detections],
																		   feed_dict={self.image_tensor: image_np_expanded})
		boxes = np.squeeze(boxes)
		scores = np.squeeze(scores)
		classes = np.squeeze(classes).astype(np.int32)
		num_detections = np.squeeze(num_detections)
		if return_img is False:
			return boxes, scores, classes, num_detections
		else:
			return boxes, scores, classes, num_detections, img
	
	def visual_img_inference(self, img, confidence_threshold=0.1):
		img_inference_res = self.infer_from_img(img)
		boxes, scores, classes, num_detections = img_inference_res
		vis_util.visualize_boxes_and_labels_on_image_array(
			img,
			boxes,
			classes,
			scores,
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=4,
			min_score_thresh=confidence_threshold)
		
		# cv2.imshow('window', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
		# cv2.imshow('window', img)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		return boxes, scores, classes, num_detections, img
		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	cv2.destroyAllWindows()
		
		
class ObjDectMiningActuatorControl:
	
	def __init__(self, roi):
		self.roi = roi
		self.lmc_click_time = 0
		
	def grab_game_client_roi_screen_shot(self):
		screen_shot_img = np.array(ImageGrab.grab(bbox=self.roi))
		self.screen_shot_img = screen_shot_img
		self.screen_shot_img_height = self.screen_shot_img[0]
		self.screen_shot_img_width = self.screen_shot_img[1]
		
	def compute_inference_bbox_centre_coords(self, img_height, img_width, infered_bbox_norm_coords):
		norm_y_min, norm_x_min, norm_y_max, norm_x_max = tuple(infered_bbox_norm_coords.tolist())
		y_min, y_max = int(norm_y_min * img_height), int(norm_y_max * img_height)
		x_min, x_max = int(norm_x_min * img_width), int(norm_x_max * img_width)
		y_c = (y_max - y_min) // 2 + y_min + self.roi[1]
		x_c = (x_max - x_min) // 2 + x_min + self.roi[0]
		return y_c, x_c
	
	def perform_lmc(self, img_height, img_width, infered_bbox_norm_coords):
		wait_time = random.uniform(10, 15)
		if time.time() - self.lmc_click_time > wait_time or self.lmc_click_time == 0:
			y_c, x_c = self.compute_inference_bbox_centre_coords(img_height, img_width, infered_bbox_norm_coords)
			hc = HumanClicker()
			hc.move((x_c, y_c), random.uniform(0.5, 0.9))
			hc.click()
			self.lmc_click_time = time.time()
		else:
			return
		
	


if __name__ == "__main__":
	inf = ObjDectInferenceGenerator("mining")
	print(inf.label_map_dict)
	print(inf.num_class_labels)
	print(inf.inference_sess)
	
	
	# from PIL import Image
	# import cv2
	cv2_img = cv2.imread('mining_12.png')
	cv2_rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
	# resized_cv2_rgb_img = cv2.resize(cv2_rgb_img, (600, 600))
	# resized_cv2_rgb_img = cv2.resize(cv2_rgb_img, (int(cv2_rgb_img.shape[0]*1.5), int(cv2_rgb_img.shape[1]*1.5)))
	# resized_cv2_rgb_img = cv2.resize(cv2_img, (int(cv2_img.shape[0]*1.5), int(cv2_img.shape[1]*1.5)))
	
	from src.ui_automation_tools import screen_tools
	
	screen_tools.set_window_pos_and_size()
	client_main_view_roi_coords = (8, 31, 791, 591)
	region = client_main_view_roi_coords
	
	inf_actuator_controller = ObjDectMiningActuatorControl(region)
	
	while True:
		screen_shot_img = np.array(ImageGrab.grab(bbox=region))
		img_2_infer = screen_shot_img
		img_height = img_2_infer.shape[0]
		img_width = img_2_infer.shape[1]
		
		# img_inference_res = inf.infer_from_img(img_2_infer)
		img_inference_res = inf.visual_img_inference(img_2_infer)
		
		bbox_overlayed_inf_img_res = img_inference_res[-1]
		
		cv2.imshow('window', cv2.cvtColor(bbox_overlayed_inf_img_res, cv2.COLOR_BGR2RGB))
		first_bbox_norm_coords = img_inference_res[0][random.randint(1, 3)]
		
		inf_actuator_controller.perform_lmc(img_height, img_width, first_bbox_norm_coords)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
		
	# print(img_2_infer.shape)
	# img_height = img_2_infer.shape[0]
	# img_width = img_2_infer.shape[1]
	# first_bbox_norm_coords = img_inference_res[0][0]
	# norm_y_min, norm_x_min, norm_y_max, norm_x_max = tuple(first_bbox_norm_coords.tolist())
	# y_min, y_max = int(norm_y_min * img_height), int(norm_y_max * img_height)
	# x_min, x_max = int(norm_x_min * img_width), int(norm_x_max * img_width)
	# print(f"y_min: {y_min}")
	# print(f"x_min: {x_min}")
	# print(f"y_max: {y_max}")
	# print(f"x_max: {x_max}")
	# y_c = (y_max - y_min) // 2 + y_min + client_main_view_roi_coords[1]
	# x_c = (x_max - x_min) // 2 + x_min + client_main_view_roi_coords[0]
	#
	# import pyautogui
	# import random
	# from pyclick import HumanClicker
	#
	# hc = HumanClicker()
	# hc.move((x_c, y_c), random.uniform(0.5, 0.9))
	# hc.click()
	import pyautogui
	import random
	x_lmc = random.randint(400, 600)
	y_lmc = random.randint(400, 600)
	pyautogui.moveTo(x_lmc, y_lmc, random.uniform(0.5, 0.9))
	pyautogui.mouseDown(button='left')
	time.sleep(0.01)
	pyautogui.mouseUp()
	#
	# print(f"y_c: {y_c}")
	# print(f"x_c: {x_c}")
	#
	#
	# print(img_inference_res[1][:5])
