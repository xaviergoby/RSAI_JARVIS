import json
import os

class JSONDataToolKit:
	
	# def __init__(self):
	
	@staticmethod
	def check_json_file_existence(json_file_path):
		if os.path.exists(json_file_path) is False:
			return False
		elif os.path.exists(json_file_path) is True:
			return True
	
	@staticmethod
	def load_json_data(json_file_path):
		with open(json_file_path, "r") as json_file_obj:
			json_data = json.load(json_file_obj)
		return json_data
	
	@staticmethod
	def write_json_data(list_data, json_file_path):
		with open(json_file_path, "w") as json_file_obj:
			# cmplt_list_data = []
			# cmplt_list_data.append(list_data)
			# json.dump(list_data, json_file_obj, separators=',')
			# json.dump(list_data, json_file_obj, separators=(',', ':'))
			json.dump(list_data, json_file_obj, separators=(',', ':'), indent=2)
			# json.dump(list_data, json_file_obj, separators=(',', ':'), indent=4)
		return
	
	@staticmethod
	def update_json_data(list_data, json_file_path):
		json_file_existence_bool = JSONDataToolKit.check_json_file_existence(json_file_path)
		if json_file_existence_bool is False:
			new_json_list_data = [list_data]
		else:
			old_json_list_data = JSONDataToolKit.load_json_data(json_file_path)
			new_json_list_data = old_json_list_data.copy()
			new_json_list_data.append(list_data)
		JSONDataToolKit.write_json_data(new_json_list_data, json_file_path)



# if __name__ == "__main__":
# 	import settings
#
# 	data = [[[152, 235], [342, 245], [231, 534]], [[352, 314], [163, 371], [604, 742]]]
#
# 	file_name = "mining.json"
# 	file_path = os.path.join(settings.MOUSE_MOTION_DATA_DIR, r"idle_mouse_mode_data\{0}".format(file_name))
#
#
# 	def write_to_json_file(file_path, data):
# 		with open(file_path, "w") as json_file:
# 			json.dump(data, json_file, indent=2)
	
	
	