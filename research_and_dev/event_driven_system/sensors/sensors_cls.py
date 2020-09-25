from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import keyboard_events_monitoring
from src.ui_automation_tools.hardware_states_listener_old import HardWareStatesListener
from src.utils import image_processing_tools
# from src.utils.image_processing_tools import draw_sq_grid_lines_on_img_v1
import numpy as np
from PIL import ImageGrab
import cv2
import settings
from research_and_dev.event_driven_system.actuators import mouse_event_handler
from research_and_dev.event_driven_system.actuators import keyboard_event_handler
import pyautogui
from src.utils import time_tools
import os
import datetime
from research_and_dev.end2end_nav.handlers import nav_grid_handler
from src.utils import csv_tools
from src.ui_automation_tools import screen_tools




class Sensors:
	
	def __init__(self, roi=None, data_storage_dir_name="test_run_data"):
		self.roi = screen_tools.get_client_specific_bounding_region_px_coords() if roi is None else roi

	
	def get_sensor_percept_array(self):
		sensor_percept_array = np.array(ImageGrab.grab(bbox=self.roi))
		return sensor_percept_array
	
	
	def get_sensors_percept(self):
		sensor_percept_array = np.array(ImageGrab.grab(bbox=self.roi))
		sensor_percept_rgb_img = cv2.cvtColor(sensor_percept_array, cv2.COLOR_BGR2RGB)
		return sensor_percept_array, sensor_percept_rgb_img
		
		
	def get_sensor_percept_rgb_img(self, sensor_percept_array=None):
		if sensor_percept_array is None:
			sensor_percept_array = self.get_sensor_percept_array()
		else:
			pass
		sensor_percept_rgb_img = cv2.cvtColor(sensor_percept_array, cv2.COLOR_BGR2RGB)
		return sensor_percept_rgb_img
	
		
	def display_sensor_percept(self, sensor_percept_array=None, display_cursor=False):
		img_wndw_name = 'Game Client Sreen Cast of region {0}'.format(self.roi)
		cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)
		if sensor_percept_array is None:
			sensor_percept_array = self.get_sensor_percept_array()
		# else:
		# 	pass
		# sensor_percept_rgb_img = self.get_sensor_percept_rgb_img(sensor_percept_array)
		if display_cursor is True:
			sensor_percept_rgb_img = self.get_sensor_percept_rgb_img(sensor_percept_array)
			sensor_percept_rgb_img_copy = sensor_percept_rgb_img.copy()
			current_mouse_pos_coords = pyautogui.position()
			current_mouse_x = current_mouse_pos_coords[0] - 8
			current_mouse_y = current_mouse_pos_coords[1] - 31
			current_mouse_pos_color = (0, 0, 255)
			current_mouse_pos_radius = 5
			current_mouse_pos_thickness = -2
			sensor_percept_rgb_img_copy = cv2.circle(sensor_percept_rgb_img_copy, (current_mouse_x, current_mouse_y),
			                                           current_mouse_pos_radius, current_mouse_pos_color,
			                                           current_mouse_pos_thickness)
			return cv2.imshow(img_wndw_name, sensor_percept_rgb_img_copy)
		# else:
		# 	pass
		# print(f"sensor_percept_rgb_img.shape: {sensor_percept_rgb_img.shape}")
		# img_wndw_name = 'Game Client Sreen Cast of region {0}'.format(self.roi)
		# cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)
		sensor_percept_rgb_img = self.get_sensor_percept_rgb_img(sensor_percept_array)
		return cv2.imshow(img_wndw_name, sensor_percept_rgb_img)
		
	def end_bot_sensors_percept(self):
		cv2_close_key = cv2.waitKey(1) & 0xFF
		if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
			cv2.destroyAllWindows()


