import numpy as np


# A single 256 x 256 pixels image represents a 1/4 of the complete grid.
# This single image of 256 x 256 pixels will either represent the:
# Top Left
# Top Right
# Bottom Left
# Bottom Right
# segment of the grid.
# A single one of these 256 x 256 pixels images will have 32 game tiles/squares along both its
# width and height! So 1 game square/tile = 8 x 8 pixels
# 256 x 256 pixels = 32 x 32 game squares/tiles

#         bottom left OR  top left
# 12850: (3200, 3200) OR (3200, 3263)
# 12851: (3200, 3264) OR (3200, 3327)




class ImageToWorldGridNavigabilityMapper:


	def __init__(self, img_array, tile_side_px_len, origin_tile_coords):
		self.img_array = img_array
		self.tile_side_px_len = tile_side_px_len
		self.origin_tile_coords = origin_tile_coords
		self.origin_tile_row_idx = self.origin_tile_coords[0]
		self.origin_tile_col_idx = self.origin_tile_coords[1]
		self.img_side_px_len = self.img_array.shape[0]
		self.subgrid_side_sq_len = int(self.img_side_px_len/self.tile_side_px_len)
		self.init_navigable_template = np.ones((32, 32))



	def get_img_px_world_tile_coords(self, img_px_row_idx, img_px_col_idx):
		world_tile_row_idx = self.origin_tile_row_idx - int(img_px_row_idx/self.tile_side_px_len)
		world_tile_col_idx = self.origin_tile_col_idx + int(img_px_col_idx/self.tile_side_px_len)
		return world_tile_row_idx, world_tile_col_idx

	def get_subgrid_world_tile_coords(self, subgrid_row_idx, subgrid_col_idx):
		world_tile_row_idx = self.origin_tile_row_idx - subgrid_row_idx
		world_tile_col_idx = self.origin_tile_col_idx + subgrid_col_idx
		return world_tile_row_idx, world_tile_col_idx


	def create_navigable_tiles_mapping(self):
		for img_px_row_i_idx in range(self.img_array.shape[0]):
			for img_px_col_j_idx in range(self.img_array.shape[1]):
				img_px_row_i_col_j_val = self.img_array[img_px_row_i_idx, img_px_col_j_idx]
				pass




if __name__ == "__main__":
	img_array = np.zeros((256, 256))
	tile_side_px_len = 8
	# bottom_left_origin_tile_coords = (3200, 3232)
	top_left_tile_row_coord = 3232 # tile row idx
	top_left_tile_col_coord = 3232 # tile col idx
	top_left_origin_tile_coords = (top_left_tile_row_coord, top_left_tile_col_coord)  # (x, y)

	img_px_row_idx = 17
	img_px_col_idx = 14

	subgrid_row_idx = 0
	subgrid_col_idx = 0

	nav_mapper = ImageToWorldGridNavigabilityMapper(img_array, tile_side_px_len, top_left_origin_tile_coords)
	img_px_idx_world_tile_coords = nav_mapper.get_img_px_world_tile_coords(img_px_row_idx, img_px_col_idx)
	subgrid_world_tile_coords = nav_mapper.get_subgrid_world_tile_coords(img_px_row_idx, img_px_col_idx)
	print(img_px_idx_world_tile_coords)
