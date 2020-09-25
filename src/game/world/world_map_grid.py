from src.game.world.world_map_square import GameSquare




class WorldMapGrid:

	WORLD_MAP_ORIGIN_GRID_COORDS = (3216, 3219)

	def __init__(self, region_grid_label):
		self.region_grid_label = region_grid_label
		self.gen_new_grid()


	def grid_sqs_coords_generator(self):
		"""
		:return: a list of the x and local_y coords of each of all the squares in the grid
		 list[0] returns the x & local_y coords of all the squars from (0, 0) to (0, 63) - so all the squares located horizontally
		 rightwards starting from the bottom left corner. list[1] then returns the x & local_y coords of all the squars from (1, 0) to (1, 63) etc
		"""
		grid_sq_row_idx_list = list(range(0, 63 + 1))
		grid_sq_col_idx_list = list(range(0, 63 + 1))

		for grid_sq_row_idx in grid_sq_row_idx_list:
			for grid_sq_col_idx in grid_sq_col_idx_list:
				yield grid_sq_row_idx, grid_sq_col_idx


	def gen_grid_sqs(self):
		game_sq_wm_coords_objs_dict = {}
		game_sq_grid_coords_objs_dict = {}
		for grid_sq_coord in self.grid_sqs_coords_generator():
			game_sq_grid_x_coord = grid_sq_coord[0]
			game_sq_grid_y_coord = grid_sq_coord[1]
			game_sq_grid_coords = (game_sq_grid_x_coord, game_sq_grid_y_coord)

			# Transform the grid sq coords to world map sq coords for the grid containing Lumbridge
			# in other words, the grid in the world map whose bottom-left sq has the coords (3200, 3200)
			game_sq_wm_x_coord = 3200 + game_sq_grid_x_coord
			game_sq_wm_y_coord = 3200 + game_sq_grid_y_coord
			game_sq_wm_coords = (game_sq_wm_x_coord, game_sq_wm_y_coord)

			game_sq_obj = GameSquare(vissited=False, grid_sq_coords=game_sq_grid_coords, wm_sq_coords=game_sq_wm_coords)
			game_sq_grid_coords_objs_dict[game_sq_grid_coords] = game_sq_obj
			game_sq_wm_coords_objs_dict[game_sq_wm_coords] = game_sq_obj

		self.game_sq_wm_coords_objs_dict = game_sq_wm_coords_objs_dict
		self.game_sq_grid_coords_objs_dict = game_sq_grid_coords_objs_dict

	def gen_new_grid(self):
		self.gen_grid_sqs()




if __name__ == "__main__":
	# world_map_file_name = "world_maps.json"
	wm = WorldMapGrid(12850)
	# sqs = wm.get_grid_sq_coords_list()
	# grid_sq_coords_gen = wm.grid_sq_coords_generator(sqs)
	gen = wm.grid_sqs_coords_generator()
	# gen = wm.grid_sq_coords_generator(sqs)
	n = 0
	max = 66
	for i in gen:
		if n < max:
			print("\ncoord pos {0}/{1}: x={2} & local_y={3}".format(n, max-1, i[0], i[1]))
			n = n + 1
		else:
			break
	# print(next(gen))
	# res = np.asarray(res_list)
	# res_dict = wm.gen_grid()
	# print(res_dict)
	# print(res_dict.keys())