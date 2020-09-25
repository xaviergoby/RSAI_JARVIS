from research_and_dev.misc.mini_map_objs import MiniMapGrid
from game.humanization_tools import humanize_mm_click_pos_coords
from game.humanization_tools import humanize_mm_jitter_pos_coords
from game.humanization_tools import humanize_mm_jitter_x_y_coords
import pyautogui
import time
import random
from pyclick import HumanClicker



class Navigator:

	def __init__(self):
		# self._world_map_grid = WorldMapGrid(num_of_grids=200)
		self._mini_map_grid = MiniMapGrid(mini_map_grid_square_length_radius=10)
		# self.world_maps = world_map_objs_improved.WorldMap("world_maps.json")


	def get_mm_rand_click_coords_and_durations(self, mm_path_displacement_vectors):
		# mm_path_displacement_vectors = path_obj.mm_path_displacement_vectors
		rand_click_coords_and_durations_list = []
		for mm_path_displacement_vector in mm_path_displacement_vectors:
			game_squares_traversed = abs(mm_path_displacement_vector[0]) + abs(mm_path_displacement_vector[1])
			seconds_req_to_travel = game_squares_traversed * 0.6
			mm_cell_obj = self._mini_map_grid.grid_coords_cell_objs_key_value_pair_dict[mm_path_displacement_vector]
			rand_click_coords = humanize_mm_click_pos_coords(mm_cell_obj.left_most_px,
			                                                 mm_cell_obj.top_most_px,
			                                                 mm_cell_obj.right_most_px,
			                                                 mm_cell_obj.bottom_most_px)

			rand_jittered_coords = humanize_mm_jitter_pos_coords(mm_cell_obj.left_most_px,
			                                                     mm_cell_obj.top_most_px,
			                                                     mm_cell_obj.right_most_px,
			                                                     mm_cell_obj.bottom_most_px)
			rand_click_x_coord = rand_click_coords[0]
			rand_click_y_coord = rand_click_coords[1]
			# rand_jittered_x_coord = rand_jittered_coords[0]
			# rand_jittered_y_coord = rand_jittered_coords[1]
			rand_click_coords_and_durations_list.append((rand_click_x_coord, rand_click_y_coord, seconds_req_to_travel))

		return rand_click_coords_and_durations_list


	def navigate_path(self, path_obj):
		# wm_grid_sq_coords = path_obj.game_sq_wm_path_coords
		mm_path_displacement_vectors = path_obj.mm_path_displacement_vectors
		rand_click_coords_and_durations_list = self.get_mm_rand_click_coords_and_durations(mm_path_displacement_vectors)
		hc = HumanClicker()
		delay_seconds = 5
		print("Clicking on wish in ...")
		for delay_sec in range(round(delay_seconds), 0, -1):
			print("{0} seconds".format(delay_sec))
			time.sleep(1)
		print("Clicking now!")
		# hc = HumanClicker()
		for rand_click_coords_and_duration in rand_click_coords_and_durations_list:
			delay1 = random.uniform(0.1, 0.2)
			hc.move((rand_click_coords_and_duration[0], rand_click_coords_and_duration[1]), delay1)
			print("x: {0}   &   local_y: {1}".format(rand_click_coords_and_duration[0] ,rand_click_coords_and_duration[1]))
			time.sleep(delay1)
			pyautogui.click(clicks=2)
			delay2 = random.uniform(0.01, 0.05)
			time.sleep(delay2)
			# jitter_coords = humanize_mm_jitter_x_y_coords(rand_click_coords_and_duration[0],
			#                                               rand_click_coords_and_duration[1],
			#                                               jitter_bufer=0.01)
			# x_jitter_coord = jitter_coords[0]
			# y_jitter_coord = jitter_coords[1]
			if random.random() < 0.25:
				jitter_coords = humanize_mm_jitter_x_y_coords(rand_click_coords_and_duration[0],
				                                              rand_click_coords_and_duration[1],
				                                              jitter_bufer=0.01)
				x_jitter_coord = jitter_coords[0]
				y_jitter_coord = jitter_coords[1]
				print("JITTER")
				delay3 = random.uniform(0.09, 0.15)
				hc.move((x_jitter_coord, y_jitter_coord), delay3)
				time.sleep(delay3)
				movement_duration_start_time = time.time()
				tot_delay = delay1 + delay2 + delay3
				time.sleep(rand_click_coords_and_duration[2]-tot_delay)
				movement_duration_end_time = time.time() - movement_duration_start_time
				print("Recorded duration of movement: {0}".format(movement_duration_end_time))
				print("Calculated duration of movement: {0}".format(rand_click_coords_and_duration[2]))
				print("Total duration of delays: {0}".format(tot_delay))
			else:
				movement_duration_start_time = time.time()
				tot_delay = delay1 + delay2
				time.sleep(rand_click_coords_and_duration[2] - tot_delay)
				movement_duration_end_time = time.time() - movement_duration_start_time
				print("Calculated duration of movement: {0}".format(rand_click_coords_and_duration[2]))
				print("Recorded duration of movement: {0}".format(movement_duration_end_time))
				print("Total duration of delays: {0}".format(tot_delay))


		print("Arrived at destination (gopefully)")




if __name__ == "__main__":

	from src.ui_automation_tools import screen_tools
	import settings
	from game.world.path import Path


	def test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
	                                 window_name=settings.GAME_WNDW_NAME):

		return screen_tools.set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
		                                            wndw_name=settings.GAME_WNDW_NAME)


	# true_lmd_castle_door_to_gs_door_path_coords
	Xis = [3216, 3225, 3234, 3235, 3229, 3223, 3219, 3214]
	Yis = [3219, 3219, 3219, 3226, 3233, 3239, 3244, 3245]

	# true_lmd_castle_door_to_al_kharid_gate
	# Xis = [3216, 3224, 3230, 3234, 3235, 3240, 3245, 3252, 3257, 3262, 3267]
	# Yis = [3219, 3219, 3218, 3219, 3223, 3225, 3226, 3225, 3228, 3228, 3227]


	def zip_Xis_Yis(Xis, Yis, wm_square_info_dict=None):
		wm_coords = []
		for xi, yi in zip(Xis, Yis):
			wm_square_info_dict = wm_square_info_dict
			if wm_square_info_dict is None:
				wm_coords.append((xi, yi))
			else:
				info = wm_square_info_dict[(xi, yi)]
				wm_coords.append((xi, yi, info))
		# wm_coords.append([xi, yi])
		return wm_coords


	wm_coords = zip_Xis_Yis(Xis, Yis)

	test_set_window_pos_and_size()

	# world = WorldMapGrid()
	# world.set_path_to_travel(wm_coords)

	path = Path(wm_coords)
	nav = Navigator()
	# nav.get_mm_rand_click_coords_and_durations(wm_coords)
	nav.navigate_path(path)
	# time.sleep(3)
	# print("Returning back...")
	# reversed_wm_coords = zip_Xis_Yis(list(reversed(Xis)), list(reversed(Yis)))
	# nav.travel_path(reversed_wm_coords)
	print(nav.world_map.load_world_map_json_data_dict()[(3216, 3219)])

