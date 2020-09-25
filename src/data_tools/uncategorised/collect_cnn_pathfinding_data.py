from src.path_manipulation_tools import file_path_tools
from src.ui_automation_tools.mouse_events_monitoring import *
import time
# from ui_automation_tools.screen_tools import grab_screen_v2


class CollectCNNPathFindingData:

	def __init__(self):
		self.training_data = []
		self.training_cnt = 0
		self.last_time = time.time()


	def gen_task_data(self, task_name, region=None):
		"""
		:param task_name: e.g. "lumbridge_to_bridge"
		:param region: RuneScapeClass.rs_client_screen_tl_br_coords
		"region" <==> "bbox"   -    (left, top, right, bottom)
		:return:
		"""
		np_arrays_dir_path = os.path.join(DATA_DIR, r"raw\path_finding\{0}\np_arrays".format(task_name))
		images_dir_path = os.path.join(DATA_DIR, r"raw\path_finding\{0}\images".format(task_name))
		if file_path_tools.get_last_data_file_name(np_arrays_dir_path) is False:
			img_idx = 0
		else:
			latest_img_file = file_path_tools.get_last_data_file_name(np_arrays_dir_path)
			latest_img_idx = int(latest_img_file.split("_")[-1][:-4])
			img_idx = latest_img_idx

		delay_seconds = 5
		print("You may start in...")
		for delay_sec in range(delay_seconds, 0, -1):
			print("{0} seconds".format(delay_sec))
			time.sleep(1)
		print("Start!")

		paused = False
		init_key_states = get_init_mouse_states(mouse_nVirtKey_dict)
		while True:
			printscreen = np.array(ImageGrab.grab(bbox=region))
			# print('loop took {} seconds'.format(time.time() - last_time)) # NOTE: KEEP THIS COMMENT, IT CAN BE USEFULL
			last_time = time.time()
			cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))

			if not paused:
				coords = pyautogui.position()
				mouse_click_events = get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)

				# screen = grab_screen_v2(region=region)     # cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
				# screen = np.array(ImageGrab.grab(bbox=region))
				# cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
				cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)

				key_output = key_check()

				if mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
					time.sleep(0.4)
					screen = np.array(ImageGrab.grab(bbox=region))
					click_coords = list(pyautogui.position())
					click_coords_str = "_".join([str(coord) for coord in coords])
					img_full_path = os.path.join(images_dir_path, "{0}_path_img_{1}.jpg".format(task_name, click_coords_str))
					cv2.imwrite(img_full_path, cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY))
					mouse_button_clicked = get_mouse_button_clicked_str(mouse_click_events)
					init_key_states = update_mouse_states(init_key_states, mouse_click_events)
					# output = coords
					self.training_data.append([cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY), click_coords])
					self.training_cnt = self.training_cnt + 1
					print("Total number of client screenshot images captured: {0}".format(self.training_cnt))
					# if len(self.training_data) == 10:
					img_array_full_path = os.path.join(np_arrays_dir_path, "{0}_path_img_{1}".format(task_name, click_coords_str))
					np.save(img_array_full_path, self.training_data)
					print('SAVED (img_idx){0}, Session total (training_cnt): {1}'.format(img_idx, self.training_cnt))
					self.training_data = []
					img_idx = img_idx + 1
					key_output = key_check()


			keys = key_check()

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
					# init_key_states = update_mouse_states(init_key_states, mouse_click_events)
					print('unpaused!')
					time.sleep(1)
				else:
					print('Pausing!')
					paused = True
					time.sleep(1)

			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break




	def gen_mini_map_data(self, region=None):
		pass

if __name__ == "__main__":
	import numpy as np
	import cv2
	from src.ui_automation_tools import screen_tools
	import win32gui
	from PIL import ImageGrab


	# win_name = "Old School RuneScape"
	win_name = "RuneLite - PolarHobbes"
	hwnd = win32gui.FindWindow(None, win_name)
	# wndw_x_wrt_screen = 0  # -8
	wndw_x_wrt_screen = -3  # -8
	# wndw_y_wrt_screen = 0  # -31
	wndw_y_wrt_screen = -26  # -31
	wndw_width_in_screen = 800 + 4 + 4
	# wndw_width_in_screen = 800
	wndw_height_in_screen = 600 + 4 + 27
	screen_tools.set_window_pos_and_size(hwnd=None, x_new=wndw_x_wrt_screen, y_new=wndw_y_wrt_screen,
	                                     new_width=wndw_width_in_screen, new_height=wndw_height_in_screen,
	                                     wndw_name=win_name)

	client_rect_pos_n_size = win32gui.GetClientRect(hwnd)
	print("client_rect_pos_n_size: {0}".format(client_rect_pos_n_size))
	wndw_left_border_pxs_width = 8
	wndw_top_border_pxs_height = 31
	client_area_width = wndw_width_in_screen - 8
	client_area_height = wndw_height_in_screen - 8
	client_region = (wndw_left_border_pxs_width, wndw_top_border_pxs_height, client_area_width, client_area_height)
	print("grab_screen_v3: {0}".format(screen_tools.grab_screen_v3()))
	print("get_client_screen_tl_coord_and_size: {0}".format(screen_tools.get_client_screen_tl_coord_and_size(win_name)))
	print("get_client_screen_tl_br_coords: {0}".format(screen_tools.get_client_screen_tl_br_coords(win_name)))
	print("get_window_screen_tl_br_coords: {0}".format(screen_tools.get_window_screen_tl_br_coords(win_name)))
	print("client_region: {0}".format(client_region))

	# mm_left_x = 584
	# mm_top_y = wndw_top_border_pxs_height
	# mm_width = client_area_width
	# mm_height = 190 + 8
	# mm_region = (mm_left_x, mm_top_y, mm_width, mm_height)

# rs1 = rs_class.RuneScapeClass("xaviergoby", "keyboard")
	# rs1.launch_login_and_play_rs()
	# print("Wait 10 seconds...")
	# time.sleep(10)
	# print("You can start now!")
	# bbox_region = (0, 40, 800, 640)  # OG
	# bbox_region = (-7, 0, 700, 500)
	# bbox_region = (1, 31, 918, 689)
	# task_name = "lumbridge_to_bridge"
	# task_name = "wc_tree_lumbridge"
	# CollectCNNPathFindingData().gen_task_data(task_name=task_name, region=client_region)
	# GenClfData().gen_task_data(task_name="wc", region=rs1.rs_client_screen_tl_br_coords)
# main_run("RuneScape", "X")