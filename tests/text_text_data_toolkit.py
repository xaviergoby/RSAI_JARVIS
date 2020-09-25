
if __name__ == "__main__":
	from src.data_tools.text_data_toolkit import TextDataToolKit
	import settings
	import os
	
	data = [[[152, 235], [342, 245], [231, 534]], [[352, 314], [163, 371], [604, 742]]]
	new_data = [[[999, 999], [999, 999], [999, 999]], [[111, 111], [111, 111], [111, 111]]]
	newer_data = [[[333, 333], [333, 333], [333, 333]], [[222, 222], [222, 222], [222, 222]]]
	str_outer_newer_data = "[[[333, 333], [333, 333], [333, 333]], [[222, 222], [222, 222], [222, 222]]]"
	str_mid_newer_data = ["[[444, 444], [444, 444], [444, 444]]", "[[333, 333], [333, 333], [333, 333]]"]
	str_inner_newer_data = [["[555, 555]", "[555, 555]", "[555, 555]"], ["[444, 444]", "[444, 444]", "[444, 444]"]]
	
	file_name = "mining.txt"
	file_path = os.path.join(settings.MOUSE_MOTION_DATA_DIR, r"idle_mouse_mode_data\{0}".format(file_name))
	
	TextDataToolKit.update_text_file_data(data, file_path)
	TextDataToolKit.update_text_file_data(new_data, file_path)
	TextDataToolKit.update_text_file_data(newer_data, file_path)
	
	# text_data = TextDataToolKit.load_text_data(file_path)
	text_data = TextDataToolKit.load_text_data_as_list(file_path)
	