import numpy as np
import settings
import os







class TrajectoryDataHandler:

	def __init__(self, data_dir_name="test_run_data"):
		self.data_dir_name = data_dir_name
		self.traj_frames = []
		self.traj_positions = []
		self.traj_data = []
		self.data_storage_dir = os.path.join(settings.DATA_DIR,
		                                     r"end_2_end_slam_data\{0}".format(self.data_dir_name))
		self.traj_frames_dir_path = os.path.join(self.data_storage_dir, "images")
		self.traj_metadata_dir_path = os.path.join(self.data_storage_dir, r"metadata\meta_data.csv")
		self.traj_frames_and_pos_arrays_data = os.path.join(self.data_storage_dir, r"frames_arrays")


	def add_traj_data(self, frame, pos):
		# pos = [int_x, int_y]
		self.traj_frames.append(frame)
		self.traj_positions.append(pos)
		self.traj_data.append([frame, pos])


