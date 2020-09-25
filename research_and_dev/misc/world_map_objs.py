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
from research_and_dev.misc.mini_map_objs import MiniMapGrid

# Xis = [3216, 3225, 3234, 3235, 3229, 3223, 3219, 3214]
# Yis = [3219, 3219, 3219, 3226, 3233, 3239, 3244, 3245]
#
# paths = {(3216, 3219):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_castle", "square_objs_occupied":[]},
#          (3225, 3219):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3234, 3219):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3235, 3226):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3229, 3233):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3223, 3239):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3219, 3244):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":"lumbridge_walls", "square_objs_occupied":[]},
#          (3214, 3245):{"area_label_name":"Lumbridge", "region_label_id":12850, "square_confinement_name":None, "square_objs_occupied":[]}}
#
# def zip_Xis_Yis(Xis, Yis, wm_square_info_dict = None):
# 	wm_coords = []
# 	for xi, yi in zip(Xis, Yis):
# 		wm_square_info_dict = wm_square_info_dict
# 		if wm_square_info_dict is None:
# 			wm_coords.append((xi, yi))
# 		else:
# 			info = wm_square_info_dict[(xi, yi)]
# 			wm_coords.append((xi, yi, info))
# 		# wm_coords.append([xi, yi])
# 	return wm_coords
#
#
# wm_coords = zip_Xis_Yis(Xis, Yis)


class WorldMapSquare:

	def __init__(self, x, y, area_label_name = None, region_label_id = None, square_confinement_name = None,
	             square_objs_occupied = None):
		self.x_coord = x
		self.y_coord = y
		self.area_label_name = area_label_name
		self.region_label_id = region_label_id
		self.square_confinement_name = square_confinement_name
		self.square_objs_occupied = square_objs_occupied


		# self.world_map_square_ = world_map_square_







class WorldMapPath:

	def __init__(self, wm_grid_sq_coords, origin_info = None, destination_info = None, wm_path_squares_info_dict = None):
		self.wm_path_coords = wm_grid_sq_coords
		self.origin_info = origin_info
		self.destination_info = destination_info
		self.wm_path_squares_info_dict = wm_path_squares_info_dict
		# self.wm_path_origin_square_obj = WorldMapSquare(wm_path_coords[0][0], wm_path_coords[0][1])
		# self.wm_path_destination_square_obj = WorldMapSquare(wm_path_coords[-1][0], wm_path_coords[-1][1])
		self.wm_path_origin_square_coords = wm_grid_sq_coords[0]
		self.wm_path_destinartion_square_coords = wm_grid_sq_coords[1]
		self._wm_path_sqs_and_wm_grid_sq_objs_dict = self.create_path_points_wm_square_objs_dict()
		# self.wm_path_origin_square_obj = self._wm_path_sqs_and_wm_grid_sq_objs_dict[list(self._wm_path_sqs_and_wm_grid_sq_objs_dict.keys())[0]]
		# self.wm_path_destination_square_obj = self._wm_path_sqs_and_wm_grid_sq_objs_dict[list(self._wm_path_sqs_and_wm_grid_sq_objs_dict.keys())[-1]]
		self.wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords()


	def create_path_points_wm_square_objs_dict(self):
		"""

		:return: dict of (Xi, Yi):WorldMapSquare(Xi, Yi) class obj instances
		"""
		path_points_wm_square_objs_dict = {}
		# print("self.wm_path_coords", self.wm_path_coords)
		for path_points_list_idx, path_point_coords in enumerate(self.wm_path_coords):
			# print("path_points_list_idx", path_points_list_idx)
			# print("path_point_coords", path_point_coords)
			path_point_x_coord = path_point_coords[0]
			path_point_y_coord = path_point_coords[1]
			path_points_wm_square_objs_dict[path_point_coords] = WorldMapSquare(path_point_x_coord, path_point_y_coord)
		return path_points_wm_square_objs_dict


	def compute_wm_path_displacement_vectors_via_wm_coords(self):
		"""

		:return: list of nested 2-tuples e.g. [(9, 0), (5, 0), (-2, -5)]
		"""
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
			wm_path_displacement_vectors.append((dXi, dYi))

		return wm_path_displacement_vectors








