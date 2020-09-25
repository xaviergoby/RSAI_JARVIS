import numpy as np


class MiniMapSquare:

	minimap_px_square_length = 4

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.left_most_px = 708 + self.x * self.minimap_px_square_length
		self.top_most_px = 114 + self.y * self.minimap_px_square_length
		self.right_most_px = 711 + self.x * self.minimap_px_square_length
		self.bottom_most_px = 117 + self.y * self.minimap_px_square_length


class MiniMapGrid:
	current_world_grid_coords = 3216, 3219

	def __init__(self, mini_map_grid_square_length_radius=10):
		self.cells_coords_list = []
		self.grid_coords_cell_objs_key_value_pair_dict = {}
		self.mini_map_grid_square_length_radius = mini_map_grid_square_length_radius # i.e. 10 (true osrs mini_map square-length radius is 10)
		self.mini_map_square_grid_square =  1 + self.mini_map_grid_square_length_radius * 2
		self.grid_leftmost_cell_x_coord = - self.mini_map_grid_square_length_radius
		self.grid_topmost_cell_y_coord = - self.mini_map_grid_square_length_radius
		self.grid_righttmost_cell_x_coord = self.mini_map_grid_square_length_radius
		self.grid_bottomtmost_cell_y_coord = self.mini_map_grid_square_length_radius

		self.mm_grid_cell_x_coords_range_list = list(range(self.grid_leftmost_cell_x_coord, self.grid_righttmost_cell_x_coord + 1))
		self.mm_grid_cell_y_coords_range_list = list(range(self.grid_topmost_cell_y_coord, self.grid_bottomtmost_cell_y_coord + 1))

		self.mm_grid_cell_rows_range_list = self.mm_grid_cell_x_coords_range_list
		self.mm_grid_cell_cols_range_list = self.mm_grid_cell_y_coords_range_list

		self.mm_grid_num_rows = self.mini_map_square_grid_square
		self.mm_grid_num_cols = self.mini_map_square_grid_square


	def create_mm_grid_cells_coords(self):
		"""
		:return:None
		"""
		cells_coords_list = []
		if len(self.cells_coords_list) == 0 and len(self.grid_coords_cell_objs_key_value_pair_dict) == 0:
			for mm_grid_row_idx, mm_grid_x_coord in enumerate(self.mm_grid_cell_x_coords_range_list):
				self.cells_coords_list.append([])
				cells_coords_list.append([])
				for mm_grid_y_coord in self.mm_grid_cell_cols_range_list:
					self.cells_coords_list[mm_grid_row_idx].append([mm_grid_x_coord, mm_grid_y_coord])
					cells_coords_list[mm_grid_row_idx].append([mm_grid_x_coord, mm_grid_y_coord])
					mm_grid_cell_x_y_obj_inst = MiniMapSquare(mm_grid_x_coord, mm_grid_y_coord)
					mm_grid_cell_x_y_coords = (mm_grid_x_coord, mm_grid_y_coord)
					self.grid_coords_cell_objs_key_value_pair_dict[mm_grid_cell_x_y_coords] = mm_grid_cell_x_y_obj_inst


	def reshape_cells_coords_list_to_array(self, cells_coords_list, grid_array_shape):
		"""
		:param cells_coords_list:
		:param grid_array_shape: e.g. (rows, cols, depth) so for mm (2D) w/ a diameter of 25 game square-lengths then (25, 25, 2)
		:return:
		"""
		x = np.reshape(cells_coords_list, grid_array_shape)
		return x


	def get_mm_coords_from_mouse_click_coords(self, mouse_click_x_coord, mouse_click_y_coord):
		mm_mouse_click_x_coord = (mouse_click_x_coord - 708)//4
		mm_mouse_click_y_coord = (mouse_click_y_coord - 114)//4
		return mm_mouse_click_x_coord, mm_mouse_click_y_coord

	def compute_observable_boundary_region_coords(self):
		leftmost_obs_x = self.current_world_grid_coords[0] - self.mini_map_grid_square_length_radius//2
		topmost_obs_y = self.current_world_grid_coords[1] + self.mini_map_grid_square_length_radius//2
		rightmost_obs_x = self.current_world_grid_coords[0] + self.mini_map_grid_square_length_radius//2
		bottommost_obs_y = self.current_world_grid_coords[1] - self.mini_map_grid_square_length_radius//2
		return leftmost_obs_x, topmost_obs_y, rightmost_obs_x, bottommost_obs_y

	def get_world_grid_coords_from_mouse_click_coords(self, mouse_click_coords):
		current_world_grid_coords = self.current_world_grid_coords
		mouse_click_x_coord, mouse_click_y_coord = mouse_click_coords[0], mouse_click_coords[1]
		mm_mouse_click_x_coord, mm_mouse_click_y_coord = self.get_mm_coords_from_mouse_click_coords(mouse_click_x_coord, mouse_click_y_coord)
		mouse_click_world_grid = current_world_grid_coords[0] + mm_mouse_click_x_coord, current_world_grid_coords[1] - mm_mouse_click_y_coord
		return mouse_click_world_grid

	def update_current_world_grid_coords(self, mouse_click_world_grid):
		self.current_world_grid_coords = mouse_click_world_grid[0], mouse_click_world_grid[1]


