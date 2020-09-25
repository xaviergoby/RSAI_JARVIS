import numpy as np
from PIL import ImageGrab
import cv2
import settings
from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import keyboard_events_monitoring
import pyautogui
from src.utils import time_tools
import os
import datetime
from research_and_dev.end2end_nav.handlers import nav_grid_handler
from research_and_dev.end2end_nav.handlers import trajectory_data_handler
from src.utils import csv_tools
from src.ui_automation_tools.hardware_states_listener_old import HardWareStatesListener
from src.utils import image_processing_tools
# from src.utils.image_processing_tools import draw_sq_grid_lines_on_img_v1
import tiledb

class BotNavigator:

	def __init__(self, grid_opt=1, data_dir_name="test_run_data", mouse_buttons_2_monitor="LMB",
	             keyboard_keys_2_monitor=settings.keyboard_nVirtKey_dict_keys):
		self.grid_opt = grid_opt
		self.data_dir_name = data_dir_name
		self.mouse_buttons_2_monitor = [mouse_buttons_2_monitor]
		self.keyboard_keys_2_monitor = keyboard_keys_2_monitor
		self.nav_grid = trajectory_data_handler.TrajectoryDataHandler(self.data_dir_name)
		self.nav_grid = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[self.grid_opt])
		self.hw_states_listener = HardWareStatesListener(self.mouse_buttons_2_monitor, self.keyboard_keys_2_monitor)

if __name__ == "__main__":
	keyboard_keys_2_monitor_list = list(settings.keyboard_nVirtKey_dict.keys())
	nav = BotNavigator( )