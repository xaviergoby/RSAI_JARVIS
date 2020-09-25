




class Path:

	def __init__(self, game_sq_wm_path_coords):
		self.game_sq_wm_path_coords = game_sq_wm_path_coords
		# self.origin_info = origin_info
		# self.destination_info = destination_info
		# self.wm_path_squares_info_dict = wm_path_squares_info_dict
		# self.wm_path_origin_square_obj = WorldMapSquare(wm_path_coords[0][0], wm_path_coords[0][1])
		# self.wm_path_destination_square_obj = WorldMapSquare(wm_path_coords[-1][0], wm_path_coords[-1][1])
		# self.wm_path_origin_square_coords = game_sq_wm_path_coords[0]
		# self.wm_path_destinartion_square_coords = game_sq_wm_path_coords[1]
		# self._wm_path_sqs_and_wm_grid_sq_objs_dict = self.create_path_points_wm_square_objs_dict()
		# self.wm_path_origin_square_obj = self._wm_path_sqs_and_wm_grid_sq_objs_dict[list(self._wm_path_sqs_and_wm_grid_sq_objs_dict.keys())[0]]
		# self.wm_path_destination_square_obj = self._wm_path_sqs_and_wm_grid_sq_objs_dict[list(self._wm_path_sqs_and_wm_grid_sq_objs_dict.keys())[-1]]
		self.wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors()
		self.mm_path_displacement_vectors = self.compute_mm_path_displacement_vectors()



	# def create_path_points_wm_square_objs_dict(self):
	# 	"""
	#
	# 	:return: dict of (Xi, Yi):WorldMapSquare(Xi, Yi) class obj instances
	# 	"""
	# 	path_points_wm_square_objs_dict = {}
	# 	# print("self.wm_path_coords", self.wm_path_coords)
	# 	for path_point_coords in self.game_sq_wm_path_coords:
	# 		# print("path_points_list_idx", path_points_list_idx)
	# 		# print("path_point_coords", path_point_coords)
	# 		path_point_x_coord = path_point_coords[0]
	# 		path_point_y_coord = path_point_coords[1]
	# 		path_points_wm_square_objs_dict[path_point_coords] = WorldMapSquare(path_point_x_coord, path_point_y_coord)
	# 	return path_points_wm_square_objs_dict


	def compute_wm_path_displacement_vectors(self):
		"""

		:return: list of nested 2-tuples e.g. [(9, 0), (5, 0), (-2, -5)]
		"""
		# path_wm_origin_x = self.game_sq_wm_path_coords[0][0]
		# path_wm_origin_y = self.game_sq_wm_path_coords[0][1]
		# path_wm_squares_travelled_to = self.wm_path_coords[0:]
		wm_path_displacement_vectors = []
		# wm_init_square_x = path_wm_origin_x
		# wm_init_square_y = path_wm_origin_y
		for path_points_list_idx, path_point_coords in enumerate(self.game_sq_wm_path_coords[:-1]):
			departure_path_point = self.game_sq_wm_path_coords[path_points_list_idx]
			arrival_path_point = self.game_sq_wm_path_coords[path_points_list_idx + 1]
			dXi = arrival_path_point[0] - departure_path_point[0]
			dYi = arrival_path_point[1] - departure_path_point[1]
			wm_path_displacement_vectors.append((dXi, dYi))

		return wm_path_displacement_vectors


	def compute_mm_path_displacement_vectors(self):
		# world_map_path = WorldMapPath(wm_coords)
		wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors()
		# wm_path_displacement_vectors = self.compute_wm_path_displacement_vectors_via_wm_coords(wm_coords)
		mm_path_displacement_vectors = []
		for wm_displacement_vector in wm_path_displacement_vectors:
			dxi = wm_displacement_vector[0]
			dyi = wm_displacement_vector[1] * -1
			mm_path_displacement_vectors.append([dxi, dyi])

		return mm_path_displacement_vectors



