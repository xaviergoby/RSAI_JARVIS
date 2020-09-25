from src.path_manipulation_tools import file_path_tools
from src.ui_automation_tools import screen_tools
import os
from settings import DATA_DIR, mouse_nVirtKey_dict
import pyautogui
from src.ui_automation_tools import mouse_events_monitoring
# from src.ui_automation_tools.hw_input_output_tools import key_check
import time
import win32gui, win32ui, win32con, win32api
# from ui_automation_tools.hw_input_output_tools import get_mouse_state
from ui_automation_tools.screen_tools import get_client_screen_tl_br_coords, grab_screen
from ui_automation_tools.screen_tools import grab_screen_v2
from game import rs_class
import cv2
import ctypes
import numpy as np
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab


class CollectTaskObjDectTrckData:
	"""
	The data which is being generated, is, in essence, nothing more than screen shots
	of the game as it is being played.
	"""
	task_data_sub_dir_names = ["xml_annots", "images", "np_arrays", "combined"]
	def __init__(self, task_category, task_name=None, main_view=True,
	             mini_map=False, window_name=None,
	             watch_nVirtKey = None, nVirtKey_watch_list = None):
		"""
		NOTE: DISREGARD EVERYTHING BELOW OF THIS AND ABOVE THE ARGS & KWARGS INFO/HELP SECTION ABOUT THIS CLASSES "SINGLE/DUAL" USAGE!!!
		A single class instance of this CollectTaskObjDectTrckData class object should be used per task category. This means that you shouldn't/cannot
		collect data for tasks in different categories. If you do want to do this then you should reinitialise a new class instance of this
		CollectTaskObjDectTrckData class object. For example:
		Allowed:
		slaying = CollectTaskObjDectTrckData("slaying", "cows")
		or
		slaying = CollectTaskObjDectTrckData("slaying", ["cows", "goblins"]
		:param task_category: str of task category dir, e.g. "mining" or "slaying"
		:param task_name: str or list of strs of the task names, e.g. "cows" or "tree", "oak", ["cows", "goblins"]
		:param main_view: boolean of whether to screenshot the entire viewing area of the clients main game view. True by def.
		:param mini_map: boolean of whether to screenshot the mini_map in the top right corner of the game. False by def.
		:param window_name: str of the name of the osrs client window. Is "Old School RuneScape" if left as None.
		:param watch_nVirtKey: the str of the keys of the virtual keys to watch which are present in the var mouse_nVirtKey_dict in cv_nav_settings.py
		:param nVirtKey_watch_list: a list of str's of the keys of the virtual keys to watch which are present in the var mouse_nVirtKey_dict in cv_nav_settings.py
		"""
		self.task_category = task_category
		self.task_name = task_name
		self.main_view = main_view
		self.mini_map = mini_map
		self.window_name = window_name
		self.watch_nVirtKey = watch_nVirtKey
		self.nVirtKey_watch_list = nVirtKey_watch_list
		self.data_save_dir_name = r"pre_bboxed_data\tasks"
		self.training_data = []
		self.training_cnt = 0
		self.current_session_total = 0
		self.init_all_necessary_paths()
		# self.last_time = time.time()

	def setup_window_pos_and_size(self):
		"""
		This function is meant for properly positioning and sizing the game window!
		:return: None
		"""
		if self.window_name is not None:
			screen_tools.set_window_pos_and_size(wndw_name=self.window_name)
		elif self.window_name is None:
			screen_tools.set_window_pos_and_size()


	def init_data_save_dir_path(self):
		r"""
		Instantiates the self.data_Save_dir_path var with the str value r"C:\Users\XGOBY\RSAIBot\data\pre_bboxed_data\tasks"
		:return:None
		"""
		self.data_save_dir_path = os.path.join(DATA_DIR, self.data_save_dir_name)


	def init_task_category_data_save_dir_path(self):
		r"""
		Instantiates the self.task_category_data_save_dir_path var with the e.g. str value r"C:\Users\XGOBY\RSAIBot\data\pre_bboxed_data\tasks\slaying"
		:return:None
		"""
		self.task_category_data_save_dir_path = os.path.join(self.data_save_dir_path, self.task_category)
		file_path_tools.make_dir_if_nonexistent(self.task_category_data_save_dir_path)


	def init_task_names_data_save_dir_paths(self):
		"""
		This class method is meant for initializing all the paths with which the class instance
		will be dealing with. This involves creating a pathlib.Path(<full_path>) class instance for
		each full_path in addition to creating any directories which may not already exist.
		:return: None
		"""
		if isinstance(self.task_name, str):
			self.task_name_data_save_dir_path = os.path.join(self.task_category_data_save_dir_path, self.task_name)
			self.task_image_data_dir_path = os.path.join(self.task_name_data_save_dir_path, "images")
			file_path_tools.make_dir_if_nonexistent(self.task_name_data_save_dir_path)
			file_path_tools.make_dir_if_nonexistent(self.task_image_data_dir_path)
			self.task_image_data_dir_total_files_count = len(file_path_tools.get_dir_contents_list(self.task_image_data_dir_path))


		elif isinstance(self.task_name, list):
			task_name_data_save_dir_path_dict = {}
			for task_name in self.task_name:
				task_name_data_save_dir_path = os.path.join(self.task_category_data_save_dir_path, task_name)
				task_name_data_save_dir_path_dict[task_name] = task_name_data_save_dir_path
				file_path_tools.make_dir_if_nonexistent(task_name_data_save_dir_path)
				file_path_tools.make_dir_if_nonexistent(self.task_image_data_dir_path)
			self.task_name_data_save_dir_path = task_name_data_save_dir_path_dict


	def init_all_necessary_paths(self):
		self.init_data_save_dir_path()
		self.init_task_category_data_save_dir_path()
		self.init_task_names_data_save_dir_paths()

	def update_image_dir_files_current_total(self):
		print(len(file_path_tools.get_dir_contents_list(self.task_image_data_dir_path)))
		self.task_image_data_dir_total_files_count = len(file_path_tools.get_dir_contents_list(self.task_image_data_dir_path))

	def get_most_recent_file_id_code(self, windows_format_full_dir_path):
		most_recent_file_name = file_path_tools.get_most_recent_data_file_name(windows_format_full_dir_path)
		if most_recent_file_name is False:
			img_idx = 0
			return img_idx
		else:
			img_idx = file_path_tools.get_img_file_name_vals(most_recent_file_name)
			return img_idx


	def create_image_file_name(self, img_idx):
		img_file_name = "{0}_{1}_{2}.jpg".format(self.task_category, self.task_name, img_idx)
		return img_file_name


	def create_image_file_full_path(self, img_idx):
		img_file_name = self.create_image_file_name(img_idx)
		img_file_full_path = os.path.join(self.task_image_data_dir_path, img_file_name)
		return img_file_full_path


	def run_task_data_collection(self):
		screen_tools.set_window_pos_and_size()
		most_recent_img_idx = int(self.get_most_recent_file_id_code(self.task_image_data_dir_path))
		img_idx = most_recent_img_idx + 1
		paused = False
		region = screen_tools.get_client_specific_bounding_region_px_coords()
		delay_seconds = 10
		print("You may start in...")
		for delay_sec in range(delay_seconds, 0, -1):
			print("{0} seconds".format(delay_sec))
			time.sleep(1)
		print("Start, recording mouse & keyboard states/events!")
		init_key_states = mouse_events_monitoring.get_init_mouse_states(mouse_nVirtKey_dict)
		while True:
			screen_shot = np.array(ImageGrab.grab(bbox=region))
			cv2.imshow('window', cv2.cvtColor(screen_shot, cv2.COLOR_BGR2RGB))
			if not paused:
				# Check whether any of the mouse buttons/keys being watched have been clicked/triggered
				mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
				if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
					screen = np.array(ImageGrab.grab(bbox=region))
					img_file_full_path = self.create_image_file_full_path(img_idx)
					cv2.imwrite(img_file_full_path, cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
					init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)
					self.current_session_total = self.current_session_total + 1
					self.update_image_dir_files_current_total()
					print("Saved image full_path: {0}".format(img_file_full_path))
					print("Current image files dir total count: {0}".format(self.task_image_data_dir_total_files_count))
					print("Current session images screen shot count: {0}".format(self.current_session_total))
					self.training_data = []
					img_idx = img_idx + 1

			keys = mouse_events_monitoring.key_check()

			if 'T' in keys:
				if paused:
					paused = False
					print('unpaused!')
					time.sleep(1)
				else:
					print('Pausing!')
					paused = True
					self.training_cnt = self.training_cnt - len(self.training_data)
					self.training_data = []
					time.sleep(1)

			if 'P' in keys:
				if paused:
					paused = False
					print('unpaused!')
					time.sleep(1)
				else:
					print('Pausing!')
					paused = True
					time.sleep(1)
				mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
				init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)

			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break




	def gen_mini_map_data(self, region=None):
		pass

if __name__ == "__main__":
	# task_data_collector1 = CollectTaskObjDectTrckData("slaying", "goblins")
	task_data_collector1 = CollectTaskObjDectTrckData("slaying", "cows")
	# task_data_collector1 = CollectTaskObjDectTrckData("slaying", ["cows", "goblins"])
	test_path = r"C:\Users\XGOBY\RSAIBot\data\pre_bboxed_data\tasks\slaying\cows\images"
	task_data_collector1.run_task_data_collection()
