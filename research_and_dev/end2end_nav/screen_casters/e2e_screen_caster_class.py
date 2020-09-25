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
from src.utils import csv_tools


class E2EScreenCaster:
	
	def __init__(self, keyboard_keys_2_monitor_list, mesh_grid_opt=settings.MESH_GRID_OPTIONS[1], data_storage_dir_name="test_run_data"):
		self.keyboard_keys_2_monitor_list = keyboard_keys_2_monitor_list
		self.mesh_grid_opt = mesh_grid_opt
		self.data_storage_dir_name = data_storage_dir_name
		self.data_storage_dir = os.path.join(settings.DATA_DIR, r"end_2_end_slam_data\{0}".format(self.data_storage_dir_name))
		
		self.grid = nav_grid_handler.NavigationGridHandler(self.mesh_grid_opt)
		
		self.paused = False
		

def screen_caster(roi):
	keyboard_keys_2_monitor_list = ["P", "T"]
	
	mgrid = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[1])
	# traj_scene_data_handler = trajectory_scene_data_handler.TrajectorySceneDataHandler()
	
	data_storage_dir = os.path.join(settings.DATA_DIR, r"end_2_end_slam_data\test_run_data")
	time_tools.delay_timer(3)
	# Setting paused as False in the very begining before the while loop will result in the program immediately running
	# after the delay_timer(s) has return control after s # of seconds. So any H/W state changes will start being
	# registered after s # of seconds.
	paused = False
	# Get the current states of the mouse buttons and keyboard keys and set them as the very 1st init
	# mouse & keyboard states
	init_mouse_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
	init_keyboard_states = keyboard_events_monitoring.get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
	# hardware_states_handler.init_all_states()
	# Infinite loop
	while True:
		current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		printscreen = np.array(ImageGrab.grab(bbox=roi))
		rgb_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
		img_wndw_name = 'Game Client Sreen Cast of region {0}'.format(roi)
		cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)
		cv2.imshow(img_wndw_name, rgb_img)
		
		# Get the states of the mouse and the keyboard at the very start of each iteration/loop/time step
		mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_mouse_states,
		                                                                    settings.mouse_nVirtKey_dict)
		keyboard_click_events = keyboard_events_monitoring.get_keyboard_click_events(init_keyboard_states,
		                                                                             settings.keyboard_nVirtKey_dict)
		
		# Check to see
		# mouse_events = mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"])
		# keyboard_events = keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events, ["P", "T"])
		if paused is False:
			mouse_screen_pos = pyautogui.position()
			if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
				###################################################################################
				# task to perform
				lmc_px_x, lmc_px_y = mouse_screen_pos[0], mouse_screen_pos[1]
				grid_pnt_x, grid_pnt_y = mgrid.get_lmc_nn_grid_pnt(lmc_px_x, lmc_px_y)
				
				# traj_scene_data_handler.update_traj_scene_data(rgb_imgs, [grid_pnt_x, grid_pnt_y])
				
				screen_shot_img_path = os.path.join(data_storage_dir,
				                                    r"images\({0},{1})_{2}.jpg".format(int(grid_pnt_x),
				                                                                       int(grid_pnt_y),
				                                                                       current_datetime))
				meta_data_csv_path = os.path.join(data_storage_dir, r"metadata\meta_data.csv")
				meta_data_csv_data_row = [lmc_px_x, lmc_px_y, int(grid_pnt_x), int(grid_pnt_y),
				                          current_datetime, screen_shot_img_path]
				csv_tools.append_list_as_row(meta_data_csv_path, meta_data_csv_data_row)
				print(f"lmc_px_x: {lmc_px_x}  &  lmc_px_y: {lmc_px_y}")
				print(f"grid_pnt_x x: {grid_pnt_x}   &   grid_pnt_y: {grid_pnt_y}")
				cv2.imwrite(screen_shot_img_path, rgb_img)
			###################################################################################
			
			if keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events,
			                                                   keyboard_keys_2_monitor_list) is True:
				keyboard_key_clicked = keyboard_events_monitoring.get_keyboard_key_clicked_str(keyboard_click_events)
				if keyboard_key_clicked == "P":
					print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					if paused is False:
						print("Pausing...")
						paused = True
						print("Paused!")
				elif keyboard_key_clicked == "T":
					print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("Terminating Screen Casting...")
					cv2.destroyAllWindows()
					break
		
		
		elif paused is True:
			if keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events,
			                                                   keyboard_keys_2_monitor_list) is True:
				keyboard_key_clicked = keyboard_events_monitoring.get_keyboard_key_clicked_str(keyboard_click_events)
				if keyboard_key_clicked == "P":
					print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					if paused is True:
						print("Unausing...")
						paused = False
						print("Unaused!")
				elif keyboard_key_clicked == "T":
					print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("Terminating Screen Casting...")
					cv2.destroyAllWindows()
					break
		
		init_mouse_states = mouse_events_monitoring.update_mouse_states(init_mouse_states, mouse_click_events)
		init_keyboard_states = keyboard_events_monitoring.update_keyboard_states(init_keyboard_states,
		                                                                         keyboard_click_events)
		
		cv2_close_key = cv2.waitKey(1) & 0xFF
		if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
			cv2.destroyAllWindows()
			break

# if __name__ == "__main__":
#     screen_caster()
