import numpy as np



class CoordinatesMap:


	def __init__(self, top_left_origin_world_coords, world_map_tiles_size):
		self.top_left_origin_world_coords = top_left_origin_world_coords
		self.top_left_origin_world_x_coords = self.top_left_origin_world_coords[0]
		self.top_left_origin_world_y_coords = self.top_left_origin_world_coords[1]
		self.world_map_tiles_size = world_map_tiles_size


	def __getitem__(self, key):
		# print(key)
		# print(type(key))
		row_idx = key[0]
		col_idx = key[1]
		world_x_coord = self.top_left_origin_world_x_coords + col_idx
		world_y_coord = self.top_left_origin_world_y_coords - row_idx
		return world_x_coord, world_y_coord

if __name__ == "__main__":
	tl_origin_world_coords = (3216, 3219)
	world_map_tiles_size = (32, 32)
	coords_map = CoordinatesMap(tl_origin_world_coords, world_map_tiles_size)
	idxs = (1, 2)
	print(coords_map[1,2])