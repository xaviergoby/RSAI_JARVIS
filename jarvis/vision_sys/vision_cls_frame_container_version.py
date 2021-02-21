import numpy as np
from PIL import ImageGrab
from jarvis.vision_sys.sensor import Sensor
from jarvis.vision_sys.obj_detector import ObjectDetector
from jarvis.vision_sys.obj_tracker import CentroidTracker


class Vision:  # \\TODO: Renamed from ObjDectSensorSubSystem to Sensor
	"""
	roi: region of interest
	ss: screen shot
	"""

	def __init__(self, roi: "(l, t, w, h) tuple", max_detections=10, confidence_threshold=0.1, max_obj_frames_lost=5,
	             mode="PIL"):
		"""
		:param roi: tuple of game client area pos & size (left, top, width height)
		"""
		self.roi = roi
		self.img_dims = (self.roi[2] - 8, self.roi[3] - 31)
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
		self._current_frame = None
		self._current_objs_detected = None


	def update_current_frame(self):
		self._current_frame = self.sensor.get_frame()# frame.shape -> (560, 783)

	@property
	def current_frame(self):
		if self._current_frame is None:
			self.update_current_frame()
		return self._current_frame

	@property
	def current_objs_detected(self):
		current_objs_detected = self.detector.get_current_frame_detections(self._current_frame)  # apparently I had removed this line in favour of the below, on 13/11/2020
		return current_objs_detected

	def conf_threshold_down_sampling(self):
		confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes = self.detector.confident_detections(self._current_objs_detected)


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

	def objs_detected(self):
		frame = self.sensor.get_frame()
		obj_dects = self.detector.get_current_frame_detections(frame)
		obj_dects_norm_coords, obj_dects_scores, obj_dects_classes = self.detector.confident_detections(obj_dects)  # //TODO
		obj_dects_frame_coords = self.detector.compute_boxes_frame_coords(obj_dects_norm_coords)
		obj_dects_frame_centroids = self.detector.compute_boxes_frame_centroids(obj_dects_frame_coords)







