import json
import pickle
from pathlib import Path
import glob
from settings import *
import os
from pathlib import Path


def get_project_root_dir_path():
	return Path(__file__).parent.parent.parent


def get_most_recent_data_file_name(path):
	r"""
	:param path: the full full_path to the directory of interest
	NOTE the format/style/template/convention oa provided full_path must respect (see e.g. below)
	e.g. full_path = r"obj_dect\tasks\wc" or full_path = r"obj_dect\bank"
	:return:str of the full full_path of the most recently created file present
	in the directory searched
	e.g. full_path= r"obj_dect\tasks\wc\images" returns "polar bear.jpg"
	"""
	fixed_path = path + r"\*"
	full_path = os.path.join(DATA_DIR, fixed_path)
	list_of_files = glob.glob(full_path)
	if len(list_of_files) == 0:
		return False
	else:
		latest_file_full_path = max(list_of_files, key=os.path.getctime)
		file_name = Path(latest_file_full_path).name
		return file_name


def get_last_data_file_name(path):
	full_path = os.path.join(DATA_DIR, path)
	list_of_files = os.listdir(full_path)
	if len(list_of_files) == 0:
		return False
	else:
		last_file = os.listdir(full_path)[-1]
		return last_file


def get_img_id_from_file_name(img_file_name):
	"""
	:param img_file_name:
	:return: str of the id associated/in the imag file name
	"""
	img_file_base_name = Path(img_file_name).stem
	latest_img_idx = img_file_base_name.split("_")[-1]
	return latest_img_idx


def get_file_stem_name(file_name_with_ext):
	"""
	:param file_name_with_ext: str of the file name with its extension
	e.g. "bronze_pickaxe.PNG"
	:return: str of the file name without its extension
	e.g. "bronze_pickaxe"
	"""
	file_name_without_extension = file_name_with_ext.split(".")[0]
	return file_name_without_extension


def get_img_file_name_vals(img_file_name, return_type=None):
	"""
	:param img_file_name: str of the complete file name (so with its exntesion e.g. .jpg)
	e.g. "wc_obj_dect_15,png" or e.g. "slaying_obj_dect_125.jpg" or e.g. "lumbridge_to_bridge_path_img_412_366.jpg"
	:return: str of the id associated/in the imag file name. If there is only one value in the name of the file then
	it is returned as an str by default else as an int if return_type = "int". If there are more 2 or more values
	in the name of the file then a list of str's or int's is returned!
	e.g.
	img_file_name =
	e.g. "wc_obj_dect_15,png" or e.g. "slaying_obj_dect_125.jpg" or e.g. "lumbridge_to_bridge_path_img_412_366.jpg"
	returns the following by def:
	e.g. "15" or e.g. "125" or e.g. ["412", "366"]
	"""
	img_file_base_name = Path(img_file_name).stem
	img_file_name_vals_list = []
	split_img_file_name = img_file_base_name.split("_")
	for split_str in split_img_file_name:
		if split_str.isalpha() is False:
			if return_type is None:
				img_file_name_vals_list.append(split_str)
			elif return_type is "int":
				img_file_name_vals_list.append(int(split_str))
		else:
			continue
	if len(img_file_name_vals_list) == 1:
		return img_file_name_vals_list[0]
	elif len(img_file_name_vals_list) > 1:
		return img_file_name_vals_list


def get_dir_contents_list(dir_path, without_ext=False):
	"""
	:param dir_path: windows format str full full_path
	:return: a list of str names of each of the files contained within the dir located @ dir_path.
	The files names incl. their extension, e.g. "bones.PNG"
	"""
	dir_contents_list = os.listdir(dir_path)
	if without_ext is True:
		dir_contents_list = list(map(get_file_stem_name, dir_contents_list))
	return dir_contents_list


def get_dir_path_with_task_name(task_name):
	"""
	NOTE: THIS IS A BADLY CODED FUNCTION BECAUSE OF THE PRESENCE OF A HARDCODED PATH
	THIS FUNCTION IS NOT BEING USED AND SHOULD BE AVOIDED!
	:param task_name:
	:return:
	"""
	path_to_tasks = os.path.join(DATA_DIR, r"post_bboxed_dir\tasks\{0}".format(task_name))
	return path_to_tasks


