import os
import settings
from jarvis.utils import file_path_tools


class WorldMapGrid:

	def __init__(self, vissited, navigable, grid_pos, world_map_pos, world_map_row_idx, world_map_col_idx):

		self.vissited = vissited
		self.navigable = navigable
		self.grid_pos = grid_pos
		self.world_map_pos = world_map_pos
		self.world_map_row_idx = world_map_row_idx
		self.world_map_col_idx = world_map_col_idx



class WorldMap:

	WORLD_MAP_ORIGIN_GRID_COORDS = (3216, 3219)

	def __init__(self, world_map_array, world_map_data_file, file_name=None, world_map_origin_grid_coords=(3216, 3219)):
		self.world_map_origin_grid_coords = world_map_origin_grid_coords
		self.world_map_data_file = world_map_data_file
		self.file_name = world_map_array if isinstance(world_map_array, str) else self.world_map_data_file
		# self.data_dir_path = os.path.join(settings.DATA_DIR, r"world")
		self.world_map_data_file_path = os.path.join(self.data_dir_path, self.world_map_data_file)
		self.world_map_data_file_path = os.path.join(settings.MAP_DATA_DIR, self.world_map_data_file) if isinstance(world_map_array, str) else self.world_map_data_file
		self.world_map_array =


	def gen_new_world_map_grid(self):
		grid_sq_coords_nested_list = []
		game_sq_coords_data_pair_dict = {}
		grid_sq_objs_dict = {}
		world_map_sq_objs_dict = {}
		grid_sq_row_idx_list = list(range(0, 63 + 1))
		grid_sq_col_idx_list = list(range(0, 63 + 1))
		for grid_sq_row_idx in grid_sq_row_idx_list:
			grid_sq_coords_nested_list.append([])
			for grid_sq_col_idx in grid_sq_col_idx_list:
				grid_sq_coords_nested_list[grid_sq_row_idx].append([grid_sq_row_idx, grid_sq_col_idx])
				grid_sq_x_y_coords = (grid_sq_row_idx, grid_sq_col_idx)

				# Transform the grid sq coords to world map sq coords for the grid containing Lumbridge
				# in other words, the grid in the world map whose bottom-left sq has the coords (3200, 3200)
				world_map_sq_row_idx = 3200 + grid_sq_row_idx
				world_map_sq_col_idx = 3200 + grid_sq_col_idx
				world_map_sq_pos = (world_map_sq_row_idx, world_map_sq_col_idx)

				game_sq_dict_data = {"vissited": False, "navigable":False, "grid_pos" : grid_sq_x_y_coords, "world_map_pos" : world_map_sq_pos,
				                      "world_map_row_idx" : world_map_sq_row_idx, "world_map_col_idx" : world_map_sq_col_idx}
				game_sq_coords_data_pair_dict[grid_sq_x_y_coords] = game_sq_dict_data

				grid_obj = WorldMapGrid(vissited=False, navigable=False, grid_pos=grid_sq_x_y_coords, world_map_pos=world_map_sq_pos,
				                        world_map_row_idx=world_map_sq_row_idx, world_map_col_idx=world_map_sq_col_idx)
				grid_sq_objs_dict[grid_sq_x_y_coords] = grid_obj
				world_map_sq_objs_dict[world_map_sq_pos] = grid_obj

		# file_path_tools.write_to_json_file(self.world_map_data_file_path, grid_coords_dict)
		return world_map_sq_objs_dict



	def load_world_map_json_data_dict(self):
		if file_path_tools.check_file_path_existence(self.world_map_data_file_path) is True:
			return file_path_tools.load_pickled_json(self.world_map_data_file_path)
		else:
			file_path_tools.create_new_pickled_json(self.world_map_data_file_path, self.gen_new_world_map_grid())
			# file_path_tools.create_new_json_file(self.world_map_data_file_path, self.gen_new_world_map_grid())
			return file_path_tools.load_pickled_json(self.world_map_data_file_path)



if __name__ == "__main__":
	world_map_file_name = "world_maps.json"
	wm = WorldMap(world_map_file_name)
	wm.gen_new_world_map_grid()
	# res = np.asarray(res_list)
	res_dict = wm.load_world_map_json_data_dict()
	print(res_dict)
	print(res_dict.keys())

