import subprocess
import pyautogui
import win32gui
import time
import cv2
import numpy as np
import os
from src.ui_automation_tools import screen_tools
from settings import *
# from main import *
# from main import main_run, get_mouse_state, grab_screen, get_window_region

class RuneScapeClass:

	def __init__(self, username, password):
		self.rs_window_name = "RuneScape"
		self.username = username
		self.password = password
		self.data_dir_path = os.path.join(os.getcwd(), r"data\images")
		# self.data_dir_path = os.full_path.join(os.full_path.dirname(os.getcwd()), r"data\images")
		self.mini_map_region = (1455, 24, 464, 382) # (left, top, width, height)
		self.full_screen_region = (0, 25, 1915, 1010) # (left, top, width, height)

	def get_full_img_path_via_img_name(self, name):
		img_data_dir_path = os.path.join(DATA_DIR, "images")
		full_img_path = os.path.join(img_data_dir_path, name)
		return full_img_path

	def launch_rs(self):
		self.rs_exe_subprocess_call_path  = r"C:\ProgramData\Jagex\launcher\rs2client.exe"
		# self.rs_window_name = "RuneScape"
		self.rs_subprocess_called_obj = subprocess.call([self.rs_exe_subprocess_call_path])
		time.sleep(5)
		# self.rs_window_handle_obj = win32gui.FindWindow(None, self.rs_window_name)
		self.rs_client_screen_tl_br_coords = screen_tools.get_client_screen_tl_br_coords(self.rs_window_name)
		self.rs_client_screen_lt_wh = screen_tools.get_client_screen_tl_coord_and_size(self.rs_window_name)
		# self.rs_window_coords = self.get_client_screen_region()
		# self.rs_window_coords = win32gui.GetWindowRect(self.rs_window_handle_obj)

	def login(self):
		pyautogui.typewrite(self.username+"\n", interval=0.1)
		pyautogui.typewrite(self.password+"\n", interval=0.1)

	def locate_and_click_on_play_btn(self):
		# self.get_full_img_path_via_img_name('in_game_world_screen_shot.png')
		x, y = pyautogui.locateCenterOnScreen(self.get_full_img_path_via_img_name('play_now_btn.PNG'))
		pyautogui.click(x, y)

	def launch_login_and_play_rs(self):
		self.launch_rs()
		time.sleep(8)
		self.login()
		time.sleep(8)
		self.locate_and_click_on_play_btn()
		# self.locate_and_click_on_btn('play_now_btn.PNG')

	def open_map(self):
		pyautogui.keyDown('m')
		pyautogui.keyUp('m')

	def close_map(self):
		pyautogui.keyDown("esc")
		pyautogui.keyUp("esc")

	def set_map_marker(self, img_file_path):
		x, y = pyautogui.locateCenterOnScreen(img_file_path)
		pyautogui.click(x, y, clicks=2, interval=0.25)

	def set_and_recentre_map_on_marker(self, img_file_path):
		self.set_map_marker(img_file_path)
		pyautogui.click()

	def mini_map_img_template_coords_match(self, mini_map_template_img_path, confidence=0.6,
	                                       threshold=.08, mini_map_screen_shot_img_name="mini_map_screen_shot.png"):
		"""

		:param mini_map_template_img_path: e.g. "Blue_Arrow7.png"
		:param confidence: 0.6 by def
		:return: x and local_y coords of template img if found else False
		"""
		pyautogui.screenshot(self.get_full_img_path_via_img_name(mini_map_screen_shot_img_name), region=self.mini_map_region)
		mini_map_screen_shot_img = cv2.imread(self.get_full_img_path_via_img_name(mini_map_screen_shot_img_name))
		mini_map_template_img = cv2.imread(mini_map_template_img_path)
		template_matching_result = cv2.matchTemplate(mini_map_screen_shot_img, mini_map_template_img, cv2.TM_CCOEFF_NORMED)
		threshold = threshold
		loc = np.where(template_matching_result >= threshold)
		if len(loc[0]) > 0:
			template_img_loc = pyautogui.locateOnScreen(mini_map_template_img_path, confidence=confidence, region=self.mini_map_region)
			if template_img_loc is None:
				return False
			elif template_img_loc is not None:
				x = template_img_loc[0]
				y = template_img_loc[1]
				return x, y
		return False

	def mini_map_img_template_coords_match_recursion(self, mini_map_template_img_path, confidence=0.6, threshold=.08):
		img_template_coords_match_result = self.mini_map_img_template_coords_match(mini_map_template_img_path,
		                                                                           confidence=confidence, threshold=threshold)

		while img_template_coords_match_result is False:
			print("not found")
			img_template_coords_match_result = self.mini_map_img_template_coords_match(mini_map_template_img_path,
			                                                                           confidence=confidence, threshold=threshold)

		print("found")
		x, y = img_template_coords_match_result
		pyautogui.click(x, y)


	def in_game_world_img_template_coords_matching(self, main_game_ui_template_img_path,
	                                               confidence=0.6, threshold=.08):
		pyautogui.screenshot(self.get_full_img_path_via_img_name('in_game_world_screen_shot.png'), region=self.full_screen_region)
		in_game_world_screen_shot_img = cv2.imread(self.get_full_img_path_via_img_name('in_game_world_screen_shot.png'))
		in_game_world_template_img = cv2.imread(main_game_ui_template_img_path)
		template_matching_result = cv2.matchTemplate(in_game_world_screen_shot_img, in_game_world_template_img, cv2.TM_CCOEFF_NORMED)
		threshold = threshold
		loc = np.where(template_matching_result >= threshold)
		if len(loc[0]) > 0:
			template_img_loc = pyautogui.locateOnScreen(main_game_ui_template_img_path,
			                                            confidence=confidence, region=self.full_screen_region)
			if template_img_loc is None:
				return False
			elif template_img_loc is not None:
				x = template_img_loc[0]
				y = template_img_loc[1]
				return x, y
		return False

	def in_game_world_img_template_coords_match_recursion(self, main_game_ui_template_img_path,
	                                                      confidence=0.6, threshold=.08):
		img_template_coords_match_result = self.in_game_world_img_template_coords_matching(main_game_ui_template_img_path,
		                                                                                   confidence=confidence, threshold=threshold)
		while img_template_coords_match_result is False:
			print("not found")
			img_template_coords_match_result = self.in_game_world_img_template_coords_matching(main_game_ui_template_img_path,
			                                                                                   confidence=confidence, threshold=threshold)
		print("found")
		x, y = img_template_coords_match_result
		pyautogui.click(x, y)





# rs1 = RuneScapeClass("xaviergoby", "keyboard")
# rs1.launch_login_and_play_rs()
# time.sleep(5)
# main_run("RuneScape")
# if __name__ == "__main__":


	# rs1 = RuneScapeClass("xaviergoby", "keyboard")
	# rs1.launch_login_and_play_rs()
	# time.sleep(5)
	# main_run('RuneScape')
	# time.sleep(6)
	# rs1.open_map()
	# time.sleep(4)
	# rs1.set_and_recentre_map_on_marker("grand_exchange_map_label.PNG")
	# time.sleep(4)
	# rs1.close_map()
	# time.sleep(4)
	# rs1.mini_map_img_template_coords_match_recursion("Blue_Arrow7.png")
	# rs1.in_game_world_img_template_coords_match_recursion("grand_exchange_clerk_3.PNG", confidence=0.7)