def check_dir_or_file_existence(windows_format_full_file_or_dir_path):
	r"""
	:param windows_format_full_file_or_dir_path: str of the Windows format (so with r'\' instead of /) full full_path to the dir
	e.g. r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge\images\lumbridge_to_bridge_path_img_395_847.jpg"
	:return: True if the directory already exists else False
	"""
	pass
	if os.path.exists(windows_format_full_file_or_dir_path) is True:
		return True
	elif os.path.exists(windows_format_full_file_or_dir_path) is False:
		return False


def make_dir(windows_format_full_file_or_dir_path):
	r"""
	For creating a new directory which does not already exist!
	:param windows_format_full_file_or_dir_path:
	e.g. r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge"
	:return:
	If the dir located @ the full_path provided already exists then the following exception error is raised:
	FileExistsError: [WinError 183] Cannot create a file when that file already exists:
	"""
	path = Path(windows_format_full_file_or_dir_path)
	path.mkdir()


def make_dir_if_nonexistent(windows_format_full_dir_path):
	"""
	This function is for simplifying the process of creating a new directory for a given file full_path
	for which no directory exists.
	:param windows_format_full_dir_path: windows format str full full_path
	:return:
	"""
	if check_dir_or_file_existence(windows_format_full_dir_path) is False:
		# print("dir does not exist... creating it now")
		make_dir(windows_format_full_dir_path)
	elif check_dir_or_file_existence(windows_format_full_dir_path) is True:
		# print("dir exists already")
		pass


def check_file_path_existence(file_path):
	if os.path.exists(file_path) is False:
		return False
	elif os.path.exists(file_path) is True:
		return True


def create_new_empty_json_file(json_file_path):
	with open(json_file_path, "w") as json_file:
		empty_dict = {}
		json.dump(empty_dict, json_file, indent=2)


def create_new_json_file(json_file_path, data):
	with open(json_file_path, "w") as json_file:
		json.dump(data, json_file, indent=2)


def load_json_data_dict(json_file_path):
	with open(json_file_path, "r") as json_file:
		json_data_dict = json.load(json_file) # dict type
		return json_data_dict


def write_to_json_file(json_file_path, data):
	with open(json_file_path, "w") as json_file:
		json.dump(data, json_file, indent=2)

def create_new_pickled_json(pickled_json_file_path, data):
	with open(pickled_json_file_path, 'wb') as outfile:
		pickle.dump(data, outfile)


def load_pickled_json(pickled_json_file_path):
	with open(pickled_json_file_path, 'rb') as outfile:
		dict_data = pickle.load(outfile)
		return dict_data


def update_pickled_json(pickled_json_file_path, data):
	with open(pickled_json_file_path, 'wb') as outfile:
		pickle.dump(data, outfile)




if __name__ == "__main__":
	# r"C:\Users\XGOBY\RSAIBot\data\pre_bboxed_data\tasks\slaying\cows\images\slaying_obj_dect_18.jpg"


	existing_full_file_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge\images\lumbridge_to_bridge_path_img_395_847.jpg"
	existing_full_dir_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge"
	nonexisting_full_file_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge\images\lumbridge_to_bridge_path_img_1000_1000.jpg"
	nonexisting_full_dir_path = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\cambridge2oxford"
	nonexisting_full_dir_path2 = r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\delfttodenhaag"

	print(check_dir_or_file_existence(existing_full_file_path))
	print(check_dir_or_file_existence(nonexisting_full_file_path))
	print(check_dir_or_file_existence(existing_full_dir_path))
	print(check_dir_or_file_existence(nonexisting_full_dir_path))
	# make_new_dir(nonexisting_full_dir_path)
	vals1 = get_img_file_name_vals(r"C:\Users\XGOBY\RSAIBot\data\pre_bboxed_data\tasks\slaying\cows\images\slaying_obj_dect_18.jpg", return_type="int")
	vals2 = get_img_file_name_vals(r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge\images\lumbridge_to_bridge_path_img_395_847.jpg", return_type="int")
	print(vals1)
	print(vals2)
	# print(get_img_file_name_vals(get_most_recent_data_file_name(r"C:\Users\XGOBY\RSAIBot\data\paths_travelled\path_finding_images\lumbridge2bridge\images")))
	# make_dir_if_nonexistent(nonexisting_full_dir_path2)
	print(get_dir_contents_list(r"C:\Users\Xavier\RSAI_JARVIS\data\obj_dect\inv_items\images"))
	print(get_dir_contents_list(r"C:\Users\Xavier\RSAI_JARVIS\data\obj_dect\inv_items\images", without_ext=True))

