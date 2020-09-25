import numpy as np
import itertools
from research_and_dev.event_driven_system.utils.data_storage_tools import get_bot_current_loc
from sklearn.preprocessing import OneHotEncoder
import os
import settings




class WorldMapNavGrid:


	def __init__(self, world_map_shape):
		self.world_map_shape = world_map_shape
		self.world_map_grid_name = "world_map_{0}_by_{1}.npy".format(self.world_map_shape[0], self.world_map_shape[1])
		self.world_map_grid_data_dir = os.path.join(settings.DATA_DIR, "world_maps")
		self.world_map_grid_path = os.path.join(self.world_map_grid_data_dir, self.world_map_grid_name)


	# @property
	def get_saved_world_maps(self):
		saved_world_maps = os.listdir(self.world_map_grid_data_dir)
		return saved_world_maps

	def check_world_map_existence(self):
		saved_world_maps = self.get_saved_world_maps()
		if self.world_map_grid_name in saved_world_maps:
			return True
		else:
			return False

	def gen_world_map_grid(self):
		world_map_grid_array = np.zeros((self.world_map_shape[0]*64, self.world_map_shape[1]*64))
		np.save(self.world_map_grid_path, world_map_grid_array)

	def load_world_map(self):
		if self.check_world_map_existence() is False:
			print("Creating new world map grid of shape: {0}".format(self.world_map_shape))
			self.gen_world_map_grid()
			self.world_map_grid = np.load(self.world_map_grid_path)
		else:
			self.world_map_grid = np.load(self.world_map_grid_path)

	def update_word_grid_tile(self, world_grid_loc):
		world_grid_col_loc = world_grid_loc[0]
		world_grid_row_loc = world_grid_loc[1]
		world_grid_tile_col_idx = (world_grid_col_loc-1152)
		world_grid_tile_row_idx = (4159-world_grid_row_loc)
		self.world_map_grid[world_grid_tile_row_idx,world_grid_tile_col_idx] = 1

	def get_word_grid_tile_val(self, world_grid_loc):
		world_grid_col_loc = world_grid_loc[0]
		world_grid_row_loc = world_grid_loc[1]
		world_grid_tile_col_idx = (world_grid_col_loc-1152)
		world_grid_tile_row_idx = (4159-world_grid_row_loc)
		return self.world_map_grid[world_grid_tile_row_idx,world_grid_tile_col_idx]

	def update_world_grid(self):
		np.save(self.world_map_grid_path, self.world_map_grid)
		# return world_grid_tile_row_idx, world_grid_tile_col_idx


			# break


if __name__ == "__main__":
	src = WorldMapNavGrid((43, 26))
	# print(src.get_saved_world_maps())
	# print(src.check_world_map_existence())
	print(src.load_world_map())
	print(src.world_map_grid)
	print(src.world_map_grid.shape)
	src.update_word_grid_tile((1159, 2496))
	print(src.get_word_grid_tile_val((1159, 2496)))
	