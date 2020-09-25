import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
	xml_list = []
	for xml_file in glob.glob(path + '/*.xml'):
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

def main(task_name):
	path_to_task = r"C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\images\tasks\{0}".format(task_name)
	for directory in ['train', 'test']:
		dataset_dir = os.path.join(path_to_task, directory)
		xml_df = xml_to_csv(dataset_dir)
		annots_dir_path = r"C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\annots\{0}_{1}_labels.csv".format(task_name, directory)
		xml_df.to_csv(annots_dir_path, index=None)
		print('Successfully converted xml to csv.')

if __name__ == "__main__":
	task_name = "slaying_cows"
	main(task_name)