import json
import os
import ast

class TextDataToolKit:
	
	# def __init__(self):
	
	@staticmethod
	def check_text_file_existence(text_file_path):
		if os.path.exists(text_file_path) is False:
			return False
		elif os.path.exists(text_file_path) is True:
			return True
	
	@staticmethod
	def load_text_data(text_file_path):
		with open(text_file_path, "r") as text_file_obj:
			text_data = text_file_obj.read()
			return text_data
		
	@staticmethod
	def load_text_data_as_list(text_file_path):
		text_file_lines_list = []
		with open(text_file_path, "r") as text_file_obj:
			text_file_lines = text_file_obj.readlines()
			for text_file_line in text_file_lines:
				text_file_line_data = ast.literal_eval(text_file_line)
				text_file_lines_list.append(text_file_line_data)
		return text_file_lines_list
		
	@staticmethod
	def write_text_file_data(new_text_file_line_data, text_file_path):
		with open(text_file_path, "w") as text_file_obj:
			text_file_obj.write(new_text_file_line_data)
		
	@staticmethod
	def append_text_file_data(new_text_file_line_data, text_file_path):
		with open(text_file_path, "a") as text_file_obj:
			text_file_obj.write("\n")
			text_file_obj.write(new_text_file_line_data)
			
	@staticmethod
	def update_text_file_data(new_text_file_line_data, text_file_path):
		new_text_file_line_data_str_format = "{0}".format(str(new_text_file_line_data))
		if TextDataToolKit.check_text_file_existence(text_file_path) is False:
			TextDataToolKit.write_text_file_data(new_text_file_line_data_str_format, text_file_path)
		else:
			TextDataToolKit.append_text_file_data(new_text_file_line_data_str_format, text_file_path)
			
		