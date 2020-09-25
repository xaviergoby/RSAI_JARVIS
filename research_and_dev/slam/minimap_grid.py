import numpy as np
from research_and_dev.slam import minimap_square



class MiniMapGrid:

	# current_wg_coords = 3216, 3219

	def __init__(self, current_world_grid_coords=(3216, 3219), mm_radius_sq_len=10):
		self.current_world_grid_coords = current_world_grid_coords
		self.mm_radius_sq_len = mm_radius_sq_len  # i.e. 10 (true osrs mini_map square-length radius is 10)

		self.mm_side_sq_len = 1 + self.mm_radius_sq_len * 2
		self.grid_leftmost_cell_x = - self.mm_radius_sq_len
		self.grid_topmost_cell_y = - self.mm_radius_sq_len
		self.grid_righttmost_cell_x = self.mm_radius_sq_len
		self.grid_bottomtmost_cell_y = self.mm_radius_sq_len

		self.cells_coords_list = []
		self.grid_coords_cell_objs_key_value_pair_dict = {}

		self.mm_valid_sq_x_coords_list = list(range(self.grid_leftmost_cell_x, self.grid_righttmost_cell_x + 1))
		self.mm_valid_sq_y_coords_list = list(range(self.grid_topmost_cell_y, self.grid_bottomtmost_cell_y + 1))

		# self.mm_grid_cell_rows_range_list = self.mm_valid_sq_x_coords_list
		# self.mm_grid_cell_cols_range_list = self.mm_valid_sq_y_coords_list

		# self.mm_grid_num_rows = self.mm_side_sq_len
		# self.mm_grid_num_cols = self.mm_side_sq_len

		self.grid_array_shape = (self.mm_side_sq_len, self.mm_side_sq_len, 2)



	def create_mm_grid_cells_coords(self):
		"""
		:return:None
		"""
		cells_coords_list = []
		if len(self.cells_coords_list) == 0 and len(self.grid_coords_cell_objs_key_value_pair_dict) == 0:
			for mm_grid_row_idx, mm_local_grid_x in enumerate(self.mm_valid_sq_x_coords_list):
				self.cells_coords_list.append([])
				cells_coords_list.append([])
				for mm_local_grid_y in self.mm_valid_sq_y_coords_list:
					self.cells_coords_list[mm_grid_row_idx].append([mm_local_grid_x, mm_local_grid_y])
					cells_coords_list[mm_grid_row_idx].append([mm_local_grid_x, mm_local_grid_y])
					mm_global_grid_x_coord = self.current_world_grid_coords[0] + mm_local_grid_x # //TODO
					mm_global_grid_y_coord = self.current_world_grid_coords[1] + mm_local_grid_x # //TODO
					mm_grid_cell_x_y_obj_inst = minimap_square.MiniMapSquare(mm_local_grid_x, mm_local_grid_y)
					mm_grid_cell_x_y_coords = (mm_local_grid_x, mm_local_grid_y)
					self.grid_coords_cell_objs_key_value_pair_dict[mm_grid_cell_x_y_coords] = mm_grid_cell_x_y_obj_inst


	def reshape_cells_coords_list_to_array(self):
		"""
		:return:
		"""
		x = np.reshape(self.cells_coords_list, self.grid_array_shape)
		return x


	def convert_mouse_click_screen_coords_2_mm_local_grid_coords(self, screen_mouse_click_x, screen_mouse_click_y):
		mm_mouse_click_x = (screen_mouse_click_x - 708) // 4
		mm_mouse_click_y = (screen_mouse_click_y - 114) // 4
		return mm_mouse_click_x, mm_mouse_click_y


	def compute_observable_boundary_region_coords(self): #//TODO What the hell was this function for?
		leftmost_obs_x = self.current_world_grid_coords[0] - self.mm_radius_sq_len // 2
		topmost_obs_y = self.current_world_grid_coords[1] + self.mm_radius_sq_len // 2
		rightmost_obs_x = self.current_world_grid_coords[0] + self.mm_radius_sq_len // 2
		bottommost_obs_y = self.current_world_grid_coords[1] - self.mm_radius_sq_len // 2
		return leftmost_obs_x, topmost_obs_y, rightmost_obs_x, bottommost_obs_y


	def get_world_grid_coords_from_mouse_click_coords(self, mouse_click_coords):
		current_world_grid_coords = self.current_world_grid_coords
		mouse_click_x, mouse_click_y_coord = mouse_click_coords[0], mouse_click_coords[1]
		mm_mouse_click_x, mm_mouse_click_y_coord = self.convert_mouse_click_screen_coords_2_mm_local_grid_coords(mouse_click_x, mouse_click_y_coord)
		mouse_click_world_grid = current_world_grid_coords[0] + mm_mouse_click_x, current_world_grid_coords[1] - mm_mouse_click_y_coord
		return mouse_click_world_grid


	def update_current_world_grid_coords(self, mouse_click_world_grid):
		self.current_world_grid_coords = mouse_click_world_grid[0], mouse_click_world_grid[1]