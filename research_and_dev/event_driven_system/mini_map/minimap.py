from research_and_dev.event_driven_system.mini_map.minimap_nav_grid import MinimapNavGrid
from research_and_dev.event_driven_system.mini_map.minimap_nav_grid_crs import MinimapNavGridCoordRefSys
from research_and_dev.event_driven_system.mini_map.minimap_screen_roi_properties import MiniMapScreenRegion
from research_and_dev.event_driven_system.nav_data_tools.nav_data_toolkit import NavigationDataToolkit
from research_and_dev.event_driven_system.utils.data_storage_tools import get_bot_current_loc


class Minimap(MinimapNavGrid, MinimapNavGridCoordRefSys, MiniMapScreenRegion):
	"""
	The 3 classes from which this class inherits are:
	MinimapNavGrid, MinimapNavGridCoordRefSys and MiniMapScreenRegion.

		MinimapNavGrid: Container of all the minimap grid points and ohe cls labels data and
		conains the methods necessary to convert between ds vectors and ohe cls labels!

		MinimapNavGridCoordRefSys: This class so far (updated: 21/05/2020) only provides a sinple
		(publicly accesible) function/method for converting the the x and y coordinates of where
		a left mouse click occured to the x and y componenents of the displacement vector associated
		with this lmc. NOTE: This displacement vector's point of origin is located at the very centre of the
		minimap, essentially where your dude is also located within the minimap.

		MiniMapScreenRegion: This class only contains property methods/functions which provide detailed
		information regarding the dimensions and position coordinates etc of the minimap's region of interest
		NOTE: This class makes use of parameter variables assigned in settings.py
	"""
	def __init__(self, game_client_dims, nav_grid_side_len=19, current_world_grid_loc=None):
		self.current_world_grid_loc = current_world_grid_loc
		self.game_client_dims = game_client_dims
		self.game_client_width = self.game_client_dims[0]
		self.game_client_height = self.game_client_dims[1]
		self.nav_grid_side_len = nav_grid_side_len
		self.current_world_grid_loc = NavigationDataToolkit.load_bot_init_world_loc() if current_world_grid_loc is None else current_world_grid_loc
		self.current_world_grid_x_loc = self.current_world_grid_loc[0]
		self.current_world_grid_y_loc = self.current_world_grid_loc[1]
		self.name = "Minimap"
		self.current_world_grid_loc = None

		MinimapNavGridCoordRefSys.__init__(self, game_client_dims)
		MinimapNavGrid.__init__(self, nav_grid_side_len)
		MiniMapScreenRegion.__init__(self, nav_grid_side_len)

	def get_lmc_ds_vec(self, lmc_pxx, lmc_pxy):
		"""
		Convert the x and y pixel coordinates of where the left mouse was clicked to the x and y
		components of the displacement vector associated with the lmc
		:param lmc_pxx: int
		:param lmc_pxy: int
		:return:a tuple containing 2 ints (world_nav_grid_x_coord, world_nav_grid_y_coord)
		"""
		ds_x, ds_y = self.convert_px_coords_2_ds_vec(lmc_pxx, lmc_pxy)
		return ds_x, ds_y

	def get_lmc_world_grid_loc(self, lmc_pxx, lmc_pxy):
		"""
		Convert the x and y pixel coordinates of where the left mouse was clicked to the x and y
		world (grid) coordinates associated with where the lmc occured
		:param lmc_pxx: int
		:param lmc_pxy: int
		:return: a tuple containing 2 ints (world_nav_grid_x_coord, world_nav_grid_y_coord)
		"""
		local_nav_grid_x_coord, local_nav_grid_y_coord = self.convert_px_coords_2_ds_vec(lmc_pxx, lmc_pxy)
		world_nav_grid_x_coord = self.current_world_grid_x_loc + local_nav_grid_x_coord
		world_nav_grid_y_coord = self.current_world_grid_y_loc + local_nav_grid_y_coord
		return world_nav_grid_x_coord, world_nav_grid_y_coord

	def get_lmc_ds_vect_ohe_cls_label(self, lmc_pxx, lmc_pxy):
		"""
		What this function does is that it converts the x and y of the lmc to the one-hot encoded class
		label of the displacement (vector) associated with the lmc that was made.
		:param lmc_pxx: int
		:param lmc_pxy: int
		:return: the ohe cls label array
		"""
		ds_x, ds_y = self.convert_px_coords_2_ds_vec(lmc_pxx, lmc_pxy)
		ds_vect_ohe_cls_label = self.get_ds_vec_ohe_label(ds_x, ds_y)
		return ds_vect_ohe_cls_label

	def get_ohe_cls_label_ds_vect(self, ohe_cls_label):
		"""
		What this function does is that it converts the ohe cls label into the displacement vector
		corresponding to it.
		:param ohe_cls_label: array
		:return: a tuple containign 2 ints (ds_x, ds_y)
		"""
		ds_x, ds_y = self.get_ohe_ds_vect(ohe_cls_label)
		return ds_x, ds_y

	def update_current_world_grid_loc(self, lmc_world_grid_loc):
		"""
		:param lmc_world_grid_loc: list or tuple type of len 2.
		 E.g.:
		 lmc_world_grid_loc = (lmc_world_grid_x_loc , lmc_world_grid_y_loc)
		 lmc_world_grid_loc = [lmc_world_grid_x_loc , lmc_world_grid_y_loc]
		:return:
		"""
		self.current_world_grid_loc = lmc_world_grid_loc
		self.current_world_grid_x_loc = self.current_world_grid_loc[0]
		self.current_world_grid_y_loc = self.current_world_grid_loc[1]






