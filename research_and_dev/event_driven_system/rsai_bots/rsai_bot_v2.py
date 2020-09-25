import queue
import cv2
import pyautogui
import numpy as np


class RSAIBot:

	def __init__(self, bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls, bot_nav_data_handler_cls,
	             minimap, obs_percept_display_preprocessor, current_world_loc=None, events_list=None):
		self.paused = False
		self.current_world_loc = current_world_loc
		self.prev_world_loc = None
		self.events_list = [] if events_list is None else events_list
		self.events_queue = queue.Queue()
		self.bot_sensors_cls = bot_sensors_cls
		self.bot_actuators_cls = bot_actuators_cls
		self.bot_nav_grid_map_cls = bot_nav_grid_map_cls
		self.bot_nav_data_cls = bot_nav_data_handler_cls
		self.obs_percept_display_preprocessor = obs_percept_display_preprocessor
		self.minimap = minimap
		self.bot_components_cls_list = [bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls]
		# self.bot_components_cls_list = [sensor, actuators, bot_nav_grid_map_cls, bot_nav_data_cls]
		self.traj_frames_history_list = []
		self.accumulating_traj_frames_history_list = []
		self.traj_ds_vectors_history_list = []

	# @staticmethod
	def _update_run(self):
		cv2_close_key = cv2.waitKey(1) & 0xFF
		if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
			return self._end_run()

	# @staticmethod
	def _end_run(self):
		cv2.destroyAllWindows()
		return True


	def update_bot_state(self, prev_world_loc, current_world_loc):
		self.prev_world_loc = prev_world_loc
		self.current_world_loc = current_world_loc
		self.minimap.update_current_world_grid_loc((current_world_loc[0], current_world_loc[1]))


	def construct_frame_sequences(self):
		seq_frames = []
		frame_seqs = []
		for path_nav_i_idx in range(len(self.traj_frames_history_list)):
			path_nav_i_frames_seq = []
			for frame_i_idx in range(0, path_nav_i_idx+1):
				frame_i = self.traj_frames_history_list[frame_i_idx]
				path_nav_i_frames_seq.append(frame_i)
			frame_seqs.append(path_nav_i_frames_seq)
		return frame_seqs




	def run_bot(self):
		self.bot_actuators_cls.init_all_states()
		while True:
			traj_frames_history_list = []
			traj_ds_vectors_history_list = []
			accumulating_traj_frames_history_list = []
			#####
			self.sensors_percept = self.bot_sensors_cls.get_sensors_percept()
			self.bot_sensor_percept_array = self.sensors_percept[0]
			bot_sensor_percept_rgb_img = self.sensors_percept[1]
			bot_sensor_percept_array_copy = self.bot_sensor_percept_array.copy()
			self.bot_sensors_cls.display_sensor_percept(sensor_percept_array=bot_sensor_percept_array_copy, display_cursor=False)
			#####
			if self.paused is False:
				#### runtime tasks
				if self.bot_actuators_cls.lmb_clicked is True:
					print("lmb clicked!")
					lmc_mouse_screen_pos = pyautogui.position()
					lmc_px_x, lmc_px_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
					ds_vect = self.minimap.convert_px_coords_2_ds_vec(lmc_px_x, lmc_px_y)
					ds_x, ds_y = ds_vect[0], ds_vect[1]
					target_dest_world_loc = self.minimap.get_lmc_world_grid_loc(lmc_px_x, lmc_px_y)
					target_dest_world_x_loc, target_dest_world_y_loc = target_dest_world_loc[0], target_dest_world_loc[1]
					prev_world_loc = self.current_world_loc
					current_world_x_loc = target_dest_world_x_loc
					current_world_y_loc = target_dest_world_y_loc
					current_world_loc = target_dest_world_loc
					self.update_bot_state(prev_world_loc, current_world_loc)
					print(f"Previous world loc: {self.prev_world_loc}")
					print(f"ds_x: {ds_x}")
					print(f"ds_y: {ds_y}")
					print(f"Current world loc: {self.current_world_loc}")
					print(f"self.bot_sensor_percept_array.shape: {self.bot_sensor_percept_array.shape}")
					ohe_ds_vec_label = self.minimap.get_ds_vec_ohe_label(ds_x, ds_y)
					print(f"ohe_ds_vec_label: {ohe_ds_vec_label}")
					print(f"type(ohe_ds_vec_label): {type(ohe_ds_vec_label)}")
					if ohe_ds_vec_label is not None:
						self.traj_frames_history_list.append(bot_sensor_percept_array_copy)
						# traj_frames_history_list.append(bot_sensor_percept_array_copy)
						accumulated_items_list = [self.traj_frames_history_list]
						accumulating_traj_frames_history_list.append(accumulated_items_list)
						print(f"len(self.traj_frames_history_list): {len(self.traj_frames_history_list)}")
						self.traj_ds_vectors_history_list.append(ohe_ds_vec_label)
						# traj_frames_hist_list = traj_frames_history_list
						# accumulating_traj_frames_history_list.append([traj_frames_history_list])
						self.accumulating_traj_frames_history_list.append(accumulated_items_list)
						print(f"len(self.traj_ds_vectors_history_list): {len(self.traj_ds_vectors_history_list)}")
						# self.accumulating_traj_frames_history_list.append([self.traj_frames_history_list])
						print(f"len(self.accumulating_traj_frames_history_list): {len(self.accumulating_traj_frames_history_list)}")
					elif ohe_ds_vec_label is None:
						print("LMC Out of Region of Validity! Data will not be saved for this step!")
						pass
					print()



				elif self.bot_actuators_cls.P_clicked is True:
					self.paused = True
					print("paused...")

				elif self.bot_actuators_cls.T_clicked is True:
					frame_seqs = self.construct_frame_sequences()
					self.bot_nav_data_cls.save_frame_traj_data(frame_seqs, self.traj_ds_vectors_history_list)
					break
					# self.traj_frames_history_list = []
					# self.accumulating_traj_frames_history_list = []
					# self.traj_ds_vectors_history_list = []

			elif self.paused is True:
				#### runtime tasks
				if self.bot_actuators_cls.P_clicked is True:
					print("unpaused...")
					self.paused = False

			self.bot_actuators_cls.update_all_states()

			if self._update_run() is True:
				self.bot_nav_data_cls.load_bot_init_world_loc()
				self.bot_nav_data_cls.update_loc_memory(self.current_world_loc)
				break



