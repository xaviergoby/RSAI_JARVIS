import numpy as np
import itertools
from sklearn.preprocessing import OneHotEncoder
import settings

class LocalNavigationGridMap:
	"""
	ego_cent: egocentric
	rf/ref_frame: reference frame
	nn: nearest neighbour
	scrn: screen
	px: pixel
	pnt: point
	abs: absolute
	coords: coordinates
	ohe: one-hot encoded/encoding
	ohel: one-hot encoded/encoding label
	"""
	
	def __init__(self, grid_opt):
		self.events_list = None
		self.bot_current_loc = None
		self.grid_opt = grid_opt
		self.grid_settings = settings.MESH_GRID_OPTIONS[self.grid_opt]
		
		self.px_x_axes_pnts = np.linspace(*self.grid_settings["x_grid_pnts"])
		self.px_y_axes_pnts = np.linspace(*self.grid_settings["y_grid_pnts"])
		self.grid_x_px_pnts, self.grid_y_px_pnts = np.meshgrid(self.px_x_axes_pnts, self.px_y_axes_pnts)
		
		self.num_of_px_pnts_on_axes = len(self.px_x_axes_pnts)
		self.ego_cent_rf_grid_rad = (self.num_of_px_pnts_on_axes - 1) / 2
		self.ego_cent_rf_grid_x_axes_pnts = np.linspace(-self.ego_cent_rf_grid_rad,
		                                                self.ego_cent_rf_grid_rad,
		                                                self.num_of_px_pnts_on_axes)
		self.ego_cent_rf_grid_y_axes_pnts = np.linspace(self.ego_cent_rf_grid_rad,
		                                                -self.ego_cent_rf_grid_rad,
		                                                self.num_of_px_pnts_on_axes)
		self.grid_x_pnts, self.grid_y_pnts = np.meshgrid(self.ego_cent_rf_grid_x_axes_pnts,
		                                                 self.ego_cent_rf_grid_y_axes_pnts)
	
	def get_lmc_nn_grid_pnt_px_coords(self, lmc_px_x, lmc_px_y):  # 1.2
		abs_diff_x_coord_func = lambda list_value: abs(list_value - lmc_px_x)
		abs_diff_y_coord_func = lambda list_value: abs(list_value - lmc_px_y)
		nn_px_x = min(self.px_x_axes_pnts, key=abs_diff_x_coord_func)
		nn_px_y = min(self.px_y_axes_pnts, key=abs_diff_y_coord_func)
		return nn_px_x, nn_px_y
	
	def get_lmc_nn_grid_pnt_idxs(self, lmc_px_x, lmc_px_y):  # 1.1
		lmc_nn_px_x, lmc_nn_px_y = self.get_lmc_nn_grid_pnt_px_coords(lmc_px_x, lmc_px_y)
		lmc_nn_grid_pnt_coords_idxs = np.argwhere((self.grid_x_px_pnts == lmc_nn_px_x) &
		                                          (self.grid_y_px_pnts == lmc_nn_px_y))[0]
		lmc_nn_grid_pnt_x_idx, lmc_nn_grid_pnt_y_idx = lmc_nn_grid_pnt_coords_idxs
		return lmc_nn_grid_pnt_x_idx, lmc_nn_grid_pnt_y_idx
	
	def get_lmc_nn_grid_pnt(self, lmc_px_x, lmc_px_y):  # 1.0
		"""
		:param lmc_px_x: the true/original/real x pixel coordinate of where lmc occured, e.g. 392
		:param lmc_px_y: the true/original/real y pixel coordinate of where lmc occured, e.g. 212
		:return: a 2-tuple of the x and y coords of the nn grid point of where lmc occired, e.g. (0.0, 2.0)
		"""
		lmc_nn_grid_pnt_idxs = self.get_lmc_nn_grid_pnt_idxs(lmc_px_x, lmc_px_y)
		lmc_nn_grid_pnt_y_coord_idx = lmc_nn_grid_pnt_idxs[0]
		lmc_nn_grid_pnt_x_coord_idx = lmc_nn_grid_pnt_idxs[1]
		ego_cent_rf_grid_x_axes_pnts = self.ego_cent_rf_grid_x_axes_pnts
		ego_cent_rf_grid_y_axes_pnts = self.ego_cent_rf_grid_y_axes_pnts
		nn_grid_pnt_x = ego_cent_rf_grid_x_axes_pnts[lmc_nn_grid_pnt_x_coord_idx]
		nn_grid_pnt_y = ego_cent_rf_grid_y_axes_pnts[lmc_nn_grid_pnt_y_coord_idx]
		return nn_grid_pnt_x, nn_grid_pnt_y
	
	@property
	def grid_pnts(self):
		valid_grid_pnt_coords_permutations_nested_list = list(itertools.product(self.ego_cent_rf_grid_x_axes_pnts,
		                                                                        self.ego_cent_rf_grid_y_axes_pnts))
		valid_grid_pnt_coords_permutations_nested_list = list(map(list, valid_grid_pnt_coords_permutations_nested_list))
		return valid_grid_pnt_coords_permutations_nested_list
	
	@property
	def grid_px_pnts(self):
		valid_grid_pnt_coords_permutations_nested_list = list(itertools.product(self.px_x_axes_pnts,
		                                                                        self.px_y_axes_pnts))
		valid_grid_pnt_coords_permutations_nested_list = list(map(list, valid_grid_pnt_coords_permutations_nested_list))
		return valid_grid_pnt_coords_permutations_nested_list
	
	@property
	def grid_pnt_ohe_labels(self):
		onehotencoder = OneHotEncoder()
		one_hot_encoded_grid_pnt_coord_labels = onehotencoder.fit_transform(self.grid_pnts).toarray()
		return one_hot_encoded_grid_pnt_coord_labels
	
	def grid_pnt_2_ohe_label(self, x, y):
		all_mesh_grid_pnts = self.grid_pnts
		one_hot_encoded_grid_pnt_coord_labels = self.grid_pnt_ohe_labels
		grid_pnt_x_coord = float(x)
		grid_pnt_y_coord = float(y)
		grid_pnt_coord_list = [grid_pnt_x_coord, grid_pnt_y_coord]
		for grid_pnt_coord in all_mesh_grid_pnts:
			if grid_pnt_coord_list == grid_pnt_coord:
				grid_pnt_coord_idx = all_mesh_grid_pnts.index(grid_pnt_coord)
				grid_pnt_coord_encoded_label = one_hot_encoded_grid_pnt_coord_labels[grid_pnt_coord_idx]
				return grid_pnt_coord_encoded_label
	
	def ohe_label_2_grid_pnt(self, ohe_label):
		grid_pnts = self.grid_pnts
		one_hot_encoded_grid_pnt_coord_labels = self.grid_pnt_ohe_labels
		for encoded_label_i_idx in range(len(one_hot_encoded_grid_pnt_coord_labels)):
			encoded_label_i = one_hot_encoded_grid_pnt_coord_labels[encoded_label_i_idx]
			if encoded_label_i.tolist() == ohe_label.tolist():
				grid_pnt_matching_1_ = grid_pnts[encoded_label_i_idx]
				return grid_pnt_matching_1_


