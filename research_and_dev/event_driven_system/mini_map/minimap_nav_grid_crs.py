import numpy as np



class MinimapNavGridCoordRefSys:
	"""
	Check Minimap class located @
	from research_and_dev.event_driven_system.mini_map.minimap import Minimap
	for information
	"""
	def __init__(self, game_client_dims):
		self.game_client_dims = game_client_dims
		self.game_client_width = self.game_client_dims[0]
		self.game_client_height = self.game_client_dims[1]
		self.grid_centre_pnt_leftmost_pxx_coord = self.game_client_width - 83
		self.grid_centre_pnt_topmost_pxy_coord = self.game_client_height - 478

	# @staticmethod
	def _convert_px_x_coord_2_ds_x(self, px_x_coord):
		"""
		Formula: gx = int(np.floor(((lmc_pxx-708)/4)))
		:param px_x_coord: int of the pixel x coord on screen
		:return: int type of the x coord of the corresponding grid pnt
		"""
		ds_x = int(np.floor(((px_x_coord-self.grid_centre_pnt_leftmost_pxx_coord)/4)))
		return ds_x

	# @staticmethod
	def _convert_px_y_coord_2_ds_y(self, px_y_coord):
		"""
		Formula: gy = int(-np.floor(((lmc_pxy-113)/4)))
		:param px_y_coord: int of the pixel y coord on screen
		:return: int type of the y coord of the corresponding grid pnt
		"""
		ds_y = int(-np.floor(((px_y_coord-self.grid_centre_pnt_topmost_pxy_coord)/4)))
		return ds_y

	# @staticmethod
	def convert_px_coords_2_ds_vec(self, px_x, px_y):
		"""
		Transformation formulas:
		gx = int(np.floor(((lmc_pxx-708)/4)))
		gy = int(-np.floor(((lmc_pxy-113)/4)))
		:param px_x: int of the pixel x coord on screen
		:param px_y: int of the pixel y coord on screen
		:return: 2-tuple of ints: (gx, gy)
		"""
		ds_x = self._convert_px_x_coord_2_ds_x(px_x)
		ds_y = self._convert_px_y_coord_2_ds_y(px_y)
		return ds_x, ds_y



if __name__ == "__main__":
	mm_local_nav_grid_crs = MinimapNavGridCoordRefSys((791, 591))
	lmc_pxx = 715
	# lmc_pxx = 652
	# lmc_pxx = 764
	lmc_pxy = 112
	gx, gy = mm_local_nav_grid_crs.convert_px_coords_2_ds_vec(lmc_pxx, lmc_pxy)
	print(f"lmc_pxx: {lmc_pxx}  &  gx: {gx}\nlmc_pxy: {lmc_pxy}  &  gy: {gy}")