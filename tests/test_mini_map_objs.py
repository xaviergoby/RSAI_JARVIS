from research_and_dev.misc.mini_map_objs import MiniMapGrid
import numpy as np

if __name__ == "__main__":
	rad = 10
	# grid_side_pxs_length = int(1 + (mm_rad_sq_len * 2))
	grid_side_pxs_length = 21
	mm = MiniMapGrid(grid_side_pxs_length=grid_side_pxs_length)
	# mm = MiniMapGrid(mm_rad_sq_len=mm_rad_sq_len)
	mm.create_mm_grid_cells_coords()
	# print("mm.cells_coords_list: {0}".format(mm.cells_coords_list))
	print("mm.cells_coords_list len: {0}".format(len(mm.cells_coords_list)))
	print("mm.cells_coords_list[0] len: {0}".format(len(mm.cells_coords_list[0])))
	x = mm.reshape_cells_coords_list_to_array(mm.cells_coords_list, (21, 21, 2))
	# print("mm.cells_coords_list reshaped: {0}".format(local_x))
	print("mm.cells_coords_list reshaped shape: {0}".format(x.shape))
	print("mm.cells_coords_list reshaped len: {0}".format(x.size))
	# print("local_x: {0}".format(local_x))
	mm_coords = mm.get_mm_coords_from_mouse_click_coords(726, 110)
	print(f"mm_coords: {mm_coords}")
	# print("Screen mouse location coords: {0}\nMini map grid location coords: {1}".format())

	print("mm_side_sq_len: {0}".format(mm.mini_map_square_grid_square))
	print("grid_leftmost_cell_x: {0}".format(mm.grid_leftmost_cell_x_coord))
	print("grid_topmost_cell_y: {0}".format(mm.grid_topmost_cell_y_coord))
	print("grid_righttmost_cell_x: {0}".format(mm.grid_righttmost_cell_x_coord))
	print("grid_bottomtmost_cell_y: {0}".format(mm.grid_bottomtmost_cell_y_coord))
	# print("grid_coords_cell_objs_key_value_pair_dict: {0}".format(mm.grid_coords_cell_objs_key_value_pair_dict))
	print(mm.grid_coords_cell_objs_key_value_pair_dict[(-rad, 0)].left_most_px)
	print(mm.grid_coords_cell_objs_key_value_pair_dict[(0, -rad)].top_most_px)
	print(mm.grid_coords_cell_objs_key_value_pair_dict[(rad, 0)].right_most_px)
	print(mm.grid_coords_cell_objs_key_value_pair_dict[(0, rad)].bottom_most_px)

	mm_left = mm.grid_coords_cell_objs_key_value_pair_dict[(-rad, 0)].left_most_px
	mm_top = mm.grid_coords_cell_objs_key_value_pair_dict[(0, -rad)].top_most_px
	mm_right = mm.grid_coords_cell_objs_key_value_pair_dict[(rad, 0)].right_most_px
	mm_bottom = mm.grid_coords_cell_objs_key_value_pair_dict[(0, rad)].bottom_most_px

	width = mm_right - mm_left
	height = mm_bottom - mm_top

	import pyautogui
	from src.ui_automation_tools import screen_tools
	import settings
	import time
	import cv2
	from PIL import ImageGrab
	import hw_input_output_tools


	def test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
	                                 window_name=settings.GAME_WNDW_NAME):
		return screen_tools.set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
		                                            wndw_name=settings.GAME_WNDW_NAME)


	test_set_window_pos_and_size()
	time.sleep(2)
	mm_screen_region = (mm_left, mm_top, width + 1, height + 1)
	mm_screen_dims = (mm_left, mm_top, mm_right + 1, mm_bottom + 1)

	img_width = mm_right + 1 - mm_left
	img_height = mm_bottom + 1 - mm_top
	og_dim = (img_width, img_height)

	print(f"mm_screen_region: {mm_screen_region}")
	print(f"mm_screen_dims: {mm_screen_dims}")
	init_key_states = hw_input_output_tools.get_init_key_states(settings.mouse_nVirtKey_dict)
	print("Initial mm.current_wg_coords: {0}".format(mm.current_world_grid_coords))
	print("Initial screen coords pyautogui.position(): {0}".format(pyautogui.position()))
	Origin_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(3, 9)]
	print("Origin_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(3, 9)]: {0}".format(Origin_cell))
	print("Origin_cell local_x, local_y: {0}, {1}".format(Origin_cell.x, Origin_cell.y))
	# grid_coords_cell_objs_key_value_pair_dict = mm.grid_coords_cell_objs_key_value_pair_dict
	# print("grid_coords_cell_objs_key_value_pair_dict: {0}".format(grid_coords_cell_objs_key_value_pair_dict.keys()))
	while True:
		printscreen = np.array(ImageGrab.grab(bbox=mm_screen_dims))
		rgb_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
		grey_scale = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)

		og_dim_display_img = grey_scale

		scale_percent = 220  # percent of original size
		new_width = int(img_height * scale_percent / 100)
		new_height = int(img_width * scale_percent / 100)
		new_dim = (new_width, new_height)
		resized = cv2.resize(og_dim_display_img, new_dim, interpolation=cv2.INTER_AREA)

		# w/ threshold1 = 190 other players are represented by a reasonable shape made of pixels!
		ret, thresholded_img = cv2.threshold(og_dim_display_img, 190, 255, cv2.THRESH_BINARY)

		display_img = thresholded_img

		img_wndw_name = 'Mini-map screen shot'
		cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)

		cv2.imshow(img_wndw_name, display_img)

		# coords = pyautogui.position()
		mouse_click_events = hw_input_output_tools.get_mouse_click_events(init_key_states, settings.mouse_nVirtKey_dict)
		if hw_input_output_tools.mouse_clicked(mouse_click_events, ["LMB"]) is True:
			coords = pyautogui.position()
			print("\nMouse Click Event Detected")
			clicked_mouse_button = hw_input_output_tools.get_mouse_button_clicked_tag(mouse_click_events)
			print("Mouse Button Clicked: {0}".format(clicked_mouse_button))
			print("{0} Click Location Coordinates: {1}".format(clicked_mouse_button, coords))
			# wm_grid = mm.get_mm_coords_from_mouse_click_coords(coords[0], coords[1])
			mouse_click_world_grid = mm.get_world_grid_coords_from_mouse_click_coords(coords)
			world_map_grid_displacement = mm.convert_mm_mouse_scrn_coords_to_wm_grid_coords(coords[0], coords[1])
			grid_x = world_map_grid_displacement[0]
			grid_y = world_map_grid_displacement[1]
			print(
				"Screen Mouse Click Position Coords: {0}, {1}\nWorld Map Grid Location Coords Mapping: {2}, {3}".format(
					coords[0],
					coords[1],
					grid_x,
					grid_y))
			mm.update_current_world_map_grid_loc_coords(mouse_click_world_grid)
			mm.update_mini_map_sqaure_obj_instance_grid_coords()
			# init current_wg_coords is = 3216, 3219
			print("World map grid coords: {0}, {1}".format(mouse_click_world_grid[0], mouse_click_world_grid[1]))
			print("Current grid coords loc: {0}".format(mouse_click_world_grid))
			print("Updating LMB & RMB initial key states...\n")
			init_key_states = hw_input_output_tools.update_init_key_states(init_key_states, mouse_click_events)
		else:
			pass
		# print("No Click Event Detected")
		# cv2.imshow(img_wndw_name, cv2.cvtColor(display_img, cv2.COLOR_GRAY2RGB))
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.imwrite("altered_mm_img_{0}_{1}.PNG".format(display_img.shape[0], display_img.shape[1]), display_img)
			pyautogui.screenshot("og_mm_img_{0}_{1}.PNG".format(img_width, img_height), region=mm_screen_region)
			cv2.destroyAllWindows()
			break
