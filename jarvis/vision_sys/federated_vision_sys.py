import numpy as np
from PIL import ImageGrab
from jarvis.vision_sys.sensor import Sensor
from jarvis.vision_sys.obj_detector import ObjectDetector
from jarvis.vision_sys.obj_tracker import CentroidTracker



class FederatedVision:

	# def __init__(self, roi: "(l, t, w, h) tuple", max_detections=10, confidence_threshold=0.1, max_obj_frames_lost=5, mode="PIL"):
	def __init__(self, roi: "(l, t, w, h) tuple", max_detections=10, confidence_threshold=0.1, max_obj_frames_lost=5, mode="PIL"):
		"""
		:param roi: tuple of game client area pos & size (left, top, width height), i.e. (8, 31, 783, 561) when
		using a pos of (0, 0) and size of (800, 600) for the OSRS Game client window. #//
		:param max_detections: Is dfined as the "maximum number of boxes to visualize.  If None, draw all boxes." and
		is used by the func visualize_boxes_and_labels_on_image_array() and is obtained from/as:
		from models.research.object_detection.utils import visualization_utils as vis_util
		&
		vis_util.visualize_boxes_and_labels_on_image_array(image, boxes, classes, scores, ..., max_boxes_to_draw, min_score_thresh, ...)
		:param confidence_threshold: is also used by vis_util.visualize_boxes_and_labels_on_image_array.
		Defined as "minimum score threshold for a box to be visualized
        agnostic_mode: boolean (default: False) controlling whether to evaluate in
        class-agnostic mode or not.This mode will display obj_scores but ignore classes.
		:param max_obj_frames_lost: Maintains number of consecutive traj_frames_dataset (value) a particular object ID (key)
		has been marked as “lost”for
		:param mode: The choice of "mode" for capturing screen shots of the client area, the options being either
		via the "mss" package or "PIL" package. Is "PIL" by def.
		"""
		self.roi = roi # (8, 31, 789, 561)
		self.img_dims = (self.roi[2]-8, self.roi[3]-31) # 791-8=783   &  591-31=560
		self.max_detections = max_detections
		self.confidence_threshold = confidence_threshold
		self.max_obj_frames_lost = max_obj_frames_lost
		self.mode = mode
		self.sensor = Sensor(roi=self.roi, mode=self.mode)
		self.detector = ObjectDetector(self.roi, self.img_dims, self.max_detections, self.confidence_threshold)
		self.tracker = CentroidTracker(self.roi, self.img_dims, self.max_obj_frames_lost)
		self.spatial_history = None
		self.temporal_history = None
		self.visual_memory = None
		# self.history_len = None



	def enable_manual_recording(self, recording_auth):
		if recording_auth is True:
			self.spatial_history = []
			self.temporal_history = []
			self.visual_memory = []
			# self.history_len = 0
		else:
			pass

	def update_spatial_memory(self, data_dict, frame):
		"""
		:param data_dict: a dict of object ID and obj centroid frame reference coordinates key/value pairs
		:param frame: the numpy array format of the frame img screen shot
		w/ shape (height, width, channels)
		:return:
		"""
		working_spatial_memory = (data_dict, frame)
		self.spatial_history.append(working_spatial_memory)


	def update_temporal_memory(self, data_dict, time):
		"""
		:param data_dict: a dict of object ID and obj centroid frame reference coordinates key/value pairs
		:param time: the time of recording/creation/generation of the data to update the memory with
		:return:
		"""
		working_temporal_memory = (data_dict, time)
		self.temporal_history.append(working_temporal_memory)


	def update_visual_memory(self, data_dict, time, frame):
		"""

		:param data_dict: a dict of object ID and obj centroid frame reference coordinates key/value pairs
		:param time: the time of recording/creation/generation of the data to update the memory with
		:param frame: the numpy array format of the frame img screen shot
		:return:
		"""
		self.update_spatial_memory(data_dict, frame)
		self.update_temporal_memory(data_dict, time)

	# def objs_detected(self):
	# 	frame = self.sensor.get_frame()
	# 	obj_dects = self.detector.get_current_frame_detections(frame)
	# 	obj_dects_norm_coords, obj_dects_scores, obj_dects_classes = self.detector.confident_detections(obj_dects)  # //TODO
	# 	obj_dects_frame_coords = self.detector.compute_boxes_frame_coords(obj_dects_norm_coords)
	# 	obj_dects_frame_centroids = self.detector.compute_boxes_frame_centroids(obj_dects_frame_coords)







