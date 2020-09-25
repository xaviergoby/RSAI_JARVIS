from abc import ABC, abstractmethod
import numpy as np
from PIL import ImageGrab
import cv2
import settings
from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import keyboard_events_monitoring
from src.utils import time_tools
import datetime


class ABCScreenCaster(ABC):
	
	@abstractmethod
	def __init__(self, keyboard_keys_2_monitor_list):
		self.keyboard_keys_2_monitor_list = keyboard_keys_2_monitor_list
		self.paused = False
		self.current_mouse_states = None
		self.current_keyboard_states = None
		self.grid_handler = None
		self.data_storage_dir = None
		# super().__init__()
	
	@abstractmethod
	def p_keyboard_key_action(self):
		if self.paused is False:
			print("Pausing...")
			self.paused = True
			print("Paused!")
		elif self.paused is True:
			print("Unpausing...")
			self.paused = False
			print("Unaused!")
			
	@abstractmethod
	def t_keyboard_key_action(self):
		cv2.destroyAllWindows()
		
		
	@abstractmethod
	def lmc_action(self):
		raise NotImplementedError


	@abstractmethod
	def set_current_mouse_states(self, mouse_states):
		self.current_mouse_states = mouse_states

	@abstractmethod
	def set_current_keyboard_states(self, keyboard_states):
		self.current_keyboard_states = keyboard_states

	@abstractmethod
	def set_data_storage_dir(self):
		pass

	@abstractmethod
	def set_handler(self):
		pass



	@abstractmethod
	def pre_screen_casting_setup(self):
		self.set_handler()
		self.set_data_storage_dir()
		time_tools.delay_timer(3)
		# Get the current states of the mouse buttons and keyboard keys and set them as the very 1st init
		# mouse & keyboard states
		init_mouse_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
		init_keyboard_states = keyboard_events_monitoring.get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
		self.set_current_mouse_states(init_mouse_states)
		self.set_current_keyboard_states(init_keyboard_states)




	@abstractmethod
	def start_screen_casting(self, roi):

		self.pre_screen_casting_setup()

		while True:
			current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
			printscreen = np.array(ImageGrab.grab(bbox=roi))
			rgb_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
			img_wndw_name = 'Game Client Sreen Cast of region {0}'.format(roi)
			cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)
			cv2.imshow(img_wndw_name, rgb_img)
	