class WorldMapGrid:

	WORLD_MAP_ORIGIN_GRID_COORDS = (3216, 3219)

	def __init__(self, num_of_grids=200):
		self.num_of_grids = num_of_grids
		self.path_to_travel = None
		self.travelling_path = False
		self.current_travell_path = None

	def set_travell_path(self, wm_grid_sq_coords):
		self.current_travell_path = WorldMapPath(wm_grid_sq_coords)

	def get_current_wm_travell_path_displacement_vectors(self):
		return self.current_travell_path.wm_path_displacement_vectors

	def compute_wm_path_displacement_vectors_via_wm_coords(self, wm_coords):
		path_wm_origin_x = wm_coords[0][0]
		path_wm_origin_y = wm_coords[0][1]
		path_wm_squares_travelled_to = wm_coords[0:]
		wm_path_displacement_vectors = []
		wm_init_square_x = path_wm_origin_x
		wm_init_square_y = path_wm_origin_y
		for path_points_list_idx, path_point_coords in enumerate(wm_coords[:-1]):
			departure_path_point = wm_coords[path_points_list_idx]
			arrival_path_point = wm_coords[path_points_list_idx + 1]
			dXi = arrival_path_point[0] - departure_path_point[0]
			dYi = arrival_path_point[1] - departure_path_point[1]
			wm_path_displacement_vectors.append([dXi, dYi])

		return wm_path_displacement_vectors

	def convert_wm_grid_square_coords_to_mm_displacement_vectors(self, wm_coords):
		world_map_path = WorldMapPath(wm_coords)
		wm_path_displacement_vectors= world_map_path.compute_wm_path_displacement_vectors_via_wm_coords()
		# wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(wm_coords)
		mm_path_displacement_vectors = []
		for wm_displacement_vector in wm_path_displacement_vectors:
			dxi = wm_displacement_vector[0]
			dyi = wm_displacement_vector[1] * -1
			mm_path_displacement_vectors.append([dxi, dyi])

		return mm_path_displacement_vectors


	def convert_wm_path_obj_to_mm_displacement_vectors(self, wm_path_obj):
		# print("wm_path_displacement_vectors: ", wm_path_obj)
		world_map_path_coords_list = wm_path_obj.wm_path_coords
		wm_path_displacement_vectors = wm_path_obj.compute_wm_path_displacement_vectors()
		# print("wm_path_displacement_vectors: ", wm_path_displacement_vectors)
		# wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(wm_coords)
		mm_path_displacement_vectors = []
		for wm_displacement_vector in wm_path_displacement_vectors:
			dxi = wm_displacement_vector[0]
			dyi = wm_displacement_vector[1] * -1
			mm_path_displacement_vectors.append((dxi, dyi))

		return mm_path_displacement_vectors


	def get_mm_path_displacement_vectors_via_wm_path_obj(self, world_map_path_obj):
		# world_map_path_obj = world_map_path_obj.wm_path_coords
		mm_path_displacement_vectors = self.convert_wm_path_obj_to_mm_displacement_vectors(world_map_path_obj)
		return mm_path_displacement_vectors


	def set_path_to_travel(self, wm_path_square_coords):
		wm_path_object_inst = WorldMapPath(wm_path_square_coords)
		wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(wm_path_object_inst.wm_path_coords)
		mm_path_displacement_vectors = self.convert_wm_grid_square_coords_to_mm_displacement_vectors(wm_path_displacement_vectors)
		self.mm_path_displacement_vectors_to_travel = mm_path_displacement_vectors
		self.mm_grid_obj_inst = MiniMapGrid()
		self.mm_grid_obj_inst.create_mm_grid_cells_coords()
		self.mm_grid_cells_coords_and_cell_objs_dict = self.mm_grid_obj_inst.grid_coords_cell_objs_key_value_pair_dict


	# def travel_via_set_path(self):
	# 	self.travelling_path = True
	# 	for mm_path_displacement_vertex in self.mm_path_displacement_vectors_to_travel:
	# 		self.mm_grid_obj_inst.grid_coords_cell_objs_key_value_pair_dict[]

		# MiniMapGrid()


