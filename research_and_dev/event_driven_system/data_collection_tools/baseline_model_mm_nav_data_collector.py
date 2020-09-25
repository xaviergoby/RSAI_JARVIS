import queue
import cv2
import pyautogui
from research_and_dev.event_driven_system.mini_map.minimap import Minimap
import numpy as np


class MinimapNavigationDataCollector(Minimap):

	def __init__(self, bot_sensors_cls, bot_actuators_cls, bot_nav_data_handler_cls, minimap, init_world_loc):
		# def __init__(self, game_client_dims, nav_grid_side_len=15, ):
		self.paused = False
		self.init_world_loc = init_world_loc
		self.bot_sensors_cls = bot_sensors_cls
		self.bot_actuators_cls = bot_actuators_cls
		self.bot_nav_data_cls = bot_nav_data_handler_cls
		self.minimap = minimap
		self.bot_components_cls_list = [self.bot_sensors_cls, self.bot_actuators_cls, self.bot_nav_data_cls,
		                                self.minimap]
		self.current_world_loc = init_world_loc
		self.prev_world_loc = None
		self.prev_ds_vect = None
		self.prev_ohe_ds_vec_label = None

	# self._set_init_bot_locs()
	#
	def _set_init_bot_locs(self):
		self.current_world_loc = self.bot_nav_data_cls.load_bot_init_world_loc()
		self.prev_world_loc = None
	#
	def _end_run(self):
		cv2.destroyAllWindows()
		return True

	def _update_run(self):
		cv2_close_key = cv2.waitKey(1) & 0xFF
		if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
			return self._end_run()

	def update_bot_state(self, prev_world_loc, current_world_loc):
		self.prev_world_loc = prev_world_loc
		self.current_world_loc = current_world_loc
		self.minimap.update_current_world_grid_loc((current_world_loc[0], current_world_loc[1]))

	def _set_prev_ds_vars(self, ds_vect, ohe_ds_vec_label):
		if self.prev_ds_vect is None and self.prev_ohe_ds_vec_label is None:
			self.prev_ds_vect = [0, 0]
			# x = [[] for i in range(3)]
			self.prev_ohe_ds_vec_label = [[] for i in range(len(ohe_ds_vec_label))]

	def run_bot(self):
		self.bot_actuators_cls.init_all_states()
		while True:
			#####
			self.sensors_percept = self.bot_sensors_cls.get_sensors_percept()
			self.bot_sensor_percept_array = self.sensors_percept[0]

			bot_sensor_percept_array = self.bot_sensor_percept_array.copy()
			self.bot_sensors_cls.display_sensor_percept(sensor_percept_array=bot_sensor_percept_array,
			                                            display_cursor=True)
			#####
			if self.paused is False:
				#### runtime tasks
				if self.bot_actuators_cls.lmb_clicked is True:
					print("lmb clicked!")
					lmc_mouse_screen_pos = pyautogui.position()
					lmc_px_x, lmc_px_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
					# ds_x, ds_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
					# print(f"ds_x: {ds_x} & ds_y: {ds_y}")
					# lmc_px_x, lmc_px_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
					# local_grid_pnt_x, local_grid_pnt_y = self.minimap.convert_px_coords_2_ds_vec(lmc_px_x, lmc_px_y)
					ds_vect = self.minimap.convert_px_coords_2_ds_vec(lmc_px_x, lmc_px_y)
					ds_x, ds_y = ds_vect[0], ds_vect[1]
					target_dest_world_loc = self.minimap.get_lmc_world_grid_loc(lmc_px_x, lmc_px_y)
					target_dest_world_x_loc, target_dest_world_y_loc = target_dest_world_loc[0], target_dest_world_loc[
						1]
					prev_world_loc = self.current_world_loc
					current_world_x_loc = target_dest_world_x_loc
					current_world_y_loc = target_dest_world_y_loc
					current_world_loc = target_dest_world_loc
					self.update_bot_state(prev_world_loc, current_world_loc)
					# global_grid_pnt_x, global_grid_pnt_y = self.minimap.get_lmc_world_grid_loc(lmc_px_x, lmc_px_y)
					# self.nav_data_toolkit_cls.save_frame_traj_data(self.bot_sensor_percept_array, [ds_x, ds_y])
					# self.minimap.update_current_world_grid_loc((init_world_coords[0], init_world_coords[1]))
					# grid_pnt_x, grid_pnt_y = self.bot_nav_grid_map_cls.get_lmc_nn_grid_pnt(lmc_px_x, lmc_px_y)
					print(f"Previous world loc: {self.prev_world_loc}")
					print(f"ds_x: {ds_x}")
					print(f"ds_y: {ds_y}")
					print(f"Current world loc: {self.current_world_loc}")
					print(f"self.bot_sensor_percept_array.shape: {self.bot_sensor_percept_array.shape}")
					ohe_ds_vec_label = self.minimap.get_ds_vec_ohe_label(ds_x, ds_y)
					print(f"ohe_ds_vec_label: {ohe_ds_vec_label}")
					print(f"type(ohe_ds_vec_label): {type(ohe_ds_vec_label)}")
					# self.nav_data_toolkit_cls.save_frame_traj_data(self.bot_sensor_percept_array, [ds_x, ds_y])
					self.bot_nav_data_cls.save_frame_traj_data(self.bot_sensor_percept_array, ohe_ds_vec_label)
				# print(f"global_grid_pnt_x: {init_world_coords[0]}")
				# print(f"global_grid_pnt_y: {init_world_coords[1]}")
				# bot_current_x_coord = self.init_world_coords[0] + ds_x
				# bot_current_y_coord = self.init_world_coords[1] + ds_y
				# self.init_world_coords = [bot_current_x_coord, bot_current_y_coord]
				# self.nav_data_toolkit_cls.update_loc_memory(self.init_world_coords)
				# print(f"bot_current_x_coord: {bot_current_x_coord}")
				# print(f"bot_current_y_coord: {bot_current_y_coord}")



				elif self.bot_actuators_cls.P_clicked is True:
					self.paused = True
					print("paused...")

				elif self.bot_actuators_cls.T_clicked is True:
					pass
			# np.s
			# print("paused...")
			####

			elif self.paused is True:
				#### runtime tasks
				if self.bot_actuators_cls.P_clicked is True:
					print("unpaused...")
					self.paused = False
			####p

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

	screen_tools.set_window_pos_and_size()

	# events_list = []
	# game_client_dims = (791, 591)
	game_client_dims = (783, 560)
	nav_grid_side_len = 15
	# current_world_grid_loc = None
	current_world_grid_loc = (3216, 3219)
	minimap = Minimap(game_client_dims, nav_grid_side_len)
	minimap.current_world_grid_loc = current_world_grid_loc
	roi_bbox_coords = minimap.minimap_roi_img_bbox_coords
	bot_sensors_cls = sensors_cls.Sensors(roi=roi_bbox_coords)
	bot_actuators_cls = actuators_cls.Actuators()
	# bot_nav_grid_map_cls = local_main_view_nav_grid.LocalNavigationGridMap(grid_opt=1)
	nav_data_toolkit_cls = nav_data_toolkit.NavigationDataToolkit()
	# obs_percept_display_preprocessor = img_overlay_tools.ImageOverlayTool(roi=roi_bbox_coords)
	bot = MinimapNavigationDataCollector(bot_sensors_cls, bot_actuators_cls, nav_data_toolkit_cls, minimap, (3216, 3219))
	print(f"RSAI Bot Initial Current Location: {bot.current_world_loc}")
	bot.run_bot()
