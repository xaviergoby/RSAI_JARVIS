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
from src.ui_automation_tools.hardware_states_listener_old import HardWareStatesListener
from src.utils import image_processing_tools
# from src.utils.image_processing_tools import draw_sq_grid_lines_on_img_v1

nav_grid = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[1])
def screen_caster(roi):
	# keyboard_keys_2_monitor_list = ["P", "T"]

	# nav_grid = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[1])
	# traj_scene_data_handler = trajectory_scene_data_handler.TrajectorySceneDataHandler()

	data_storage_dir = os.path.join(settings.DATA_DIR, r"end_2_end_slam_data\test_run_data")
	time_tools.delay_timer(3)
	# Setting paused as False in the very begining before the while loop will result in the program immediately running
	# after the delay_timer(s) has return control after s # of seconds. So any H/W state changes will start being
	# registered after s # of seconds.
	paused = False
	# Get the current states of the mouse buttons and keyboard keys and set them as the very 1st init
	# mouse & keyboard states
	# init_mouse_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
	# init_keyboard_states = keyboard_events_monitoring.get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
	hw_states_listener = HardWareStatesListener()
	hw_states_listener.init_all_states()
	# Infinite loop
	while True:
		current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		printscreen = np.array(ImageGrab.grab(bbox=roi))
		rgb_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
		img_wndw_name = 'Game Client Sreen Cast of region {0}'.format(roi)
		# cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)
		cv2.namedWindow(img_wndw_name, cv2.WINDOW_AUTOSIZE)
		# cv2.imshow(img_wndw_name, rgb_imgs)

		rgb_img_copy = rgb_img.copy()
		grid_lines_rgb_colour_code = (0, 0, 0)
		px_x_axes_pnts_int_list = nav_grid.px_x_axes_pnts.astype(int).tolist()
		px_y_axes_pnts_int_list = nav_grid.px_y_axes_pnts.astype(int).tolist()

		# grid_overlayed_rgb_img = image_processing_tools.draw_sq_grid_lines_on_img_v1(rgb_img_copy, px_x_axes_pnts_int_list,
		#                                                                              px_y_axes_pnts_int_list, grid_lines_rgb_colour_code)

		grid_pnts_overlayed_rgb_img = image_processing_tools.draw_sq_grid_points(rgb_img_copy, px_x_axes_pnts_int_list,
		                                                                         px_y_axes_pnts_int_list)

		current_mouse_pos_coords = pyautogui.position()
		current_mouse_x = current_mouse_pos_coords[0] - 8
		current_mouse_y = current_mouse_pos_coords[1] - 31
		current_mouse_pos_color = (0, 0, 255)
		current_mouse_pos_radius = 5
		current_mouse_pos_thickness = -2
		grid_pnts_overlayed_rgb_img = cv2.circle(grid_pnts_overlayed_rgb_img, (current_mouse_x, current_mouse_y),
		                                         current_mouse_pos_radius, current_mouse_pos_color, current_mouse_pos_thickness)

		# grid_overlayed_rgb_img = cv2.circle(grid_overlayed_rgb_img, (current_mouse_x, current_mouse_y),
		#                                     current_mouse_pos_radius, current_mouse_pos_color, current_mouse_pos_thickness)

		# image = cv2.circle(image, (current_mouse_x,current_mouse_y), radius = 0, (255, 0, 0), -1)
		cv2.imshow(img_wndw_name, grid_pnts_overlayed_rgb_img)
		# cv2.imshow(img_wndw_name, grid_overlayed_rgb_img)
		# print(f"\nrgb_img_copy.shape: {rgb_img_copy.shape}")
		# print(f"grid_overlayed_rgb_img.shape: {grid_overlayed_rgb_img.shape}")
		# print(f"len(px_x_axes_pnts_int_list): {len(px_x_axes_pnts_int_list)}")
		# print(f"px_x_axes_pnts_int_list: {px_x_axes_pnts_int_list}")
		# print(f"px_y_axes_pnts_int_list: {px_y_axes_pnts_int_list}")

		# Get the states of the mouse and the keyboard at the very start of each iteration/loop/time step
		# mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_mouse_states,
		#                                                                     settings.mouse_nVirtKey_dict)
		# keyboard_click_events = keyboard_events_monitoring.get_keyboard_click_events(init_keyboard_states,
		#                                                                              settings.keyboard_nVirtKey_dict)

		# Check to see
		# mouse_events = mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"])
		# keyboard_events = keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events, ["P", "T"])

		#################################### IF GAME IS UNPAUSED ####################################
		if paused is False:
			lmc_mouse_screen_pos = pyautogui.position()
			# if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
			if hw_states_listener.lmb_clicked is True:
				# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LMB CLICKED~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
				# task to perform
				lmc_px_x, lmc_px_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
				grid_pnt_x, grid_pnt_y = nav_grid.get_lmc_nn_grid_pnt(lmc_px_x, lmc_px_y)

				# traj_scene_data_handler.update_traj_scene_data(rgb_imgs, [grid_pnt_x, grid_pnt_y])

				screen_shot_img_path = os.path.join(data_storage_dir,
				                                    r"images\({0},{1})_{2}.jpg".format(int(grid_pnt_x),
				                                                                       int(grid_pnt_y),
				                                                                       current_datetime))
				meta_data_csv_path = os.path.join(data_storage_dir, r"metadata\meta_data.csv")
				meta_data_csv_data_row = [lmc_px_x, lmc_px_y, int(grid_pnt_x), int(grid_pnt_y),
				                          current_datetime, screen_shot_img_path]
				print(f"lmc_px_x: {lmc_px_x}  &  lmc_px_y: {lmc_px_y}")
				print(f"grid_pnt_x x: {grid_pnt_x}   &   grid_pnt_y: {grid_pnt_y}")
				print(f"rgb_img.shape: {rgb_img.shape}")
				# print(f"grid_overlayed_rgb_img.shape: {grid_overlayed_rgb_img.shape}")
				print(f"\nrgb_img_copy.shape: {rgb_img_copy.shape}")
				# print(f"grid_overlayed_rgb_img.shape: {grid_overlayed_rgb_img.shape}")
				print(f"len(px_x_axes_pnts_int_list): {len(px_x_axes_pnts_int_list)}")
				print(f"px_x_axes_pnts_int_list: {px_x_axes_pnts_int_list}")
				print(f"px_y_axes_pnts_int_list: {px_y_axes_pnts_int_list}")
			# csv_tools.append_list_as_row(meta_data_csv_path, meta_data_csv_data_row)
			# print(rgb_imgs)
			# print(grid_overlayed_rgb_img)
			# cv2.imwrite(screen_shot_img_path, rgb_imgs)
			# cv2.imwrite(screen_shot_img_path, grid_overlayed_rgb_img)
			# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# if keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events, keyboard_keys_2_monitor_list) is True:
			if hw_states_listener.keyboard_clicked is True:
				# keyboard_key_clicked = keyboard_events_monitoring.get_keyboard_key_clicked_str(keyboard_click_events)
				# if keyboard_key_clicked == "P":
				if hw_states_listener.P_clicked is True:
					# print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("P key clicked")
					if paused is False:
						print("Pausing...")
						paused = True
						print("Paused!")
				# elif keyboard_key_clicked == "T":
				elif hw_states_listener.T_clicked is True:
					# print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("T key clicked")
					print("Terminating Screen Casting...")
					cv2.destroyAllWindows()
					break
		##############################  ############################## ##############################

		#################################### IF GAME IS PAUSED ####################################
		elif paused is True:
			# if keyboard_events_monitoring.keyboard_key_clicked(keyboard_click_events, keyboard_keys_2_monitor_list) is True:
			if hw_states_listener.keyboard_clicked is True:
				# keyboard_key_clicked = keyboard_events_monitoring.get_keyboard_key_clicked_str(keyboard_click_events)
				if hw_states_listener.P_clicked is True:
					# print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("P key clicked")
					if paused is True:
						print("Unausing...")
						paused = False
						print("Unaused!")
				# elif keyboard_key_clicked == "T":
				elif hw_states_listener.T_clicked is True:
					# print(f"\nkeyboard_key_clicked: {keyboard_key_clicked}")
					print("T key clicked")
					print("Terminating Screen Casting...")
					cv2.destroyAllWindows()
					break
		##############################  ############################## ##############################

		# init_mouse_states = mouse_events_monitoring.update_mouse_states(init_mouse_states, mouse_click_events)
		# init_keyboard_states = keyboard_events_monitoring.update_keyboard_states(init_keyboard_states, keyboard_click_events)
		hw_states_listener.update_all_states()

		cv2_close_key = cv2.waitKey(1) & 0xFF
		if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
			cv2.destroyAllWindows()
			break


if __name__ == "__main__":
	# import screen_casting_func
	from src.ui_automation_tools import screen_tools

	screen_tools.set_window_pos_and_size()
	roi = screen_tools.get_client_specific_bounding_region_px_coords()  # returns (8, 31, 791, 591)
	screen_caster(roi)
