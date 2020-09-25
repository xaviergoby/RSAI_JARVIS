import os
import numpy as np
import tensorflow as tf
import sys
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util
import settings
import read_labels_map_file
import math


class ObjectDetector: # \\TODO: Renamed from ObjDectInferenceGenSubSystem to ObjectDetector

	def __init__(self, roi, max_detections, confidence_threshold):
		sys.path.append("..")
		# self.task_name = task_name
		self.task_name = "mining"
		self.roi = roi
		self.img_height = None
		self.img_width = None
		self.max_detections = max_detections
		self.confidence_threshold = confidence_threshold
		self.model_frozen_inference_graph_file_path = os.path.join(settings.OBJ_DECT_INFERENCE_GRAPHS_DIR,
		                                                           r"tasks\{0}\frozen_inference_graph.pb".format(self.task_name))
		self.label_map_file_path = os.path.join(settings.OBJ_DECT_TRAINING_LABEL_MAPS_DIR,
		                                        r"tasks\{0}_label_map.pbtxt".format(self.task_name))
		self.label_map_dict = read_labels_map_file.read_label_map(self.label_map_file_path)
		self.num_class_labels = len(list(self.label_map_dict.keys()))
		self.init_detector()
		self.current_detections = None

	def _load_model(self):
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

	def _gen_gpu_config(self):
		gpu_config = tf.ConfigProto()
		gpu_config.gpu_options.allow_growth = True
		self.gpu_config = gpu_config

	def init_detector(self):
		self._load_model()
		self._gen_gpu_config()
		self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
		self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
		with self.detection_graph.as_default():
			inference_sess = tf.Session(graph=self.detection_graph, config=self.gpu_config)
			self.inference_sess = inference_sess

	def _infer_from_img(self, img, return_img=False):
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
		if return_img is True:
			return boxes, scores, classes, num_detections, img
		else:
			return boxes, scores, classes, num_detections

	def _visual_img_inference(self, img, return_img=True):
		img_inference_res = self._infer_from_img(img)
		boxes, scores, classes, num_detections = img_inference_res
		vis_util.visualize_boxes_and_labels_on_image_array(
			img,
			boxes,
			classes,
			scores,
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=4,
			max_boxes_to_draw=self.max_detections,
			min_score_thresh=self.confidence_threshold)
		if return_img is True:
			return boxes, scores, classes, num_detections, img
		else:
			return boxes, scores, classes, num_detections


	def _gen_inf_res_dict(self, img, return_img=True):
		inf_res_dict = {}
		# img_inf_res_key_names = ["norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img"]
		img_inf_res_key_names = ["norm_boxes", "obj_scores", "classes"]
		img_inf_res = self._visual_img_inference(img, return_img=return_img)
		for img_inf_res_i_idx in range(len(img_inf_res_key_names)):
			img_inf_res_i_key_name = img_inf_res_key_names[img_inf_res_i_idx]
			# print(f"img_inf_res_i_key_name: {img_inf_res_i_key_name}")
			if self.max_detections is None or self.max_detections is False:
				img_inf_res_i_val = img_inf_res[img_inf_res_i_idx]
			else:
				img_inf_res_i_val = img_inf_res[img_inf_res_i_idx][:self.max_detections]
			inf_res_dict[img_inf_res_i_key_name] = img_inf_res_i_val
		inf_res_dict["num_detections"] = img_inf_res[3]
		if return_img is True:
			inf_res_dict["inf_res_img"] = img_inf_res[-1]
		else:
			pass
		return inf_res_dict

	def _get_current_detections(self, img, return_img):
		"""
		:param img: numyp array of an image
		:param return_img: whether to return the detect objects superimposed image
		:return: a dict with the 5 keys ("norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img")
		"""
		self.img_height = img.shape[0]
		self.img_width = img.shape[1]
		current_detections = self._gen_inf_res_dict(img, return_img=return_img)
		return current_detections

	def _update_current_detections(self, img, return_img=True):
		self.img_height = img.shape[0]
		self.img_width = img.shape[1]
		current_detections = self._gen_inf_res_dict(img, return_img=return_img)
		self.current_detections = current_detections

	def get_current_detections(self, img, return_img=True):
		"""
		:param img: numpy array of an image
		:param return_img: whether to return the detect objects superimposed image
		:return: a dict with the 5 keys ("norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img")
		where:
		type(norm_boxes) -> array & norm_boxes.shape -> (max_detections, 4)
		type(obj_scores) -> array & obj_scores.shape -> (max_detections, )
		type(classes) -> array & classes.shape -> (max_detections, )
		num_detections??
		type(inf_res_img) -> array & inf_res_img.shape -> (560, 783, 3) when wndw set using def (0, 0, 800, 600) opt
		"""
		return self._get_current_detections(img, return_img)

	# def detect_frame_objects(self, img, return_img=True):
	# 	return self._get_current_detections(img, return_img)

	def detect_objects(self, img, return_img=True):
		"""
		:param img: numyp array of an image
		:param return_img: whether to return the detect objects superimposed image
		:return: a dict with the 5 keys ("norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img")
		"""
		return self._get_current_detections(img, return_img)

	def confident_detections(self, detections):
		"""
		:param detections:
		:return:
		"""
		# inf_res_dict = {}
		# img_inf_res_key_names = ["norm_boxes", "obj_scores", "classes"]
		confident_detections_idxs = np.where(detections["obj_scores"] >= self.confidence_threshold)
		confident_boxes_norm_coords = detections["norm_boxes"][confident_detections_idxs]
		confident_boxes_scores = detections["obj_scores"][confident_detections_idxs]
		confident_boxes_classes = detections["classes"][confident_detections_idxs]
		# inf_res_dict["num_detections"] = img_inf_res[3]
		return confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes

	def compute_bbox_frame_coords(self, bbox_norm_coords: "numpy array w/ shape (1,4)") -> "list [top, left, bottom, right]":
		"""
		NOTE:
		# [y_min, x_min, y_max, x_max] <=> [top, left, bottom, right] <=> [startY, startX, endY, endX]
		:param bbox_norm_coords: numpy array w/ shape (1,4)
		:return: list [top, left, bottom, right]
		"""
		frame_height = self.img_height
		frame_width = self.img_width
		norm_bbox_coords_tuple = tuple(bbox_norm_coords.tolist())
		y_norm_min, x_norm_min, y_norm_max, x_norm_max = norm_bbox_coords_tuple
		y_min, y_max = int(y_norm_min * frame_height), int(y_norm_max * frame_height)
		x_min, x_max = int(x_norm_min * frame_width), int(x_norm_max * frame_width)
		# y_min, x_min, y_max, x_max <= > [top, left, bottom, right]
		# y_min, x_min, y_max, x_max <= > [startY, startX, endY, endX]
		top, left, bottom, right = y_min, x_min, y_max, x_max
		bbox_frame_coords = [top, left, bottom, right]
		return bbox_frame_coords

	def compute_boxes_frame_coords(self, boxes_norm_coords: "numpy array w/ shape (len(boxes_norm_coords), 4)") -> "list of nested [top, left, bottom, right] list":
		"""
		:param boxes_norm_coords: "numpy array w/ shape (len(boxes_norm_coords),4)"
		:return: list of nested [top, left, bottom, right] lists
		"""
		boxes_frame_coords_list = []
		for bbox_i_norm_coords in boxes_norm_coords:
			bbox_i_frame_coords = self.compute_bbox_frame_coords(bbox_i_norm_coords)
			boxes_frame_coords_list.append(bbox_i_frame_coords)
		return boxes_frame_coords_list


	def compute_bbox_frame_centroid(self, bbox_frame_coords: "list [top, left, bottom, right]"):
		top, left, bottom, right = bbox_frame_coords
		print(f"(top, left, bottom, right): {(top, left, bottom, right)}")
		# bbox_fxc = math.ceil((right - left) / 2)
		# bbox_fyc = math.ceil((bottom - top) / 2)
		# print(f"(bbox_fxc, bbox_fyc): {(bbox_fxc, bbox_fyc)}")
		bbox_fxc = (right - left) // 2 + left
		bbox_fyc = (bottom - top) // 2 + top
		print(f"(bbox_fxc, bbox_fyc): {(bbox_fxc, bbox_fyc)}")
		bbox_centroid_in_frame = [bbox_fxc, bbox_fyc]
		# bbox_centroid_in_frame = [bbox_fxc, bbox_fyc]
		return bbox_centroid_in_frame

	def compute_boxes_frame_centroids(self, boxes_frame_coords: "list of nested [top, left, bottom, right] lists"):
		boxes_centroids_in_frame_list = []
		for bbox_i_frame_coords in boxes_frame_coords:
			bbox_i_centroid_in_frame = self.compute_bbox_frame_centroid(bbox_i_frame_coords)
			boxes_centroids_in_frame_list.append(bbox_i_centroid_in_frame)
		return boxes_centroids_in_frame_list

	def compute_bbox_screen_centroid(self, bbox_frame_centroid: "list [fx_c, fy_c]"):
		fx_c, fy_c = bbox_frame_centroid
		pxx_c = fx_c + self.roi[0]
		pxy_c = fy_c + self.roi[1]
		bbox_centroid_on_screen = [pxx_c, pxy_c]
		return bbox_centroid_on_screen

	def compute_boxes_screen_centroids(self, boxes_true_coords):
		boxes_centroids_on_screen_list = []
		for bbox_i_true_coords in boxes_true_coords:
			fx_c_i, fy_c_i = self.compute_bbox_frame_centroid(bbox_i_true_coords)
			pxx_c_i = fx_c_i + self.roi[0]
			pxy_c_i = fy_c_i + self.roi[1]
			boxes_centroids_on_screen_list.append([pxx_c_i, pxy_c_i])
		return boxes_centroids_on_screen_list

	def compute_single_inf_obj_bbox_centre_screen_coords(self, obj_bbox_norm_coords):
		"""
		:param obj_bbox_norm_coords: np arra, [norm_y_min, norm_x_min, norm_y_max, norm_x_max]
		:return: 2-tuple (inf_obj_bbox_screen_centre_y_coord, inf_obj_bbox_screen_centre_x_coord)
		"""
		# frame_height = self.img_height
		# frame_width = self.img_width
		# img_height = self.current_ss.shape[0]
		# img_width = self.current_ss.shape[1]
		obj_bbox_norm_coords_tuple = tuple(obj_bbox_norm_coords.tolist())
		norm_y_min, norm_x_min, norm_y_max, norm_x_max = obj_bbox_norm_coords_tuple
		y_min, y_max = int(norm_y_min * self.img_height), int(norm_y_max * self.img_height)
		x_min, x_max = int(norm_x_min * self.img_width), int(norm_x_max * self.img_width)
		y_c = (y_max - y_min) // 2 + y_min + self.roi[1]
		x_c = (x_max - x_min) // 2 + x_min + self.roi[0]
		return y_c, x_c

	# @staticmethod
	def compute_all_inf_obj_bbox_centre_screen_coords(self, obj_bbox_norm_coords) -> "list of nested [x, y] lists":
		obj_bbox_norm_coords_list = []
		for obj_bbox_norm_coords_i_array in obj_bbox_norm_coords:
			obj_bbox_norm_coords_i = self.compute_single_inf_obj_bbox_centre_screen_coords(obj_bbox_norm_coords_i_array)
			obj_bbox_norm_coords_list.append([obj_bbox_norm_coords_i[0], obj_bbox_norm_coords_i[1]])
		return obj_bbox_norm_coords_list






