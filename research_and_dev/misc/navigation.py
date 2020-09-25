from research_and_dev.misc.mini_map_objs import MiniMapGrid
from research_and_dev.misc import world_map_objs_improved
from research_and_dev.misc.world_map_objs import WorldMapPath, WorldMapGrid
from game.humanization_tools import humanize_mm_click_pos_coords
from game.humanization_tools import humanize_mm_jitter_pos_coords
from game.humanization_tools import humanize_mm_jitter_x_y_coords
import pyautogui
import time
import random
from pyclick import HumanClicker


# Xis = [3216, 3225, 3234, 3235, 3229, 3223, 3219, 3214]
# Yis = [3219, 3219, 3219, 3226, 3233, 3239, 3244, 3245]
#
# paths = {(3216, 3219): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_castle", "square_objs_occupied": []},
# 		 (3225, 3219): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3234, 3219): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3235, 3226): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3229, 3233): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3223, 3239): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3219, 3244): {"area_label_name": "Lumbridge", "region_label_id": 12850,
# 						"square_confinement_name": "lumbridge_walls", "square_objs_occupied": []},
# 		 (3214, 3245): {"area_label_name": "Lumbridge", "region_label_id": 12850, "square_confinement_name": None,
# 						"square_objs_occupied": []}}
#
#
# def zip_Xis_Yis(Xis, Yis, wm_square_info_dict=None):
# 	wm_coords = []
# 	for xi, yi in zip(Xis, Yis):
# 		wm_square_info_dict = wm_square_info_dict
# 		if wm_square_info_dict is None:
# 			wm_coords.append((xi, yi))
# 		else:
# 			info = wm_square_info_dict[(xi, yi)]
# 			wm_coords.append((xi, yi, info))
# 	# wm_coords.append([xi, yi])
# 	return wm_coords
#
#
# wm_coords = zip_Xis_Yis(Xis, Yis)
#
# world = WorldMapGrid()
# world.set_path_to_travel(wm_coords)


class Navigation:

	def __init__(self):
		self._world_map_grid = WorldMapGrid(num_of_grids=200)
		self._mini_map_grid = MiniMapGrid(mini_map_grid_square_length_radius=10)
		self.world_map = world_map_objs_improved.WorldMap("world_maps.json")

	# self.path_to_travel = None
	# self.travelling_path = False

	def set_up_mm_virtual_env(self):
		self._mini_map_grid.create_mm_grid_cells_coords()

	def set_up_world_map_grid(self):
		self.world_map.gen_new_world_map_grid()

	def get_mm_rand_click_coords_and_durations(self, wm_grid_sq_coords):
		self._world_map_grid.set_travell_path(wm_grid_sq_coords)
		for world_map_grid_pos_coords in wm_grid_sq_coords:
			# grid_objs_dict = self.world_maps.load_world_map_json_data_dict()
			self.world_map.load_world_map_json_data_dict()[world_map_grid_pos_coords].navigable = True
			self.world_map.load_world_map_json_data_dict()[world_map_grid_pos_coords].vissited = True
		# wm_path_displacement_vectors = self._world_map_grid.get_current_wm_travell_path_displacement_vectors()
		wm_path_obj = WorldMapPath(wm_grid_sq_coords)
		mm_path_displacement_vectors = self._world_map_grid.get_mm_path_displacement_vectors_via_wm_path_obj(
			wm_path_obj)
		self.set_up_mm_virtual_env()
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
			rand_jittered_x_coord = rand_jittered_coords[0]
			rand_jittered_y_coord = rand_jittered_coords[1]
			rand_click_coords_and_durations_list.append((rand_click_x_coord, rand_click_y_coord, seconds_req_to_travel))

		return rand_click_coords_and_durations_list

	def travel_path(self, wm_grid_sq_coords):
		rand_click_coords_and_durations_list = self.get_mm_rand_click_coords_and_durations(wm_grid_sq_coords)
		# rand_jittered_coords = humanize_mm_jitter_pos_coords(mm_cell_obj.left_most_px,
		#                                                      mm_cell_obj.top_most_px,
		#                                                      mm_cell_obj.right_most_px,
		#                                                      mm_cell_obj.bottom_most_px)
		# rand_jittered_x_coord = rand_jittered_coords[0]
		# rand_jittered_y_coord = rand_jittered_coords[1]
		# delay_seconds = random.uniform(1, 2)
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
			print("local_x: {0}   &   local_y: {1}".format(rand_click_coords_and_duration[0] ,rand_click_coords_and_duration[1]))
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

# humanize_mm_click_pos_coords(mm_cell_obj.top_most_px)
# humanize_mm_click_pos_coords(mm_cell_obj.right_most_px)
# humanize_mm_click_pos_coords(mm_cell_obj.bottom_most_px)
# print("mm_path_displacement_vectors: ", mm_path_displacement_vectors)
# print("mm_path_displacement_vectors[2]: ", mm_path_displacement_vectors[2])
# print("wm_path_displacement_vector: ", wm_path_displacement_vector)
# self.set_up_mm_virtual_env()
# mm_grid_cell_obj = self._mini_map_grid.grid_coords_cell_objs_key_value_pair_dict[wm_path_displacement_vector]
# print("wm_path_displacement_vector: {0}".format(wm_path_displacement_vector))
# print("mm_grid_cell_obj: {0}".format(mm_grid_cell_obj))
# print("mm_grid_cell_obj.local_x: {0}".format(mm_grid_cell_obj.local_x))
# print("mm_grid_cell_obj.local_y: {0}".format(mm_grid_cell_obj.local_y))
# print("mm_grid_cell_obj.left_most_px: {0}".format(mm_grid_cell_obj.left_most_px))
# print("mm_grid_cell_obj.top_most_px: {0}".format(mm_grid_cell_obj.top_most_px))
# print("mm_grid_cell_obj.right_most_px: {0}".format(mm_grid_cell_obj.right_most_px))
# print("mm_grid_cell_obj.bottom_most_px: {0}".format(mm_grid_cell_obj.bottom_most_px))
# grid_coords_cell_objs_key_value_pair_dict
# wm_path_displacement_vectors = self._current_wm_path.get_current_wm_travell_path_displacement_vectors()


if __name__ == "__main__":

	from src.ui_automation_tools import screen_tools
	import settings


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

	nav = Navigation()
	# nav.get_mm_rand_click_coords_and_durations(wm_coords)
	nav.travel_path(wm_coords)
	# time.sleep(3)
	# print("Returning back...")
	# reversed_wm_coords = zip_Xis_Yis(list(reversed(Xis)), list(reversed(Yis)))
	# nav.travel_path(reversed_wm_coords)
	print(nav.world_map.load_world_map_json_data_dict()[(3216, 3219)])

