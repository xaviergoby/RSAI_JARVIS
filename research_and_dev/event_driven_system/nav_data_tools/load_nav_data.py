import numpy as np
import os



# old = np.load
# np.load = lambda *a,**k: old(*a,**k,allow_pickle=True)
# data = np.load(r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\data\event_driven_sys_data\frame_traj_arrays\2.npy")
# print(data.shape)


def load_traj_recs_dataset(traj_recs_dataset_dir_path):
	traj_recs_nav_frame_arrays_list = []
	traj_recs_ohe_cls_labels_list = []
	old = np.load
	np.load = lambda *a, **k: old(*a, **k, allow_pickle=True)
	traj_recs_dataset_dir_file_names = os.listdir(traj_recs_dataset_dir_path)
	for traj_rec_i_file_name in traj_recs_dataset_dir_file_names:
		traj_rec_i_file_path = os.path.join(traj_recs_dataset_dir_path, traj_rec_i_file_name)
		traj_rec_i = np.load(traj_rec_i_file_path)
		# traj_rec_i_frames_arrays = traj_rec_i[0].tolist()
		traj_rec_i_frames_arrays = traj_rec_i[0]
		# traj_rec_i_ohe_labels = traj_rec_i[1].tolist()
		traj_rec_i_ohe_labels = traj_rec_i[1]
		print(f"type(traj_rec_i_frames_arrays): {type(traj_rec_i_frames_arrays)}")
		print(f"len(traj_rec_i_frames_arrays): {len(traj_rec_i_frames_arrays)}")
		print(f"traj_rec_i_frames_arrays.shape: {traj_rec_i_frames_arrays.shape}")
		print(f"type(traj_rec_i_frames_arrays[0]): {type(traj_rec_i_frames_arrays[0])}")
		print(f"len(traj_rec_i_frames_arrays[0]): {len(traj_rec_i_frames_arrays[0])}")
		print(f"type(traj_rec_i_frames_arrays[1]): {type(traj_rec_i_frames_arrays[1])}")
		print(f"len(traj_rec_i_frames_arrays[1]): {len(traj_rec_i_frames_arrays[1])}")
		# print(f"traj_rec_i_frames_arrays[0].shape: {traj_rec_i_frames_arrays[0].shape}")
		print(f"type(traj_rec_i_ohe_labels): {type(traj_rec_i_ohe_labels)}")
		print(f"traj_rec_i_ohe_labels.shape: {traj_rec_i_ohe_labels.shape}")
		print(f"type(traj_rec_i_ohe_labels[0]): {type(traj_rec_i_ohe_labels[0])}")
		print(f"len(traj_rec_i_ohe_labels[0]): {len(traj_rec_i_ohe_labels[0])}")
		# print(f"traj_rec_i_ohe_labels[0].shape: {traj_rec_i_ohe_labels[0].shape}")
		# nav_array_data_i_ohe_cls_labels_list = traj_rec_i_ohe_labels.tolist()
		# traj_recs_ohe_cls_labels_list.append(traj_rec_i_ohe_labels)
		# nav_array_data_i_list = traj_rec_i_frames_arrays.tolist()
		traj_recs_nav_frame_arrays_list.append(traj_rec_i_frames_arrays)
		traj_recs_ohe_cls_labels_list.append(traj_rec_i_ohe_labels)
	return traj_recs_nav_frame_arrays_list, traj_recs_ohe_cls_labels_list