if __name__ == "__main__":
	# mm_rad_sq_len = 10 # OG px mm_rad_sq_len choice
	# mm_rad_sq_len = 14 # max possible
	rad = 6
	mm = MiniMapGrid(mini_map_grid_square_length_radius=rad)
	mm.create_mm_grid_cells_coords()
	x = mm.reshape_cells_coords_list_to_array(mm.cells_coords_list, (rad*2+1, rad*2+1, 2))
	print("x: {0}".format(x))
	mm_coords = mm.get_mm_coords_from_mouse_click_coords(726, 110)
	print(mm_coords)

	print("mm_side_sq_len: {0}".format(mm.mini_map_square_grid_square))
	print("grid_leftmost_cell_x: {0}".format(mm.grid_leftmost_cell_x_coord))
	print("grid_topmost_cell_y: {0}".format(mm.grid_topmost_cell_y_coord))
	print("grid_righttmost_cell_x: {0}".format(mm.grid_righttmost_cell_x_coord))
	print("grid_bottomtmost_cell_y: {0}".format(mm.grid_bottomtmost_cell_y_coord))
	print("grid_coords_cell_objs_key_value_pair_dict: {0}".format(mm.grid_coords_cell_objs_key_value_pair_dict))
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
	from src.ui_automation_tools import mouse_events_monitoring

	def test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
									 window_name=settings.GAME_WNDW_NAME):
		return screen_tools.set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
		                                            wndw_name=settings.GAME_WNDW_NAME)


	test_set_window_pos_and_size()
	time.sleep(2)
	mm_screen_region = (mm_left, mm_top, width+1, height+1)
	mm_screen_dims = (mm_left, mm_top, mm_right+1, mm_bottom+1)

	img_width = mm_right+1 - mm_left
	img_height = mm_bottom+1 - mm_top
	og_dim = (img_width, img_height)

	print(f"mm_screen_region: {mm_screen_region}")
	print(f"mm_screen_dims: {mm_screen_dims}")
	init_key_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
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


		img_wndw_name = 'Mm w/ {0} side px len sq scrnshoot'.format(rad*2+1)
		cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)

		cv2.imshow(img_wndw_name, display_img)

		coords = pyautogui.position()
		mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, settings.mouse_nVirtKey_dict)
		if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
			print("\nMouse Click Event Detected")
			clicked_mouse_button = mouse_events_monitoring.get_mouse_button_clicked_str(mouse_click_events)
			print("Mouse Button Clicked: {0}".format(clicked_mouse_button))
			print("{0} Click Location Coordinates: {1}".format(clicked_mouse_button, coords))
			# wm_grid = mm.get_mm_coords_from_mouse_click_coords(coords[0], coords[1])
			mouse_click_world_grid = mm.get_world_grid_coords_from_mouse_click_coords(coords)
			mm.update_current_world_grid_coords(mouse_click_world_grid)
			# init current_wg_coords is = 3216, 3219
			print("World map grid coords: {0}, {1}".format(mouse_click_world_grid[0], mouse_click_world_grid[1]))
			print("Current grid coords loc: {0}".format(mouse_click_world_grid))
			print("Updating LMB & RMB initial key states...\n")
			init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)
		else:
			pass
			# print("No Click Event Detected")
		# cv2.imshow(img_wndw_name, cv2.cvtColor(display_img, cv2.COLOR_GRAY2RGB))

		if cv2.waitKey(0) & 0xFF == ord('q'):
			cv2.imwrite("altered_mm_img_{0}_{1}.PNG".format(display_img.shape[0], display_img.shape[1]), display_img)
			pyautogui.screenshot("og_mm_img_{0}_{1}.PNG".format(img_width, img_height), region=mm_screen_region)
			cv2.destroyAllWindows()
			break
