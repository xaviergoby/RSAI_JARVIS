import json


def load_json_data(json_file_path):
	with open(json_file_path, "r") as json_file_obj:
		json_data = json.load(json_file_obj)
	return json_data

def get_all_dest_paths_for_origin(paths_dict, destination):
	origin = list(paths_dict.keys())[0]
	dest_paths_list = paths_dict[origin][destination]
	return dest_paths_list


def normalize(_d, to_sum=True, copy=True):
	# d is a (n local_x dimension) np array
	d = _d if not copy else np.copy(_d)
	d -= np.min(d, axis=0)
	d /= (np.sum(d, axis=0) if to_sum else np.ptp(d, axis=0))
	return d


def cut_of_list(list_of_lists):
	shortened_list_of_lists = []
	all_list_lens = [len(l) for l in list_of_lists]
	shortest_list_len = min(all_list_lens)
	for l in list_of_lists:
		l_len = len(l)
		if l_len > shortest_list_len:
			l = l[:shortest_list_len]
			shortened_list_of_lists.append(l)
		else:
			shortened_list_of_lists.append(l)
	return shortened_list_of_lists



if __name__ == "__main__":
	import matplotlib
	matplotlib.use("TkAgg")  # Do this before importing pyplot!
	import matplotlib.pyplot as plt
	import numpy as np

	# json_file_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_json\lumbridge.json"
	# data = load_json_data(json_file_path)
	# origin = "lumbridge"
	origin = "varrock_castle_yew_farm"
	# destination = "gs_tree_farm"
	destination = "ge"
	json_file_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\{0}.json".format(origin)
	data = load_json_data(json_file_path)
	all_o2d_paths_list = get_all_dest_paths_for_origin(data, destination)
	all_o2d_paths_truncated_list = cut_of_list(all_o2d_paths_list)
	print(data)
	print("Number of travelled paths recorded: {0}".format(len(data[origin][destination])))
	print("Number of travelled paths recorded: {0}".format(len(all_o2d_paths_list)))


	# x_test = np.array([[4,2,7,2,5], [2,7,4,2,8]]).T
	# y_test = np.array([[1,5,2,7,3], [2,7,3,6,3]]).T
	data_array = np.array(all_o2d_paths_truncated_list)
	x_y_coords = data_array[:, :, :2]
	x_coords = data_array[:, :, 0].T
	y_coords = data_array[:, :, 1].T
	delays = data_array[:, :, 2].T
	normalized_coords = x_y_coords / np.sqrt(np.sum(x_y_coords ** 2))
	normalized_x_coords = x_coords / np.sqrt(np.sum(x_coords ** 2))
	normalized_y_coords = y_coords / np.sqrt(np.sum(y_coords ** 2))
	fig, ax = plt.subplots()
	ax.plot(x_coords, y_coords)
	# ax.scatter(x_coords, y_coords)
	ax.xaxis.tick_top()
	ax.invert_yaxis()
	ax.set_xlim(left=8, right=791)
	ax.set_ylim(bottom=591, top=31)
	plt.grid(True)
	# plt.grid(b=True, which='minor', color='r', linestyle='--')
	plt.show()