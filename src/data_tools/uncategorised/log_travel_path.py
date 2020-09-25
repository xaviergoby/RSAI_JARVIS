import time
import pyautogui
import json
from settings import DATA_DIR, mouse_nVirtKey_dict
import os
from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import screen_tools
from pyclick import HumanClicker

class TravelledPathLogger:

	def __init__(self, origin, destination):
		"""
		:param origin: str of the name of current location, e.g. "lumbridge"
		:param destination: str of the name of destination location, e.g. "GG_cows"
		NOTE: o2d stands for "Origin to Destination" AND o2ds stands for "Origin to DestinationS"
		"""
		self.origin = origin
		self.destination = destination
		self.paths_travelled_dir_path = os.path.join(DATA_DIR, r"paths_travelled")
		self.o2ds_travel_log_json_file_path = os.path.join(self.paths_travelled_dir_path, "{0}.json".format(self.origin))
		self.o2ds_travel_log_dict = self.load_or_create_o2ds_json_file()
		self.o2d_path_travelled_click_coords_and_delays_list = self.load_or_create_o2ds_json_file()[self.origin][self.destination] if destination is not None else None

	def create_new_empty_o2ds_travel_log_json_file(self):
		with open(self.o2ds_travel_log_json_file_path, "w") as json_file:
			empty_o2ds_travel_log_dict = {self.origin:{}}
			json.dump(empty_o2ds_travel_log_dict, json_file, indent=2)

	def check_travel_log_file_existence(self):
		if os.path.exists(self.o2ds_travel_log_json_file_path) is False:
			return False
		elif os.path.exists(self.o2ds_travel_log_json_file_path) is True:
			return True

	def load_or_create_o2ds_json_file(self):
		if self.check_travel_log_file_existence() is False:
			self.create_new_empty_o2ds_travel_log_json_file()
			self.add_dest_key_to_o2ds_log_json_file()
			return self.load_o2ds_travel_log_dict()
		else:
			o2ds_travel_log_dict = self.load_o2ds_travel_log_dict()
			o2ds_travel_log_dict_keys_list = list(o2ds_travel_log_dict[self.origin].keys())
			if self.destination not in o2ds_travel_log_dict_keys_list and self.destination is not None:
				self.add_dest_key_to_o2ds_log_json_file()
			return self.load_o2ds_travel_log_dict()

	def add_dest_key_to_o2ds_log_json_file(self):
		with open(self.o2ds_travel_log_json_file_path, "r") as json_file:
			o2ds_travel_log_dict = json.load(json_file)
		o2ds_travel_log_dict[self.origin].update_tracking({self.destination : []})
		with open(self.o2ds_travel_log_json_file_path, "w") as json_file:
			json.dump(o2ds_travel_log_dict, json_file, indent=2)

	def load_o2ds_travel_log_dict(self):
		"""
		alt name "read_o2ds_travel_log_dict()"
		:return:
		"""
		with open(self.o2ds_travel_log_json_file_path, "r") as json_file:
			o2ds_log_dict = json.load(json_file) # dict type
			# print("type of o2ds_log_dict: {0}".format(type(o2ds_log_dict)))
			return o2ds_log_dict

	def update_o2d_travelled_path_click_coords_list(self, o2d_path_travelled_click_coords_list):
		with open(self.o2ds_travel_log_json_file_path, "r") as json_file:
			o2ds_log_dict = json.load(json_file)
		o2ds_log_dict[self.origin][self.destination].append(o2d_path_travelled_click_coords_list)
		with open(self.o2ds_travel_log_json_file_path, "w") as json_file:
			json.dump(o2ds_log_dict, json_file, indent=2)


	def run_logger(self):
		o2d_path_travelled_click_coords_and_delays_list = [(390, 310, 0.0)]
		screen_tools.set_window_pos_and_size()
		delay_seconds = 5
		print("You may start in...")
		for delay_sec in range(delay_seconds, 0, -1):
			print("{0} seconds".format(delay_sec))
			time.sleep(1)
		print("Start!")
		start_time = time.time()
		print("init start_time: ", start_time)
		paused = False
		init_key_states = mouse_events_monitoring.get_init_mouse_states(mouse_nVirtKey_dict)
		while True:
			if not paused:
				mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
				if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
					end_time = time.time()
					print("end_time: ", end_time)
					time_taken = end_time - start_time  # time_taken is in seconds
					hours, rest = divmod(time_taken, 3600)
					minutes, seconds = divmod(rest, 60)
					print("Delay in seconds between clicks: {0}".format(seconds))
					start_time = time.time()
					print("new start_time: ", start_time)
					# seconds
					coords = pyautogui.position()
					x = coords[0]
					y = coords[1]
					s = seconds
					x_y_s = (x, y, s)
					o2d_path_travelled_click_coords_and_delays_list.append(x_y_s)
					print("\nClick coordinates: {0}".format(pyautogui.position()))
					print("Total number of paths logged: {0}".format(len(self.o2d_path_travelled_click_coords_and_delays_list)))
					print("Current click coordinates list: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
					print("Current click coordinates list length: {0}".format(
						len(o2d_path_travelled_click_coords_and_delays_list)))
					print("Current full_path mouse click waypoint coordinates & (delays): {0}".format(
						len(o2d_path_travelled_click_coords_and_delays_list)))
					init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)

			keys = mouse_events_monitoring.key_check()
			if len(keys) != 0:
				print("keys: {0}".format(keys))

			if 'P' in keys: # P for Pause
				if paused:
					paused = False
					print('unpaused!')
					# time.sleep(1)
					start_time = time.time()
				else:
					print('Pausing!')
					paused = True
					time.sleep(1)

			if "T" in keys: # T for Terminate after saving/writting all the data which has been collected
				print("T pressed therefore terminationg running script")
				if len(o2d_path_travelled_click_coords_and_delays_list) > 1:
					print("Saving data collected...")
					self.update_o2d_travelled_path_click_coords_list(o2d_path_travelled_click_coords_and_delays_list)
					self.o2ds_travel_log_dict = self.load_or_create_o2ds_json_file()
					self.o2d_path_travelled_click_coords_and_delays_list = self.load_or_create_o2ds_json_file()[self.origin][
																		 self.destination]
					print("Terminating...")
				break

			if "D" in keys: # D for Delete
				print("D pressed therefore deleting all the data which has been collected during this run")
				print("Deleting the following travel log data: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
				print("Deleting {0} click coords and delay data points".format(len(o2d_path_travelled_click_coords_and_delays_list)))
				o2d_path_travelled_click_coords_and_delays_list = []
				print("Current empty travel log data: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
				print("Current number of click coords and delay data points: {0}".format(len(o2d_path_travelled_click_coords_and_delays_list)))
				# time.sleep(1)
				start_time = time.time()

	def run_cnn_path_finding_data(self):
		"""
		Problem: Given an image, what is the local_x and the local_y coordinates associated with it (LMB click screen coords)?
		:return:
		"""
		client_centre_coords = 390, 310
		screen_tools.set_window_pos_and_size()
		delay_seconds = 5
		print("You may start in...")
		for delay_sec in range(delay_seconds, 0, -1):
			print("{0} seconds".format(delay_sec))
			time.sleep(1)
		print("Start!")
		start_time = time.time()
		print("init start_time: ", start_time)
		paused = False
		init_key_states = mouse_events_monitoring.get_init_mouse_states(mouse_nVirtKey_dict)
		while True:
			if not paused:
				mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
				if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
					coords = pyautogui.position()
					end_time = time.time()
					print("end_time: ", end_time)
					time_taken = end_time - start_time  # time_taken is in seconds
					hours, rest = divmod(time_taken, 3600)
					minutes, seconds = divmod(rest, 60)
					print("Delay in seconds between clicks: {0}".format(seconds))
					start_time = time.time()
					print("new start_time: ", start_time)
					# seconds
					# coords = pyautogui.position()
					x = coords[0]
					y = coords[1]
					s = seconds
					x_y_s = (x, y, s)
					o2d_path_travelled_click_coords_and_delays_list.append(x_y_s)
					print("Click coordinates: {0}".format(pyautogui.position()))
					print("Current click coordinates list: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
					# print("Current click coordinates list length: {0}".format(len(o2d_path_travelled_click_coords_and_delays_list)))
					# print("Current full_path mouse click waypoint coordinates & (delays): {0}".format(len(o2d_path_travelled_click_coords_and_delays_list)))
					init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)

			keys = mouse_events_monitoring.key_check()
			if len(keys) != 0:
				print("keys: {0}".format(keys))

			if 'P' in keys: # 4P for Pause
				if paused:
					paused = False
					print('unpaused!')
					# time.sleep(1)
					start_time = time.time()
				else:
					print('Pausing!')
					paused = True
					time.sleep(1)
				mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
				init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)

			if "T" in keys: # T for Terminate after saving/writting all the data which has been collected
				print("T pressed therefore terminationg running script")
				if len(o2d_path_travelled_click_coords_and_delays_list) > 1:
					print("Saving data collected...")
					self.update_o2d_travelled_path_click_coords_list(o2d_path_travelled_click_coords_and_delays_list)
					self.o2ds_travel_log_dict = self.load_or_create_o2ds_json_file()
					self.o2d_path_travelled_click_coords_and_delays_list = self.load_or_create_o2ds_json_file()[self.origin][
																		 self.destination]
					print("Terminating...")
				break

			if "D" in keys: # D for Delete
				print("D pressed therefore deleting all the data which has been collected during this run")
				print("Deleting the following travel log data: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
				print("Deleting {0} click coords and delay data points".format(len(o2d_path_travelled_click_coords_and_delays_list)))
				o2d_path_travelled_click_coords_and_delays_list = []
				print("Current empty travel log data: {0}".format(o2d_path_travelled_click_coords_and_delays_list))
				print("Current number of click coords and delay data points: {0}".format(len(o2d_path_travelled_click_coords_and_delays_list)))
				# time.sleep(1)
				start_time = time.time()



	def travel_o2d_path(self, o2d_path_choice_list_idx):
		clicks_coords_and_time_list_of_lists = self.o2d_path_travelled_click_coords_and_delays_list
		import random
		from uncategorised.load_json_data import cut_of_list
		truncated_list_of_lists = cut_of_list(clicks_coords_and_time_list_of_lists)
		for list_click_idx in range(len(truncated_list_of_lists[0])):
			random_click_choice_list_idx = random.randint(0, len(truncated_list_of_lists)-1)
			print(random_click_choice_list_idx)
			click_coords_and_time = truncated_list_of_lists[random_click_choice_list_idx][list_click_idx]
		# print(clicks_coords_and_time_list_of_lists)
		# return clicks_coords_and_time_list_of_lists
		# reversed_path = reversed(clicks_coords_and_time_list_of_lists[1:])
		# for click_coords_and_time in clicks_coords_and_time_list[1:]:
		# for click_coords_and_time in reversed_path:
		# for click_coords_and_time in clicks_coords_and_time_list_of_lists:
		# 	print("Sleeping for 1 second...")
		# 	time.sleep(1)
		# 	print("Awake")
			x = click_coords_and_time[0]
			y = click_coords_and_time[1]
			s = click_coords_and_time[2]
			# time.sleep(s)
			hc = HumanClicker()
			hc.move((x, y))
			hc.click()
			time.sleep(s)
			# hc.click()
			# time.sleep(s)
			# print("Sleeping for: {0} seconds...".format(s))
			# time.sleep(s)
			# print("Awake!")





if __name__ == "__main__":
	# origin = "lumbridge"
	# origin = "ge"
	#####
	# origin = "varrock_castle_yew_farm"
	# destination = "ge"
	#####
	# origin = "ge"
	# destination = "varrock_castle_yew_farm"
	#####
	# destination = "varrock"
	# destination = "varrock_castle_yew_farm"
	# destination = "ge"
	# destination = "gs_tree_farm"
	# destination = "GG_cows"
	# destination = "gs"t
	travelled_path_log = TravelledPathLogger(origin = "varrock_south_mine", destination = "varrock_east_bank")
	# travelled_path_log = TravelledPathLogger(origin = "varrock_east_bank", destination = "varrock_south_mine")
	# travelled_path_log.run_logger()
	# travelled_path_log = TravelledPathLogger(origin = "ge", destination = "varrock_castle_yew_farm")
	# print(travelled_path_log.origin)
	# print(travelled_path_log.destination)
	# print(travelled_path_log.o2ds_travel_log_dict)
	# print(travelled_path_log.o2d_path_travelled_click_coords_and_time_list)
	# travelled_path_log.run_logger()
	travelled_path_log.travel_o2d_path(0)

	# travelled_path_log1 = TravelledPathLogger(origin="varrock_castle_yew_farm", destination="ge")
	# travelled_path_log1.travel_o2d_path(0)
	# travelled_path_log2 = TravelledPathLogger(origin="ge", destination="varrock_castle_yew_farm")
	# travelled_path_log2.travel_o2d_path(0)