class PathTrajectoriesDataSet:

	def __init__(self, traj_recs_dataset_dir_path=None):
		self.traj_recs_dataset_dir_path = traj_recs_dataset_dir_path
		self.traj_recs_dataset_dir_file_names = os.listdir(traj_recs_dataset_dir_path) if self.traj_recs_dataset_dir_path is not None else None
		self.traj_frames_dataset_list = []
		self.traj_way_pnts_dataset_list = []
		self._load_traj_dataset()

	def __repr__(self):
		path_traj_dataset_info = f"Number of trajectory records in dataset: {self.num_traj_paths}\n" \
								 f"Number of sequences per trajectory path recorded: {self.num_seqs_per_traj_path}"
		return path_traj_dataset_info

	@property
	def num_traj_paths(self):
		if self.traj_recs_dataset_dir_path is not None:
			return len(self.traj_recs_dataset_dir_file_names)
		else:
			return 0

	@property
	def num_seqs_per_traj_path(self):
		if self.num_traj_paths != 0:
			num_seqs_per_traj_path = [len(traj_path_i_num_seqs) for traj_path_i_num_seqs in self.traj_frames_dataset_list]
			return num_seqs_per_traj_path
		else:
			return 0

	@property
	def traj_frames_dataset(self):
		if self.traj_frames_dataset_list != 0:
			return np.array(self.traj_frames_dataset_list)
		else:
			return None

	@property
	def traj_way_pnts_dataset(self):
		if self.traj_way_pnts_dataset_list != 0:
			return np.array(self.traj_way_pnts_dataset_list)
		else:
			return None

	@property
	def frame_shape(self):
		if self.traj_frames_dataset is not None:
			return self.traj_frames_dataset[0][0][0].shape
		else:
			return None

	@property
	def ohe_way_points_shape(self):
		if self.traj_way_pnts_dataset is not None:
			return self.traj_way_pnts_dataset_list[0][0].shape
		else:
			return None

	def _load_traj_dataset(self):
		if self.traj_recs_dataset_dir_path is not None:
			old = np.load
			np.load = lambda *a, **k: old(*a, **k, allow_pickle=True)
			for traj_rec_i_file_name in self.traj_recs_dataset_dir_file_names:
				traj_rec_i_file_path = os.path.join(self.traj_recs_dataset_dir_path, traj_rec_i_file_name)
				traj_rec_i = np.load(traj_rec_i_file_path)
				traj_rec_i_frames_arrays = traj_rec_i[0]
				print(f"type(traj_rec_i_frames_arrays): {type(traj_rec_i_frames_arrays)}")
				print(f"traj_rec_i_frames_arrays.shape: {traj_rec_i_frames_arrays.shape}")
				# traj_rec_i_frames_arrays = [np.array(traj_rec_i_j[0]) for traj_rec_i_j in traj_rec_i]
				traj_rec_i_ohe_labels = traj_rec_i[1]
				# traj_rec_i_ohe_labels = [np.array(traj_rec_i_j[1]) for traj_rec_i_j in traj_rec_i]
				self.traj_frames_dataset_list.append(traj_rec_i_frames_arrays)
				self.traj_way_pnts_dataset_list.append(traj_rec_i_ohe_labels)
		else:
			pass




if __name__ == "__main__":
	nav_data_arrays_dir_path = r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\data\event_driven_sys_data\frame_traj_arrays"
	# nav_data_arrays = load_traj_recs_dataset(nav_data_arrays_dir_path)
	# # print(f"len(): {len()}")
	# # print(f"type(): {type()}")
	# # print(f".shape: {.shape}")
	# print(f"type(nav_data_arrays): {type(nav_data_arrays)}")
	# print(f"type(nav_data_arrays[0][0]): {type(nav_data_arrays[0][0])}")
	# print(f"type(nav_data_arrays[1][1]): {type(nav_data_arrays[1][1])}")
	# print(f"len(nav_data_arrays[0]): {len(nav_data_arrays[0])}")
	# print(f"len(nav_data_arrays[1]): {len(nav_data_arrays[1])}")
	# traj_pnts_dataset = nav_data_arrays[1]
	# traj_frames_dataset = nav_data_arrays[0] # ndarray
	# traj_frames_path_1 = traj_frames_dataset[0] # ndarray
	# traj_frames_path_1_seq_1 = traj_frames_path_1[1] # list
	# traj_frames_path_1_seq_1_dt_1 = traj_frames_path_1_seq_1[1] # ndarray
	# import matplotlib.pyplot as plt
	# f = traj_frames_path_1_seq_1_dt_1
	# plt.imshow(f)
	# plt.show()

	traj_path_dataset = PathTrajectoriesDataSet(nav_data_arrays_dir_path)
	traj_frames_dataset = traj_path_dataset.traj_frames_dataset
	print(traj_frames_dataset)
	print(traj_frames_dataset.shape)
	print(traj_path_dataset)
	print(traj_path_dataset.frame_shape)
	print(traj_path_dataset.ohe_way_points_shape)


	# print(f"nav_data_arrays.shape[0]: {nav_data_arrays[0].shape[0]}")
	# print(f"nav_data_arrays.shape[1]: {nav_data_arrays.shape[1]}")
	# print(fnav_data_arrays.shape: {len(nav_data_arrays)}")
	# print(fnav_data_arrays.shape[0]: nav_data_arrays.shape[0]}")
	# print(fnav_data_arrays.shape[1]: nav_data_arrays.shape[1]}")
	# print(len(nav_data_arrays))
	# print(type(nav_data_arrays[0]))
	# print(len(nav_data_arrays[0]))
	# print(len(nav_data_arrays[1]))
	# print(len(nav_data_arrays[2]))
	# print(len(nav_data_arrays[3]))
	# print(len(nav_data_arrays[4]))
	# print(len(nav_data_arrays[5]))