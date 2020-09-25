from research_and_dev.rsai_cv_navigability_mapping.world_maps.navigability_map import NavigabilityMap
from research_and_dev.rsai_cv_navigability_mapping.world_maps.world_coordinates_map import CoordinatesMap
from research_and_dev.rsai_cv_navigability_mapping.world_maps.env_coords_map import EnvironmentCoordinatesMap
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np
import random


class WorldMap:

	def __init__(self, navigability_array, top_left_origin_world_coords):
		self.navigability_array = navigability_array
		self.num_tile_rows = self.navigability_array.shape[0]
		self.num_tile_cols = self.navigability_array.shape[1]
		self.world_map_tiles_size = self.navigability_array.shape
		self.top_left_origin_world_coord = top_left_origin_world_coords
		self.navigability_map = NavigabilityMap(self.navigability_array)
		self.world_coords_map = CoordinatesMap(self.top_left_origin_world_coord, self.world_map_tiles_size)
		self.env_coords_map = EnvironmentCoordinatesMap(self.top_left_origin_world_coord, self.world_map_tiles_size)

	def get_target_tile_lmc_rand_coords(self, current_tile_world_coords, target_tile_world_coords):
		ctx, cty = current_tile_world_coords[0], current_tile_world_coords[1]
		ttx, tty = target_tile_world_coords[0], target_tile_world_coords[1]
		tt_left_px_lim = int((ttx - ctx) * 4 + 708)
		tt_right_px_lim = int((ttx - ctx) * 4 + 711)
		tt_top_px_lim = int((tty - cty) * -4 + 113)
		tt_bottom_px_lim = int((tty - cty) * -4 + 116)
		rand_lmc_x_px_coord = random.randint(tt_left_px_lim, tt_right_px_lim)
		rand_lmc_y_px_coord = random.randint(tt_top_px_lim, tt_bottom_px_lim)
		return rand_lmc_x_px_coord, rand_lmc_y_px_coord


if __name__ == "__main__":
	top_left_origin_world_coords = (3136, 3519)
	world_obstacles_array = np.load("world_array.npy")
	world_map = WorldMap(world_obstacles_array, top_left_origin_world_coords)
	# current_tile_world_coords = (3216, 3219)
	# target_tile_world_coords = (3218, 3218)
	# res = world_map.get_target_tile_lmc_rand_coords(current_tile_world_coords, target_tile_world_coords)
	# print(res)
	# 3259, 3232
	path_pos_skip_len = 4
	grid = Grid(matrix=world_obstacles_array)
	# start_pos_idxs = world_map.env_coords_map[3216, 3219]
	# end_pos_idxs = world_map.env_coords_map[3259, 3232]

	world_map_start_pos_world_coords = (3235, 3218) # (99, 301)
	start_pos_world_x_coord = world_map_start_pos_world_coords[0]
	start_pos_world_y_coord = world_map_start_pos_world_coords[1]
	start_pos_nav_coords = world_map.env_coords_map[start_pos_world_x_coord, start_pos_world_y_coord]
	start_pos_nav_x_coord = start_pos_nav_coords[0]
	start_pos_nav_y_coord = start_pos_nav_coords[1]

	start = grid.node(start_pos_nav_x_coord, start_pos_nav_y_coord)
	# end = grid.node(99, 301)
	# start = grid.node(start_pos_idxs[1], start_pos_idxs[0])
	# end = grid.node(end_pos_idxs[1], end_pos_idxs[0])
	# end = grid.node(124, 289)

	world_map_end_pos_world_coords = (3251, 3266) # (115, 253)
	end_pos_world_x_coord = world_map_end_pos_world_coords[0]
	end_pos_world_y_coord = world_map_end_pos_world_coords[1]
	end_pos_nav_coords = world_map.env_coords_map[end_pos_world_x_coord, end_pos_world_y_coord]
	end_pos_nav_x_coord = end_pos_nav_coords[0]
	end_pos_nav_y_coord = end_pos_nav_coords[1]

	end = grid.node(end_pos_nav_x_coord, end_pos_nav_y_coord)
	# end = grid.node(115, 253)

	finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
	full_path, runs = finder.find_path(start, end, grid)
	shortened_path_world_coords_list = []
	shortened_path_lmc_px_coords = []
	# current_tile_world_coords = (3216, 3219)
	current_tile_world_coords = world_map_start_pos_world_coords
	# current_tile_world_coords = (3235, 3218)
	# for path_array_idxs_pos in full_path[1:]:
	for path_array_idxs_pos in full_path[1::path_pos_skip_len]:
		path_row_idx = path_array_idxs_pos[0]
		path_col_idx = path_array_idxs_pos[1]
		# path_pos_i_world_coords = world_map.world_coords_map[path_row_idx, path_col_idx]
		path_pos_i_world_coords = world_map.world_coords_map[path_col_idx, path_row_idx]
		target_tile_world_coords = path_pos_i_world_coords
		# for path_pos_skip_i in range(path_pos_skip_len):
		# 	pass
		lmc_pos_px_coords = world_map.get_target_tile_lmc_rand_coords(current_tile_world_coords, target_tile_world_coords)
		# current_tile_world_coords = path_pos_i_world_coords

		shortened_path_world_coords_list.append(path_pos_i_world_coords)
		shortened_path_lmc_px_coords.append(lmc_pos_px_coords)
		current_tile_world_coords = path_pos_i_world_coords

	print(shortened_path_world_coords_list)
	print(len(shortened_path_world_coords_list))
	print("~"*20)
	print(shortened_path_lmc_px_coords)
	print(len(shortened_path_lmc_px_coords))

	# truncated_lmc_pos_px_coords = shortened_path_lmc_px_coords[path_pos_skip_len-1::path_pos_skip_len]
	truncated_lmc_pos_px_coords = shortened_path_lmc_px_coords[0::path_pos_skip_len]
	print("~" * 20)
	print(truncated_lmc_pos_px_coords)
	print(len(truncated_lmc_pos_px_coords))

	from src.ui_automation_tools import screen_tools
	import pyautogui
	from pyclick import HumanClicker
	import time

	screen_tools.set_window_pos_and_size()
	hc = HumanClicker()
	# delay = random.uniform(3, 4)


	for lmc_px_pos_i in shortened_path_lmc_px_coords:
		lmc_px_x_coord = lmc_px_pos_i[0]
		lmc_px_y_coord = lmc_px_pos_i[1]
		mouse_delay = random.uniform(0.4, 0.6)
		next_lmc_delay = random.uniform(3, 3.5)
		hc.move((lmc_px_x_coord, lmc_px_y_coord), mouse_delay)
		hc.click()
		time.sleep(next_lmc_delay)
		print(lmc_px_x_coord, lmc_px_y_coord)


