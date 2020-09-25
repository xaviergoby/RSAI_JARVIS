import numpy as np
from PIL import ImageGrab
from jarvis.vision_sys.obj_detector import ObjectDetector
from jarvis.vision_sys.obj_tracker import CentroidTracker
from threading import Thread
import cv2

class Sensor: # \\TODO: Renamed from ObjDectSensorSubSystem to Sensor
	"""
	roi: region of interest
	ss: screen shot
	"""

	def __init__(self, roi: "(l, t, w, h) tuple"):
		"""
		:param roi: tuple of game client area pos & size (left, top, width height)
		"""
		self.roi = roi
		# self.max_detections = max_detections
		# self.confidence_threshold = confidence_threshold
		# self.max_obj_frames_lost = max_obj_frames_lost
		self.current_ss = None
		self.current_obs = None
		# self.detector = ObjectDetector(max_detections, confidence_threshold)
		# self.tracker = CentroidTracker(max_obj_frames_lost)


	def _get_roi_ss(self) -> "(h, w, c) shaped array":
		"""
		:return: game client area screen shot img numpy array w/ shape (h, w, c)
		"""
		roi_screen_shot = np.array(ImageGrab.grab(bbox=self.roi))
		return roi_screen_shot

	def _update_current_ss(self):
		current_ss = self._get_roi_ss()
		self.current_ss = current_ss

	def get_current_ss(self):
		if self.current_ss is None:
			self._update_current_ss()
			return self.current_ss
		else:
			return self.current_ss

	def get_frame(self):
		return self._get_roi_ss()
	
	def read(self):
		return self._get_roi_ss()

	def update_sensor(self):
		self._update_current_ss()

 # if __name__ == "__main":