if __name__ == "__main__":
	import settings
	from research_and_dev.event_driven_system.utils import img_overlay_tools
	
	grid_opt = 1
	mgrid = LocalNavigationGridMap(grid_opt)
	print(mgrid.px_x_axes_pnts)
	print(mgrid.px_y_axes_pnts)
	print(mgrid.ego_cent_rf_grid_x_axes_pnts)
	print(mgrid.ego_cent_rf_grid_y_axes_pnts)
	lmc_x = 392
	lmc_y = 212
	print(mgrid.get_lmc_nn_grid_pnt_px_coords(lmc_x, lmc_y))
	print(mgrid.get_lmc_nn_grid_pnt_idxs(lmc_x, lmc_y))
	print(mgrid.ego_cent_rf_grid_x_axes_pnts[mgrid.get_lmc_nn_grid_pnt_idxs(lmc_x, lmc_y)[0]])
	print(mgrid.ego_cent_rf_grid_y_axes_pnts[mgrid.get_lmc_nn_grid_pnt_idxs(lmc_x, lmc_y)[1]])
	
	grid_pnt_coords = mgrid.get_lmc_nn_grid_pnt(lmc_x, lmc_y)
	grid_pnt_x = grid_pnt_coords[0]
	grid_pnt_y = grid_pnt_coords[1]
	print("Resulting nn grid pnt (x, y): ({0}, {1})".format(grid_pnt_x, grid_pnt_y))
	
	grid_pnt_ohe_labels = mgrid.grid_pnt_ohe_labels
	print(grid_pnt_ohe_labels)
	print(grid_pnt_ohe_labels.shape)
	
	# test_x = -5
	test_x = grid_pnt_x
	# test_y = 5
	test_y = grid_pnt_y
	label = mgrid.grid_pnt_2_ohe_label(test_x, test_y)
	grid_pnt = mgrid.ohe_label_2_grid_pnt(label)
	print(f"ohe label of {test_x}, {test_y}: {label}")
	print(f"grid point coords of {label}: {grid_pnt}")
	print(mgrid.grid_px_pnts)
	
	r = img_overlay_tools.draw_sq_grid_lines_on_img_v1(1, mgrid.px_x_axes_pnts.astype(int).tolist(),
	                                                   mgrid.px_y_axes_pnts.astype(int).tolist())
	print(r[0])
	print(r[1])
