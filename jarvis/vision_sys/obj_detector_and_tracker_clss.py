from jarvis.vision_sys.obj_detector import ObjectDetector
from jarvis.vision_sys.obj_tracker import CentroidTracker




class ODT:
	# ODT: "Object Detection/Detector and Tracking/Tracjer"
	
	def __init__(self, roi: "(l, t, w, h) tuple", max_detections=10, confidence_threshold=0.1, max_obj_frames_lost=5):
		"""
		:param roi: tuple of game client area pos & size (left, top, width height)
		"""
		self.roi = roi
		self.max_detections = max_detections
		self.confidence_threshold = confidence_threshold
		self.max_obj_frames_lost = max_obj_frames_lost
		# self.sensor = Sensor(self.roi)
		self.detector = ObjectDetector(self.roi, self.max_detections, self.confidence_threshold)
		self.tracker = CentroidTracker(self.roi, self.max_obj_frames_lost)
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