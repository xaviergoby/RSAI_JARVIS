import settings
import numpy as np
# from abc import ABC, abstractmethod
from research_and_dev.event_driven_system.mini_map import Minimap

class NavDataCollector(Minimap):

	def __init__(self, starting_loc, game_client_dims, minimap_grid_side_len=15, world_map_shape=(42, 26)):
		self.starting_loc = starting_loc
		self.game_client_dims = game_client_dims
		self.minimap_grid_side_len = minimap_grid_side_len
		self.world_map_shape = world_map_shape

		Minimap.__init__(self, self.game_client_dims, self.local_nav_sq_grid_side_len, self.starting_loc)