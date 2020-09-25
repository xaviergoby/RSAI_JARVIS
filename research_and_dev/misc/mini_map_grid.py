import numpy as np
# tile_id = 0 MM CENTRE TILE
# mm single tile width in screen coords = [708, 711]
# mm single tile height in screen coords = [114, 117]

# MINIMAP RADIUS FROM TOP TO BOTTOM PNTS IS = [39, 190]
# diameter: 191 - 38 = 151 pixels
# radius: 151 / 2 = 75.5 = 76 pixels
# 4 pixels = 1 square length and so therefore:
# 76 / 4 = 19

# FROM OSRS WIKI
# The mini_map appears as an approximately circular area with a 19 square-length radius
# 1 square-length equals 4 pixels so
# 19 * 4 = 76

# x_pxs_bounded_interval
# y_pxs_bounded_interval

Xis = [3216, 3225, 3234, 3235, 3229, 3223, 3219, 3214]
Yis = [3219, 3219, 3219, 3226, 3233, 3239, 3244, 3245]

def zip_Xis_Yis(Xis, Yis):
	wm_coords = []
	for xi, yi in zip(Xis, Yis):
		wm_coords.append([xi, yi])
	return wm_coords


wm_coords = zip_Xis_Yis(Xis, Yis)



class WorldMapSquare:

	def __init__(self, x, y):
		self.wm_square_x = x
		self.wm_square_y = y


class WorldMapPath:

	def __init__(self, wm_path_coords):

		self.wm_path_coords = wm_path_coords
		self._wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(self.wm_path_coords)

	def compute_wm_path_displacement_vectors_via_wm_coords(self):
		path_wm_origin_x = self.wm_path_coords[0][0]
		path_wm_origin_y = self.wm_path_coords[0][1]
		# path_wm_squares_travelled_to = self.wm_path_coords[0:]
		wm_path_displacement_vectors = []
		# wm_init_square_x = path_wm_origin_x
		# wm_init_square_y = path_wm_origin_y
		for path_points_list_idx, path_point_coords in enumerate(self.wm_path_coords[:-1]):
			departure_path_point = self.wm_path_coords[path_points_list_idx]
			arrival_path_point = self.wm_path_coords[path_points_list_idx + 1]
			dXi = arrival_path_point[0] - departure_path_point[0]
			dYi = arrival_path_point[1] - departure_path_point[1]
			wm_path_displacement_vectors.append([dXi, dYi])

		return wm_path_displacement_vectors


class WorldMapGrid:

	def __init__(self, grid_origin_centre_wm_coords, num_of_grids = 200):
		self.grid_origin_centre_wm_coords = grid_origin_centre_wm_coords
		self.num_of_grids = num_of_grids


	def compute_wm_path_displacement_vectors_via_wm_coords(self, wm_coords):
		path_wm_origin_x = wm_coords[0][0]
		path_wm_origin_y = wm_coords[0][1]
		path_wm_squares_travelled_to = wm_coords[0:]
		wm_path_displacement_vectors = []
		wm_init_square_x = path_wm_origin_x
		wm_init_square_y = path_wm_origin_y
		for path_points_list_idx, path_point_coords in enumerate(wm_coords[:-1]):
			departure_path_point = wm_coords[path_points_list_idx]
			arrival_path_point = wm_coords[path_points_list_idx+1]
			dXi = arrival_path_point[0] - departure_path_point[0]
			dYi = arrival_path_point[1] - departure_path_point[1]
			wm_path_displacement_vectors.append([dXi, dYi])

		return wm_path_displacement_vectors


	def convert_wm_displacement_vectors_to_mm_displacement_vectors(self, wm_coords):
		wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(wm_coords)
		mm_path_displacement_vectors = []
		for wm_displacement_vector in wm_path_displacement_vectors:
			dxi = wm_displacement_vector[0]
			dyi = wm_displacement_vector[1] * -1
			mm_path_displacement_vectors.append([dxi, dyi])

		return mm_path_displacement_vectors


	def compute_mm_path_displacement_vectors_via_wm_coords(self, wm_coords):
		mm_path_displacement_vectors = self.convert_wm_displacement_vectors_to_mm_displacement_vectors(wm_coords)
		pass



class MiniMapSquare:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.left_most_px = 708 + self.x * 4
		self.top_most_px = 114 + self.y * 4
		self.right_most_px = 711 + self.x * 4
		self.bottom_most_px = 117 + self.y * 4


