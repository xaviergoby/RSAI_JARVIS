import numpy as np
from PIL import ImageGrab
import mss
from jarvis.vision_sys.obj_detector import ObjectDetector
from jarvis.vision_sys.obj_tracker import CentroidTracker
from threading import Thread
import cv2

class Sensor: # \\TODO: Renamed from ObjDectSensorSubSystem to Sensor
	"""
	roi: region of interest
	ss: screen shot
	"""

	def __init__(self, roi: "(l, t, w, h) tuple", mode="PIL"):
		"""
		:param roi: tuple of game client area pos & size (left, top, width height)
		"""
		self.roi = roi # (left, top, width, height)
		# self.max_detections = max_detections
		# self.confidence_threshold = confidence_threshold
		# self.max_obj_frames_lost = max_obj_frames_lost
		self.current_ss = None
		self.current_obs = None
		self.mode = mode
		self.mss_sct = mss.mss()
		# (8, 31, 783, 560)
		# self.mss_sct_monitor_dims_dict = {"top": 31, "left": 8, "width": 800, "height": 600} # (top, left, width, height)
		self.mss_sct_monitor_dims_dict = {'mon': 1, "top": self.roi[1], "left": self.roi[0], "width": 783, "height": 560} # (top, left, width, height)
		# self.mss_sct_monitor_dims_dict = {'mon': 1, "top": self.roi[1], "left": self.roi[0], "width": self.roi[2], "height": self.roi[3]} # (top, left, width, height)
		# self.mss_sct_monitor_dims_list = [self.roi[0], self.roi[1], self.roi[2], self.roi[3]] # (top, left, width, height)
		# self.mss_sct_monitor_dims_tuple = [self.roi[0], self.roi[1], self.roi[2], self.roi[3]] # (top, left, width, height)
		# self.detector = ObjectDetector(max_detections, confidence_threshold)
		# self.tracker = CentroidTracker(max_obj_frames_lost)

	def _get_roi_PIL_ss(self) -> "(h, w, c) shaped array":
		"""
		:return: game client area screen shot img numpy array w/ shape (h, w, c)
		"""
		PIL_roi_screen_shot = np.array(ImageGrab.grab(bbox=self.roi))
		return PIL_roi_screen_shot

	def _get_roi_mss_ss(self) -> "(h, w, c) shaped array":
		"""
		:return: game client area screen shot img numpy array w/ shape (h, w, c)
		"""
		rgba_mss_roi_screen_shot = np.array(self.mss_sct.grab(self.mss_sct_monitor_dims_dict))
		# rgb_mss_roi_screen_shot = cv2.cvtColor(rgba_mss_roi_screen_shot, cv2.COLOR_RGBA2RGB)
		bgr_mss_roi_screen_shot = cv2.cvtColor(rgba_mss_roi_screen_shot, cv2.COLOR_RGBA2BGR)
		# mss_roi_screen_shot = np.array(self.mss_sct.grab(self.mss_sct_monitor_dims_list))
		# mss_roi_screen_shot = np.asarray(self.mss_sct.grab(self.mss_sct_monitor_dims_tuple))
		return bgr_mss_roi_screen_shot

	def _get_roi_ss(self) -> "(h, w, c) shaped array":
		"""
		:return: game client area screen shot img numpy array w/ shape (h, w, c)
		"""
		if self.mode == "PIL":
			roi_screen_shot = self._get_roi_PIL_ss()
		elif self.mode == "mss":
			roi_screen_shot = self._get_roi_mss_ss()
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
