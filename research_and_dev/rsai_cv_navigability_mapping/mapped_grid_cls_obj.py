import numpy as np
from research_and_dev.rsai_cv_navigability_mapping import cv_nav_settings



class MappedGridClsObj:

	def __init__(self, mapped_grid_array, mapped_grid_label):
		self.mapped_grid_array = mapped_grid_array
		self.mapped_grid_label = str(mapped_grid_label)
		self.tl_origin_point_world_coord = cv_nav_settings.GRID_REGION_TL_ORIGIN_WORLD_COORDS_DICT[self.mapped_grid_label]
		self.tl_origin_point_world_row_idx = self.tl_origin_point_world_coord[0]
		self.tl_origin_point_world_col_idx = self.tl_origin_point_world_coord[1]

	def get_tile_world_coord(self, grid_row_idx, grid_col_idx):
		tile_world_row_idx = self.tl_origin_point_world_row_idx - grid_row_idx
		tile_world_col_idx = self.tl_origin_point_world_col_idx - grid_col_idx
		return tile_world_row_idx, tile_world_col_idx

