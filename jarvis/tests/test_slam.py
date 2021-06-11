import numpy as np
from jarvis.navigation.slam import WorldMap
from jarvis.navigation.navigator import Navigator
from jarvis.utils import time_tools
from jarvis.utils import screen_tools
from settings import MAP_DATA_DIR
import os






top_left_origin_world_coords = (3136, 3519)
world_map_array_path = os.path.join(MAP_DATA_DIR, "world_array.npy")
world_map_array = np.load(world_map_array_path)
world_map = WorldMap(world_map_array, top_left_origin_world_coords)
navigator = Navigator(world_map)

world_map_start_pos_world_coords = (3235, 3218) # (99, 301)
# world_map_end_pos_world_coords = (3251, 3266) # (115, 253)
world_map_end_pos_world_coords = (3257, 3285) # (115, 253)

# world_map_end_pos_world_coords = (3235, 3218) # (99, 301)
# world_map_start_pos_world_coords = (3251, 3266) # (115, 253)

full_path = navigator.get_full_path(world_map_start_pos_world_coords, world_map_end_pos_world_coords)
shortened_path = navigator.shorten_path(full_path, path_pos_skip_len=4)
path_lmc_actions = navigator.gen_nav_path_lmc_actions(world_map_start_pos_world_coords, shortened_path)

screen_tools.set_window_pos_and_size()
time_tools.delay_timer(5)
navigator.navigate(path_lmc_actions)
