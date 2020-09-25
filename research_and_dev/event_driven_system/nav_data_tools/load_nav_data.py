import numpy as np
import os



# old = np.load
# np.load = lambda *a,**k: old(*a,**k,allow_pickle=True)
# data = np.load(r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\data\event_driven_sys_data\frame_traj_arrays\2.npy")
# print(data.shape)


def load_nav_arrays_data(nav_data_arrays_dir_path):
	nav_data_arrays_list = []
	nav_array_data_ohe_cls_labels_list = []
	old = np.load
	np.load = lambda *a, **k: old(*a, **k, allow_pickle=True)
	nav_arrays_data_dir_contents_names = os.listdir(nav_data_arrays_dir_path)
	for nav_array_data_file_name_i in nav_arrays_data_dir_contents_names:
		nav_array_data_file_path_i = os.path.join(nav_data_arrays_dir_path, nav_array_data_file_name_i)
		nav_array_data_and_label_i = np.load(nav_array_data_file_path_i)
		nav_array_data_i = nav_array_data_and_label_i[0]
		nav_array_data_i_ohe_cls_labels = nav_array_data_and_label_i[1]
		nav_array_data_i_ohe_cls_labels_list = nav_array_data_i_ohe_cls_labels.tolist()
		nav_array_data_ohe_cls_labels_list.append(nav_array_data_i_ohe_cls_labels_list)
		nav_array_data_i_list = nav_array_data_i.tolist()
		nav_data_arrays_list.append(nav_array_data_i_list)
	return nav_data_arrays_list, nav_array_data_ohe_cls_labels_list




if __name__ == "__main__":
	nav_data_arrays_dir_path = r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\data\event_driven_sys_data\frame_traj_arrays"
	nav_data_arrays = load_nav_arrays_data(nav_data_arrays_dir_path)[0]
	print(len(nav_data_arrays))
	print(type(nav_data_arrays[0]))
	print(len(nav_data_arrays[0]))
	print(len(nav_data_arrays[1]))
	print(len(nav_data_arrays[2]))
	print(len(nav_data_arrays[3]))
	print(len(nav_data_arrays[4]))
	print(len(nav_data_arrays[5]))