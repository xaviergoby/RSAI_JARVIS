import os
from path_manipulation_tools import file_path_tools
import settings
from src.game.world.world_map_grid import WorldMapGrid
from game.world.path import Path
from game.world.navigator import Navigator



class WorldMap:


	def __init__(self, world_map_data_file=None):
		self.world_map_data_file = world_map_data_file
		self.region_grid_labels = [12850]
		self.region_grid_label = 12850
		self.initialize_world_map()


	def initialize_world_map(self):
		if self.world_map_data_file is not None:
			self.data_dir_path = os.path.join(settings.DATA_DIR, r"world")
			self.world_map_data_file_path = os.path.join(self.data_dir_path, self.world_map_data_file)
			if file_path_tools.check_file_path_existence(self.world_map_data_file_path) is True:
				self.wm_grid_objs_dict = file_path_tools.load_pickled_json(self.world_map_data_file_path)
			elif file_path_tools.check_file_path_existence(self.world_map_data_file_path) is False:
				wm_grid_objs_dict = self.gen_new_world_map()
				file_path_tools.create_new_pickled_json(self.world_map_data_file_path, wm_grid_objs_dict)
				self.wm_grid_objs_dict = file_path_tools.load_pickled_json(self.world_map_data_file_path)
		elif self.world_map_data_file is None:
			wm_grid_objs_dict = self.gen_new_world_map()
			self.wm_grid_objs_dict = wm_grid_objs_dict
			pass


	def gen_new_world_map(self):
		wm_grid_objs_dict = {}
		for region_grid_label in self.region_grid_labels:
			grid = WorldMapGrid(region_grid_label)
			wm_grid_objs_dict[region_grid_label] = grid
		if len(self.region_grid_labels) == 1:
			self.wm_grid_obj = WorldMapGrid(self.region_grid_labels[0])
		return wm_grid_objs_dict


	def save_world_map(self, world_map_data_file_name):
		wm_grid_objs_dict = self.wm_grid_objs_dict
		if self.world_map_data_file is not None:
			file_path_tools.create_new_pickled_json(self.world_map_data_file_path, wm_grid_objs_dict)
		elif self.world_map_data_file is None:
			self.data_dir_path = os.path.join(settings.DATA_DIR, r"world")
			self.world_map_data_file_path = os.path.join(self.data_dir_path, world_map_data_file_name)
			file_path_tools.create_new_pickled_json(self.world_map_data_file_path, wm_grid_objs_dict)


	def navigate_path(self, game_sq_wm_path_coords):
		for game_sq_wm_coord in game_sq_wm_path_coords:
			self.wm_grid_obj.game_sq_wm_coords_objs_dict[game_sq_wm_coord].vissited = True
		path_obj = Path(game_sq_wm_path_coords)
		nav = Navigator()
		nav.navigate_path(path_obj)




if __name__ == "__main__":
	world_map_file_name = "world_maps.json"
	wm1 = WorldMap(world_map_file_name)
	wm2 = WorldMap()
	knw1 = wm1.wm_grid_objs_dict
	knw2 = wm2.wm_grid_objs_dict
	print(wm1.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].wm_sq_coords)
	print(wm2.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].wm_sq_coords)
	print(wm1.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].grid_sq_coords)
	print(wm2.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].grid_sq_coords)
	print(wm1.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].vissited)
	print(wm2.wm_grid_objs_dict[12850].game_sq_wm_coords_objs_dict[(3263, 3259)].vissited)
	wm2.wm_grid_obj.game_sq_wm_coords_objs_dict[(3263, 3259)].vissited = True
	wm1.wm_grid_obj.game_sq_wm_coords_objs_dict[(3263, 3259)].vissited = True
	wm2.save_world_map("world_map2.json")
	wm1.save_world_map("world_map2.json")
	print(wm1.wm_grid_obj.game_sq_wm_coords_objs_dict[(3263, 3259)].vissited)
	print(wm2.wm_grid_obj.game_sq_wm_coords_objs_dict[(3263, 3259)].vissited)