class MiniMapGrid:

	def __init__(self, mini_map_grid_square_length_radius):
		self.cells_coords_list = []
		self.grid_coords_cell_objs_key_value_pair_dict = {}
		self.mini_map_grid_square_length_radius = mini_map_grid_square_length_radius # i.e. 10 (true osrs mini_map square-length radius is 10)
		self.mini_map_square_grid_square =  1 + self.mini_map_grid_square_length_radius * 2
		# self.grid_unit_cell_radius = grid_unit_cell_radius
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


	# def create_grid_cell_x_coord_and_rows_idx_dict(self):
	#
	# 	grid_row_cells_range_list = list(range(0, self.mm_side_sq_len))
	# 	grid_ucd_range_list = self.mm_valid_sq_x_coords_list
	# 	for x_coord, idx in enumerate(grid_ucd_range_list, grid_row_cells_range_list):



	def create_mm_grid(self):
		"""
		:return:
		"""
		if len(self.cells_coords_list) == 0 and len(self.grid_coords_cell_objs_key_value_pair_dict) == 0:
			for mm_grid_row_idx, mm_grid_x_coord in enumerate(self.mm_grid_cell_x_coords_range_list):
				self.cells_coords_list.append([])
				for mm_grid_y_coord in self.mm_grid_cell_cols_range_list:
					# mm_grid_cell_x_y_coords_list = [mm_grid_x_coord, mm_grid_y_coord]
					# mm_grid_cell_x_y_coords = (mm_grid_x_coord, mm_grid_y_coord)
					self.cells_coords_list[mm_grid_row_idx].append([mm_grid_x_coord, mm_grid_y_coord])
					# mm_grid_cell_x_y_coords= (mm_grid_x_coord, mm_grid_y_coord)
					mm_grid_cell_x_y_obj_inst = MiniMapSquare(mm_grid_x_coord, mm_grid_y_coord)
					mm_grid_cell_x_y_coords = (mm_grid_x_coord, mm_grid_y_coord)
					self.grid_coords_cell_objs_key_value_pair_dict[mm_grid_cell_x_y_coords] = mm_grid_cell_x_y_obj_inst

	def create_mm_grid2(self):
		pass



			# mini_map_grid_centre_origin_cell_x_coord = 0
			# mini_map_grid_centre_origin_cell_y_coord = 0
			# mini_map_grid_centre_origin_cell_obj_inst = MiniMapSquare



if __name__ == "__main__":

	mm = MiniMapGrid(mini_map_grid_square_length_radius=10)
	mm.create_mm_grid()
	print(mm.cells_coords_list)
	print(mm.grid_coords_cell_objs_key_value_pair_dict)
	cells_array = np.asarray(mm.cells_coords_list)
	print(cells_array)
	# ells_array[10][10] = [0, 0]
	print(cells_array.shape)
	origin_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(0, 0)]
	# rand_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(1, 3)]
	# rand_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(9, 0)]
	rand_cell = mm.grid_coords_cell_objs_key_value_pair_dict[(-2, 3)]
	print(rand_cell.left_most_px)
	print(rand_cell.top_most_px)
	print(rand_cell.right_most_px)
	print(rand_cell.bottom_most_px)
	print(rand_cell.x)
	print(rand_cell.y)


	# import itertools
	# import numpy as np
	# valid_cell_ids = list(range(-10, 10 + 1))
	# x_unit_cell_distances = list(range(-10, 10 + 1))
	# y_unit_cell_distances = list(range(-10, 10 + 1))
	# mesh_grid_points_coords = list(itertools.product(x_unit_cell_distances, y_unit_cell_distances))
	# mesh_grid_points_coords_array = np.asarray(mesh_grid_points_coords)
	# print(mesh_grid_points_coords_array)
	# print(mesh_grid_points_coords_array.shape)
	# new = np.reshape(mesh_grid_points_coords_array, (21, 21, 2), order='C')
	# # combos = list(itertools.combinations(valid_cell_ids, 2))
	# combos = list(itertools.combinations_with_replacement(valid_cell_ids, 2))
	# combos_array = np.asarray(combos)
	# # new_combos_array = np.reshape(combos_array, (105, 105, 2), order='C')
	# cy1 = np.vstack((combos_array[0], combos_array[1]))
	# cy2 = np.vstack((combos_array[20], combos_array[21]))
	# cx = np.hstack((cy1, cy2))