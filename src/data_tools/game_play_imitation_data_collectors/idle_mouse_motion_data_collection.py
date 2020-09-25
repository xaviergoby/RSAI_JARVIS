import numpy as np
import settings
import pyautogui
from src.data_tools.json_data_toolkit import JSONDataToolKit
from src.data_tools.text_data_toolkit import TextDataToolKit
import os
from research_and_dev.event_driven_system.actuators.actuators_cls import Actuators



class IdleMouseMotionDataCollector:
	
	def __init__(self, data_file_name):
		self.data_file_name = data_file_name
		self.txt_data_file_name = "{0}.txt".format(data_file_name)
		self.json_data_file_name = "{0}.json".format(data_file_name)
		self.txt_data_file_path = os.path.join(settings.MOUSE_MOTION_DATA_DIR, r"idle_mouse_mode_data\{0}".format(self.txt_data_file_name))
		self.json_data_file_path = os.path.join(settings.MOUSE_MOTION_DATA_DIR, r"idle_mouse_mode_data\{0}".format(self.json_data_file_name))
		self.actuator_cls = Actuators()
		self.paused = False
		self.idle_mouse_meta_data_list = []
		
	def start_data_recording(self):
		self.actuator_cls.init_all_states()
		while True:
			# self.sensors_percept = self.bot_sensors_cls.get_sensors_percept()
			# self.bot_sensor_percept_array = self.sensors_percept[0]
			# self.bot_sensors_cls.display_sensor_percept(sensor_percept_array=self.bot_sensor_percept_array)
			if self.paused is False:
				current_idle_mouse_meta_data_list = []
				if self.actuator_cls.lmb_clicked is True:
					print("lmb clicked!")
				elif self.actuator_cls.P_clicked is True:
					self.paused = True
					print("paused...")
				
			elif self.paused is True:
				if self.actuator_cls.P_clicked is True:
					print("unpaused...")
					self.paused = False
					
			self.actuator_cls.update_all_states()
		
		# self.actuator_cls.init_all_states()
		# while self.paused is False:
		# 	if self.actuator_cls.P_clicked is True:
		#
		# 	self.actuator_cls.init_all_states()
		