import os
import numpy as np
import settings
from matplotlib import pyplot as plt



class NavigabilityMap:
	def __init__(self, navigability_array, file_name=None):
		self.navigability_array = navigability_array if isinstance(navigability_array, np.ndarray) \
			else np.load(os.path.join(settings.MAP_DATA_DIR, navigability_array))
		self.file_name = navigability_array if isinstance(navigability_array, str) else file_name
		self.shape = self.navigability_array.shape
		self.tot_num_tiles = self.navigability_array.size
		self.num_free_tiles = np.count_nonzero(np.where(self.navigability_array == 1, 1, 0))
		self.pct_free_tiles = round((self.num_free_tiles / self.tot_num_tiles) * 100, 2)
		self.num_obstacle_tiles = np.count_nonzero(np.where(self.navigability_array == 1, 0, 1))
		self.pct_obstacle_tiles = round((self.num_obstacle_tiles / self.tot_num_tiles) * 100, 2)

	def __getitem__(self, key, verbose=0):
		val = self.navigability_array[key]
		if verbose == 1:
			print(f"Key:{key}")
			print(f"Value:{val}")
		elif verbose == 2:
			print(f"Key:{key}")
			print(f"Value:{val}")
			print(f"type(key):{type(key)}")
			print(f"type(val):{type(val)}")
		return val

	def __setitem__(self, key, value):
		self.navigability_array[key] = value

	def __repr__(self):
		world_map_nav_array_info = f"World Map Array"\
		                           f"\nFile Name: {self.file_name}"\
		                           f"\nShape:{self.shape} & # Tiles:{self.tot_num_tiles}"\
		                           f"\nFree Tiles:{self.num_free_tiles}={self.pct_free_tiles}% (1-White)"\
		                           f"\nObstacle Tiles:{self.num_obstacle_tiles}={self.pct_obstacle_tiles}% (0-Black)"
		return world_map_nav_array_info

	def vis(self):
		fig, ax = plt.subplots(figsize=(10, 8))
		ax.imshow(self.navigability_array, cmap='gray')
		ax.title.set_text(self.__repr__())
		plt.show()

	# //TODO: Check out if skimage.util.regular_grid(ar_shape, n_points) is usefull to implement

if __name__ == "__main__":
	zeros_array = np.zeros((32, 32))
	nav_map = NavigabilityMap(zeros_array)
	nav_map.vis()
	###
	world_map = NavigabilityMap("bottom_left_12854_size_6_by_2_array.npy")
	print(world_map)
	world_map.vis()
