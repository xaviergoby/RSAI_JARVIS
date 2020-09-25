import settings
import os
import json
import numpy as np


class NavigationDataToolkit:

	def __init__(self):
		# self.bot_current_loc = None
		self.eds_frame_traj_arrays_dir_path = os.path.join(settings.EVENT_DRIVEN_SYS_DATA_DIR, r"frame_traj_arrays")
		# self.num_frame_traj_arrays = os.listdir(eds_frame_traj_arrays_dir_path)

	@property
	def num_frame_traj_arrays(self):
		num_frame_traj_arrays = os.listdir(self.eds_frame_traj_arrays_dir_path)
		return len(num_frame_traj_arrays)

	# \\TODO save_frame_grid_ds_vector_data(frame, ds_vector)
	# \\TODO save_frame_grid_ds_data(frame, ds_vector, global_origin_pnt, global_destination_pnt)
	# \\TODO save_frame_traj_data(frame, traj)
	# traj data = [dsx, dsy, prev_gx, prev_gy, current_gx, current_gy, target_gx, target_gy]
	# traj.shape => (1, 8)

	# For training:
	# traj data = [ohe_ds_label, prev_gx, prev_gy, current_gx, current_gy]
	# traj.shape => (1, 5)
	# features: frame feature data &  traj features data = [prev_gx, prev_gy, current_gx, current_gy]
	# features data shapes e.g.: (60, 60, 3) & (1, 4)
	# label data: ohe_ds_label   where ohe_ds_label.shape => (1, len(local_nav_grid_pnt_ohe_loc_label)) or (num_samples, len(local_nav_grid_pnt_ohe_loc_label))
	# output(s): one-got-encoded label data shape (1, len(local_nav_grid_pnt_ohe_loc_label)) or (num_samples, len(local_nav_grid_pnt_ohe_loc_label))

	def save_frame_traj_data(self, frame, traj):
		"""
		:param frame: a np.ndarray representation of the img frame
		:param traj: list type containing  [prev_gx, prev_gy, current_gx, current_gy, ohe_ds_label]
		:return:
		"""
		num_frame_traj_arrays = self.num_frame_traj_arrays
		current_num_frame_traj_arrays = num_frame_traj_arrays + 1
		frame_traj_array_name = "{0}.npy".format(current_num_frame_traj_arrays)
		frame_traj_array_path = os.path.join(self.eds_frame_traj_arrays_dir_path, frame_traj_array_name)
		np.save(frame_traj_array_path, [frame, traj])

	@staticmethod
	def load_bot_init_world_loc():
		"""
		:return: list containing the bots x and y grid location w.r.t globak/world grid map (Explsv OSRS Map coordnates)
		e.g. [3216, 3219]
		"""
		#data/event_driven_sys_data/location_memory.json
		json_path = os.path.join(settings.EVENT_DRIVEN_SYS_DATA_DIR, "location_memory.json")
		with open(json_path, 'r') as bot_memory_data_json:
			bot_memory_data = json.load(bot_memory_data_json)
			return bot_memory_data

	@staticmethod
	def update_loc_memory(bot_current_loc):
		json_path = os.path.join(settings.EVENT_DRIVEN_SYS_DATA_DIR, "location_memory.json")
		with open(json_path, 'w') as loc_memory_json:
			json.dump(bot_current_loc, loc_memory_json)





