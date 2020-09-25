import settings
import os
import json

	

def find_between(s, first, last):
	try:
		start = s.index(first) + len(first)
		end = s.index(last, start)
		return s[start:end]
	except ValueError:
		return ""
	

def read_label_map(label_map_file_path):
	with open(label_map_file_path, 'r') as label_map_file:
		label_map_txt_data = label_map_file.read()
	formated_label_map_str = label_map_txt_data.replace(" ", "").replace("}\n\n", "}|")
	formated_label_map_str.replace("\n", "")
	formated_label_map_str_items_list = formated_label_map_str.split("|")
	label_map_items_dict = {}
	for label_map_item_i in formated_label_map_str_items_list:
		label_map_item_i_info = find_between(label_map_item_i, "{", "}" )
		label_map_item_i_info_formated = label_map_item_i_info.rstrip().lstrip().split("\n")
		item_i_idx = label_map_item_i_info_formated[0].split(":")[-1]
		item_i_class_label_name = find_between(label_map_item_i_info_formated[1], "'", "'" )
		item_i = [item_i_idx, item_i_class_label_name]
		label_map_items_dict[int(item_i_idx)] = item_i_class_label_name
	return label_map_items_dict

if __name__ == "__main__":
	task_name = "mining"
	label_map_file_path = os.path.join(settings.OBJ_DECT_TRAINING_LABEL_MAPS_DIR,
	                                   r"tasks\{0}_label_map.pbtxt".format(task_name))
	res = read_label_map(label_map_file_path)
	print(res)