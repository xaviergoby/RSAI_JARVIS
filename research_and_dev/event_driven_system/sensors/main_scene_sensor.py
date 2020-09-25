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


class MainSceneSensor:
	
	def __init__(self, keyboard_keys_2_monitor_list, mesh_grid_opt=settings.MESH_GRID_OPTIONS[1],
	             data_storage_dir_name="test_run_data"):
		self.keyboard_keys_2_monitor_list = keyboard_keys_2_monitor_list
		self.mesh_grid_opt = mesh_grid_opt
		self.data_storage_dir_name = data_storage_dir_name
		self.data_storage_dir = os.path.join(settings.DATA_DIR,
		                                     r"end_2_end_slam_data\{0}".format(self.data_storage_dir_name))
		
		self.grid = nav_grid_handler.NavigationGridHandler(self.mesh_grid_opt)
		
		self.paused = False

	
