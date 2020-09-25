import os
import subprocess
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import settings


class TasksXMLToCSVToTFRecordConverter:
	
	def __init__(self, task_name):
		self.task_name = task_name
		self.task_obj_dect_data_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}".format(self.task_name))
		self.task_obj_dect_cmplt_data_dir = os.path.join(settings.OBJ_DECT_DATA_DIR,
		                                                 r"tasks\{0}\all".format(self.task_name))
		self.task_obj_dect_rgb_imgs_dir = os.path.join(self.task_obj_dect_cmplt_data_dir, "rgb_images")
		self.task_obj_dect_annots_dir = os.path.join(self.task_obj_dect_cmplt_data_dir, "xml_annots")
		self.train_dataset_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\train".format(self.task_name))
		self.test_dataset_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\test".format(self.task_name))
	
	def _xml_to_csv(self, path_to_xml_annots):
		xml_list = []
		for xml_file in glob.glob(path_to_xml_annots + '/*.xml'):
			tree = ET.parse(xml_file)
			root = tree.getroot()
			for member in root.findall('object'):
				value = (root.find('filename').text,
				         int(root.find('size')[0].text),
				         int(root.find('size')[1].text),
				         member[0].text,
				         int(member[4][0].text),
				         int(member[4][1].text),
				         int(member[4][2].text),
				         int(member[4][3].text)
				         )
				xml_list.append(value)
		column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
		xml_df = pd.DataFrame(xml_list, columns=column_name)
		return xml_df
	
	def convert_xml_to_csv(self):
		for data_subset in ['train', 'test']:
			dataset_split_dir = os.path.join(self.task_obj_dect_data_dir, data_subset)
			xml_annots_dir_path = os.path.join(dataset_split_dir, "xml_annots")
			xml_df = self._xml_to_csv(xml_annots_dir_path)
			csv_annots_dir_path = os.path.join(dataset_split_dir,
			                                   r"csv_annots\{0}_{1}.csv".format(data_subset, self.task_name))
			xml_df.to_csv(csv_annots_dir_path, index=None)
			print('Successfully converted xml to csv.')
	
	def convert_csv_to_tf_record(self):
		train_csv_input_dir_path = os.path.join(self.train_dataset_dir,
		                                        r"csv_annots\train_{0}.csv".format(self.task_name))
		test_csv_input_dir_path = os.path.join(self.test_dataset_dir, r"csv_annots\test_{0}.csv".format(self.task_name))
		train_rgb_img_dir_path = os.path.join(self.train_dataset_dir, "rgb_images")
		test_rgb_img_dir_path = os.path.join(self.test_dataset_dir, "rgb_images")
		train_tf_record_output_dir_path = os.path.join(self.train_dataset_dir,
		                                               r"tf_record_annots\train_{0}.record".format(self.task_name))
		test_tf_record_output_dir_path = os.path.join(self.test_dataset_dir,
		                                              r"tf_record_annots\test_{0}.record".format(self.task_name))
		# C:\Users\Xavier\RSAI_JARVIS\data\obj_dect_data\tasks\mining\train\csv_annots\train_mining.csv
		train_args_str = r"python C:\Users\Xavier\RSAI_JARVIS\src\data_tools\obj_dect_data_tools\my_custom_tf_records_generator.py --csv_input={0} --image_dir={1} --output_path={2}".format(
			train_csv_input_dir_path,
			train_rgb_img_dir_path,
			train_tf_record_output_dir_path)
		# C:\Users\Xavier\RSAI_JARVIS\src\data_tools\obj_dect_data_tools\gen_tf_records.py
		test_args_str = r"python C:\Users\Xavier\RSAI_JARVIS\src\data_tools\obj_dect_data_tools\my_custom_tf_records_generator.py --csv_input={0} --image_dir={1} --output_path={2}".format(
			test_csv_input_dir_path,
			test_rgb_img_dir_path,
			test_tf_record_output_dir_path)
		subprocess.call(train_args_str, shell=True)
		subprocess.call(test_args_str, shell=True)


if __name__ == "__main__":
	task_name = "mining"
	cls = TasksXMLToCSVToTFRecordConverter(task_name)
	cls.convert_xml_to_csv()
	cls.convert_csv_to_tf_record()
