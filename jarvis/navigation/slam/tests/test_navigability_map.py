import os
import numpy as np
from matplotlib import pyplot as plt
import settings
from jarvis.navigation.slam.world_maps.navigability_map import NavigabilityMap

def vis_diff_world_map_nav_arrays(wm_nav_array_1, wm_nav_array_2):
	wm_nav_array_1_obj = NavigabilityMap(wm_nav_array_1)
	wm_nav_array_2_obj = NavigabilityMap(wm_nav_array_2)
	ax[0].imshow(wm_nav_array_1_obj.navigability_array, cmap='gray')
	ax[1].imshow(wm_nav_array_2_obj.navigability_array, cmap='gray')
	ax[0].title.set_text(wm_nav_array_1_obj)
	ax[1].title.set_text(wm_nav_array_2_obj)
	plt.show()

if __name__ == "__main__":
	world_map_array_file_path = os.path.join(settings.MAP_DATA_DIR, "world_array.npy")
	world_map_obstacles_array_file_path = os.path.join(settings.MAP_DATA_DIR, "world_obstacles_array.npy")
	bl_12854_6by2_array_file_path = os.path.join(settings.MAP_DATA_DIR, "bottom_left_12854_size_6_by_2_array.npy")

	world_map_array = np.load(world_map_array_file_path)
	world_map_obstacles_array = np.load(world_map_obstacles_array_file_path)
	bl_12854_6by2_array = np.load(bl_12854_6by2_array_file_path)

	world_map_array_navigability = NavigabilityMap(world_map_array)
	world_map_obstacles_array_navigability = NavigabilityMap(world_map_obstacles_array)
	bl_12854_6by2_array_navigability = NavigabilityMap(bl_12854_6by2_array)

	print(world_map_array_navigability.navigability_array.shape) # (384, 128)
	print(world_map_obstacles_array_navigability.navigability_array.shape) # (32, 32)
	print(bl_12854_6by2_array_navigability.navigability_array.shape) # (384, 128)

	diff = world_map_array_navigability.navigability_array == bl_12854_6by2_array_navigability.navigability_array
	# diff_present = np.where(diff == False)
	# diff_abscent = np.where(diff == True)
	# diff_cmplt_false = np.where(diff == False, 1, 0)
	# diff_cmplt_true = np.where(diff == True, 1, 0)
	# diff_cmplt_false = np.where(diff == False, 0)
	# diff_cmplt_true = np.where(diff == True, 1)
	print(world_map_array_navigability.navigability_array == bl_12854_6by2_array_navigability.navigability_array)
	print(type(diff))
	# print(bl_12854_6by2_array_navigability.navigability_array)


	fig, ax = plt.subplots(1, 2, figsize=(10, 8))
	ax[0].imshow(world_map_array_navigability.navigability_array, cmap='gray')  # row=0, col=0
	ax[1].imshow(bl_12854_6by2_array_navigability.navigability_array, cmap='gray')  # row=0, col=1
	ax[0].title.set_text("world_array.npy")
	ax[1].title.set_text("bottom_left_12854_size_6_by_2_array.npy")


	print(world_map_array_navigability)
	world_map_array_navigability.vis()

	world_map = NavigabilityMap("bottom_left_12854_size_6_by_2_array.npy")
	print(world_map)
	world_map.vis()

	vis_diff_world_map_nav_arrays("world_array.npy", "bottom_left_12854_size_6_by_2_array.npy")
