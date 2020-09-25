import os
import numpy as np
import tensorflow as tf
import sys
from models.research.object_detection.utils import label_map_util
from models.research.object_detection.utils import visualization_utils as vis_util
import settings
import read_labels_map_file


class ObjDectInferenceGenSubSystem:
	
	def __init__(self, task_name, max_detections, confidence_threshold):
		sys.path.append("..")
		self.task_name = task_name
		self.max_detections = max_detections
		self.confidence_threshold = confidence_threshold
		self.model_frozen_inference_graph_file_path = os.path.join(settings.OBJ_DECT_INFERENCE_GRAPHS_DIR,
																   r"tasks\{0}\frozen_inference_graph.pb".format(self.task_name))
		self.label_map_file_path = os.path.join(settings.OBJ_DECT_TRAINING_LABEL_MAPS_DIR,
												r"tasks\{0}_label_map.pbtxt".format(self.task_name))
		self.label_map_dict = read_labels_map_file.read_label_map(self.label_map_file_path)
		self.num_class_labels = len(list(self.label_map_dict.keys()))
		self.load_model()
		self.generate_gpu_config()
		self.prepare_infer_sess()
	
	def load_model(self):
		label_map = label_map_util.load_labelmap(self.label_map_file_path)
		categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.num_class_labels,use_display_name=True)
		category_index = label_map_util.create_category_index(categories)
		detection_graph = tf.Graph()
		with detection_graph.as_default():
			od_graph_def = tf.GraphDef()
			with tf.gfile.GFile(self.model_frozen_inference_graph_file_path, 'rb') as fid:
				serialized_graph = fid.read()
				od_graph_def.ParseFromString(serialized_graph)
				tf.import_graph_def(od_graph_def, name='')
		self.detection_graph, self.category_index = detection_graph, category_index
	
	def generate_gpu_config(self):
		gpu_config = tf.ConfigProto()
		gpu_config.gpu_options.allow_growth = True
		self.gpu_config = gpu_config
	
	def prepare_infer_sess(self):
		self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
		self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
		self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
		with self.detection_graph.as_default():
			inference_sess = tf.Session(graph=self.detection_graph, config=self.gpu_config)
			self.inference_sess = inference_sess
	
	def infer_from_img(self, img, return_img=False):
		"""
		:param img: numpy.ndarray of RGB image
		:return: 4-tuple consisting of (boxes, obj_scores, classes, num_detections)
		Where:
		boxes:
			type(boxes) => numpy.ndarray
			boxes.shape => (100, 4)
			type(boxes[i]) => numpy.ndarray
			boxes[i].shape => (4,)
			boxes[i] => y_min, x_min, y_max, x_max <=> [top, left, bottom, right]
		obj_scores:
			type(obj_scores) => numnpy.ndarray
		classes:
			type(classes) => numnpy.ndarray
			classes[0] => int
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
		if return_img is True:
			return boxes, scores, classes, num_detections, img
		else:
			return boxes, scores, classes, num_detections

	def visual_img_inference(self, img, return_img=True):
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
			max_boxes_to_draw=self.max_detections,
			min_score_thresh=self.confidence_threshold)
		if return_img is True:
			return boxes, scores, classes, num_detections, img
		else:
			return boxes, scores, classes, num_detections


	def gen_inf_res_dict(self, img, return_img=True):
		inf_res_dict = {}
		# img_inf_res_key_names = ["norm_boxes", "obj_scores", "classes", "num_detections", "inf_res_img"]
		img_inf_res_key_names = ["norm_boxes", "obj_scores", "classes"]
		img_inf_res = self.visual_img_inference(img, return_img=return_img)
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

	def get_frame_inf_dict(self, img, return_img=True):
		return self.gen_inf_res_dict(img, return_img=return_img)
	
	def frame_objects_detected(self, frame, return_img=True):
		return self.gen_inf_res_dict(frame, return_img=return_img)
	
	def get_detections(self, frame, return_img=True):
		return self.gen_inf_res_dict(frame, return_img=return_img)
	
	def get_top_n_detections(self, frame, return_img=True):
		return self.gen_inf_res_dict(frame, return_img=return_img)
	

	

