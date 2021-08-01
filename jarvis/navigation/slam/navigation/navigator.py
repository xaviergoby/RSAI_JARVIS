import time
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pyclick import HumanClicker


class Navigator:
	
	def __init__(self, world_map):
		self.world_map = world_map
		self.world_obst_grid = Grid(matrix=world_map.navigability_array)
	
	def get_full_path(self, org_node_world_coords, dest_node_world_coords, return_runs=False):
		start_pos_world_x_coord = org_node_world_coords[0]
		start_pos_world_y_coord = org_node_world_coords[1]
		start_pos_nav_x_coord, start_pos_nav_y_coord = self.world_map.env_coords_map[
			start_pos_world_x_coord, start_pos_world_y_coord]
		
		end_pos_world_x_coord = dest_node_world_coords[0]
		end_pos_world_y_coord = dest_node_world_coords[1]
		end_pos_nav_x_coord, end_pos_nav_y_coord = self.world_map.env_coords_map[
			end_pos_world_x_coord, end_pos_world_y_coord]
		
		org_node = self.world_obst_grid.node(start_pos_nav_x_coord, start_pos_nav_y_coord)
		dest_node = self.world_obst_grid.node(end_pos_nav_x_coord, end_pos_nav_y_coord)
		
		path_finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
		full_path, runs = path_finder.find_path(org_node, dest_node, self.world_obst_grid)
		if return_runs is False:
			return full_path
		else:
			return full_path, runs
	
	def shorten_path(self, path, path_pos_skip_len=None, path_pos_skip_len_rand_range=None):
		next_path_pos_idx = 0
		shortened_path_list = []
		for path_pos_idx in range(len(path)):
			if next_path_pos_idx <= len(path) - 1:
				shortened_path_list.append(path[next_path_pos_idx])
				if path_pos_skip_len is None and path_pos_skip_len_rand_range is None:
					next_path_pos_idx = next_path_pos_idx + random.randint(4, 7)
				elif path_pos_skip_len is not None and path_pos_skip_len_rand_range is None:
					next_path_pos_idx = next_path_pos_idx + path_pos_skip_len
				elif path_pos_skip_len is None and path_pos_skip_len_rand_range is not None:
					next_path_pos_idx = next_path_pos_idx + random.randint(path_pos_skip_len_rand_range[0],
					                                                       path_pos_skip_len_rand_range[1])
			else:
				return shortened_path_list
	
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
	
	def gen_nav_path_lmc_actions(self, world_map_start_pos_world_coords, nav_path):
		nav_path_lmc_actions = []
		current_tile_world_coords = world_map_start_pos_world_coords
		for path_array_idxs_pos in nav_path:
			path_row_idx = path_array_idxs_pos[0]
			path_col_idx = path_array_idxs_pos[1]
			path_pos_i_world_coords = self.world_map.world_coords_map[path_col_idx, path_row_idx]
			target_tile_world_coords = path_pos_i_world_coords
			lmc_pos_px_coords = self.get_target_tile_lmc_rand_coords(current_tile_world_coords,
			                                                         target_tile_world_coords)
			nav_path_lmc_actions.append(lmc_pos_px_coords)
			current_tile_world_coords = path_pos_i_world_coords
		return nav_path_lmc_actions
	
	def navigate(self, nav_path_lmc_actions):
		hc = HumanClicker()
		for lmc_px_pos_i in nav_path_lmc_actions:
			lmc_px_x_coord = lmc_px_pos_i[0]
			lmc_px_y_coord = lmc_px_pos_i[1]
			mouse_delay = random.uniform(0.1, 0.2)
			next_lmc_delay = random.uniform(4, 4.5)
			hc.move((lmc_px_x_coord, lmc_px_y_coord), mouse_delay)
			hc.click()
			time.sleep(next_lmc_delay)
			# print(lmc_px_x_coord, lmc_px_y_coord)