if __name__ == "__main__":
	from research_and_dev.event_driven_system.sensors import sensors_cls
	from research_and_dev.event_driven_system.actuators import actuators_cls
	from research_and_dev.event_driven_system.nav_grids import local_main_view_nav_grid
	from research_and_dev.event_driven_system.nav_data_tools import nav_data_toolkit
	from research_and_dev.event_driven_system.mini_map import Minimap
	from src.ui_automation_tools import screen_tools
	from research_and_dev.event_driven_system.utils import img_overlay_tools

	# screen_tools.set_window_pos_and_size()

	events_list = []
	game_client_dims = (791, 591)
	nav_grid_side_len = 19
	# current_world_grid_loc = None
	current_world_grid_loc = (3216, 3219)

	minimap = Minimap(game_client_dims, nav_grid_side_len)
	roi_bbox_coords = minimap.minimap_roi_img_bbox_coords
	bot_sensors_cls = sensors_cls.Sensors(roi=roi_bbox_coords)
	bot_actuators_cls = actuators_cls.Actuators()
	bot_nav_grid_map_cls = local_main_view_nav_grid.LocalNavigationGridMap(grid_opt=1)
	bot_nav_data_cls = nav_data_toolkit.NavigationDataToolkit()
	obs_percept_display_preprocessor = img_overlay_tools.ImageOverlayTool(roi=roi_bbox_coords)

	bot = RSAIBot(bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls,
	              bot_nav_data_cls, minimap, obs_percept_display_preprocessor,
	              current_world_loc=current_world_grid_loc, events_list=events_list)
	print(f"RSAI Bot Initial Current Location: {bot.current_world_loc}")
	# bot.run_bot()

	# frame_seqs = bot.construct_frame_sequences()














