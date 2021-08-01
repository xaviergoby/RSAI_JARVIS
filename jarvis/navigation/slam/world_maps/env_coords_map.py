# import os
import numpy as np
# import settings
# from matplotlib import pyplot as plt


class EnvironmentCoordinatesMap:

	def __init__(self, top_left_origin_world_coords, world_map_tiles_size):
		self.top_left_origin_world_coords = top_left_origin_world_coords
		self.top_left_origin_world_x_coords = self.top_left_origin_world_coords[0]
		self.top_left_origin_world_y_coords = self.top_left_origin_world_coords[1]
		self.world_map_tiles_size = world_map_tiles_size

	def __getitem__(self, key):
		print(key)
		print(type(key))
		tile_world_row_idx = key[1]
		tile_world_col_idx = key[0]
		env_tile_col_idx = tile_world_col_idx - self.top_left_origin_world_x_coords
		env_tile_row_idx = self.top_left_origin_world_y_coords - tile_world_row_idx
		return env_tile_col_idx, env_tile_row_idx

	# def vis(self):
	# 	fig, ax = plt.subplots(figsize=(10, 8))
	# 	ax.imshow(self.navigability_array, cmap='gray')
	# 	ax.title.set_text(self.__repr__())
	# 	plt.show()


if __name__ == "__main__":
	top_left_origin_world_coords = (3136, 3519)
	world_map_tiles_size = (384, 128)
	env_coords_map = EnvironmentCoordinatesMap(top_left_origin_world_coords, world_map_tiles_size)
	# world_tile_coords = (3216, 3219)
	# 3235, 3218
	# 3251, 3266
	lumgridbe_castle_entrace_start_pos_array_idxs = env_coords_map[3235, 3218]
	bridge_cow_pen_al_kharid_junction_array_idxs = env_coords_map[3260, 3230]
	cow_pen_entrace_array_idxs = env_coords_map[3251, 3266]
	print(f"lumgridbe_castle_entrace_start_pos_array_idxs: {lumgridbe_castle_entrace_start_pos_array_idxs}")
	print(f"bridge_cow_pen_al_kharid_junction_array_idxs: {bridge_cow_pen_al_kharid_junction_array_idxs}")
	print(f"cow_pen_entrace_array_idxs: {cow_pen_entrace_array_idxs}")

	world_map_start_pos_world_coords = (3235, 3218)
	start_pos_world_x_coord = world_map_start_pos_world_coords[0]
	start_pos_world_y_coord = world_map_start_pos_world_coords[1]
	start_pos_nav_coords = env_coords_map[start_pos_world_x_coord, start_pos_world_y_coord]
	start_pos_nav_x_coord = start_pos_nav_coords[0]
	start_pos_nav_y_coord = start_pos_nav_coords[1]
	print(f"world_map_start_pos_world_coords: {world_map_start_pos_world_coords}")
	print(f"start_pos_world_x_coord: {start_pos_world_x_coord}")
	print(f"start_pos_world_y_coord: {start_pos_world_y_coord}")
	print(f"start_pos_nav_coords: {start_pos_nav_coords}")
	print(f"start_pos_nav_x_coord: {start_pos_nav_x_coord}")
	print(f"start_pos_nav_y_coord: {start_pos_nav_y_coord}")
