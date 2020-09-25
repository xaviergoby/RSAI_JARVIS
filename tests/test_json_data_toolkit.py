



if __name__ == "__main__":
	from src.data_tools.json_data_toolkit import JSONDataToolKit
	import settings
	import os
	
	data = [[[152, 235], [342, 245], [231, 534]], [[352, 314], [163, 371], [604, 742]]]
	new_data = [[[999, 999], [999, 999], [999, 999]], [[111, 111], [111, 111], [111, 111]]]
	newer_data = [[[333, 333], [333, 333], [333, 333]], [[222, 222], [222, 222], [222, 222]]]
	str_outer_newer_data = "[[[333, 333], [333, 333], [333, 333]], [[222, 222], [222, 222], [222, 222]]]"
	str_mid_newer_data = ["[[444, 444], [444, 444], [444, 444]]", "[[333, 333], [333, 333], [333, 333]]"]
	str_inner_newer_data = [["[555, 555]", "[555, 555]", "[555, 555]"], ["[444, 444]", "[444, 444]", "[444, 444]"]]
	
	file_name = "mining.json"
	file_path = os.path.join(settings.MOUSE_MOTION_DATA_DIR, r"idle_mouse_mode_data\{0}".format(file_name))
	
	
	JSONDataToolKit.update_json_data(data, file_path)
	JSONDataToolKit.update_json_data(new_data, file_path)
	# json_file_data[0] => [[[152, 235], [342, 245], [231, 534]], [[352, 314], [163, 371], [604, 742]]]
	# json_file_data[1] => [[[999, 999], [999, 999], [999, 999]], [[111, 111], [111, 111], [111, 111]]]
	
	json_file_data = JSONDataToolKit.load_json_data(file_path)
	print(json_file_data)
	print(type(json_file_data))
	print(len(json_file_data))