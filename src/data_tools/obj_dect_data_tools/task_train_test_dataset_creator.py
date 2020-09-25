import os
import settings
import random
import numpy as np
import shutil


class TrainTestDatasetSplitter:
	
	
	
	def __init__(self, task_name):
		self.task_name = task_name
		self.task_data_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\all".format(self.task_name))
		self.rgb_images_dir = os.path.join(self.task_data_dir, "rgb_images")
		self.annots_dir = os.path.join(self.task_data_dir, "annots")
		self.train_dataset_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\train".format(self.task_name))
		self.test_dataset_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\test".format(self.task_name))
		self.rgb_images_filenames = os.listdir(self.rgb_images_dir)
		self.xml_annots_filenames = os.listdir(self.annots_dir)
		self.num_tot_samples = len(self.rgb_images_filenames)
		self.dataset_samples_idxs = [sample_i_idx for sample_i_idx in range(self.num_tot_samples)]
		
	def gen_train_test_rand_samples_idxs(self, ratio):
		num_train_samples = int(self.num_tot_samples * ratio)
		self.train_samples_idxs = random.sample(self.dataset_samples_idxs, num_train_samples)
		self.test_samples_idxs = np.setdiff1d(self.dataset_samples_idxs, self.train_samples_idxs).tolist()
		return self.train_samples_idxs, self.test_samples_idxs
	
	def gen_train_rand_samples_filenames(self):
		self.train_rgb_images_filenames = []
		self.train_xml_annots_filenames = []
		for train_sample_idx_i in self.train_samples_idxs:
			self.train_rgb_images_filenames.append(self.rgb_images_filenames[train_sample_idx_i])
			self.train_xml_annots_filenames.append(self.xml_annots_filenames[train_sample_idx_i])
		return self.train_rgb_images_filenames, self.train_xml_annots_filenames
	
	def gen_test_rand_samples_filenames(self):
		self.test_rgb_images_filenames = []
		self.test_xml_annots_filenames = []
		for test_sample_idx_i in self.test_samples_idxs:
			self.test_rgb_images_filenames.append(self.rgb_images_filenames[test_sample_idx_i])
			self.test_xml_annots_filenames.append(self.xml_annots_filenames[test_sample_idx_i])
		return self.test_rgb_images_filenames, self.test_xml_annots_filenames
	
	def create_train_test_rgb_imgs_annots_dataset_split(self, ratio, random_sampling=True):
		if random_sampling is True:
			self.gen_train_test_rand_samples_idxs(ratio)
			self.gen_train_rand_samples_filenames()
			self.gen_test_rand_samples_filenames()
		else:
			num_train_images = int(len(self.rgb_images_filenames) * ratio)
			self.train_rgb_images_filenames = self.rgb_images_filenames[:num_train_images]
			self.test_rgb_image_filenames = self.rgb_images_filenames[num_train_images:]
			self.train_xml_annots_filenames = self.xml_annots_filenames[:num_train_images]
			self.test_xml_annots_filenames = self.xml_annots_filenames[num_train_images:]
		
		for train_sample_i_filename_idx in range(len(self.train_samples_idxs)):
			train_rgb_image_filename = self.train_rgb_images_filenames[train_sample_i_filename_idx]
			train_xml_annot_filename = self.train_xml_annots_filenames[train_sample_i_filename_idx]
			train_rgb_image_file_src = os.path.join(self.rgb_images_dir, train_rgb_image_filename)
			train_xml_annot_file_src = os.path.join(self.annots_dir, train_xml_annot_filename)
			train_rgb_image_file_dst = os.path.join(self.train_dataset_dir, r"rgb_images\{0}".format(train_rgb_image_filename))
			train_xml_annot_file_dst = os.path.join(self.train_dataset_dir, r"xml_annots\{0}".format(train_xml_annot_filename))
			shutil.copy(train_rgb_image_file_src, train_rgb_image_file_dst)
			shutil.copy(train_xml_annot_file_src, train_xml_annot_file_dst)
			
		for test_sample_i_filename_idx in range(len(self.test_samples_idxs)):
			test_rgb_image_filename = self.test_rgb_images_filenames[test_sample_i_filename_idx]
			test_xml_annot_filename = self.test_xml_annots_filenames[test_sample_i_filename_idx]
			test_rgb_image_file_src = os.path.join(self.rgb_images_dir, test_rgb_image_filename)
			test_xml_annot_file_src = os.path.join(self.annots_dir, test_xml_annot_filename)
			test_rgb_image_file_dst = os.path.join(self.test_dataset_dir, r"rgb_images\{0}".format(test_rgb_image_filename))
			test_xml_annot_file_dst = os.path.join(self.test_dataset_dir, r"xml_annots\{0}".format(test_xml_annot_filename))
			shutil.copy(test_rgb_image_file_src, test_rgb_image_file_dst)
			shutil.copy(test_xml_annot_file_src, test_xml_annot_file_dst)
	
	
		
if __name__ == "__main__":
	cls = TrainTestDatasetSplitter("mining")
	cls.create_train_test_rgb_imgs_annots_dataset_split(0.8, random_sampling=True)
	train_rgb_images_filenames, train_xml_annots_filenames = cls.train_rgb_images_filenames, cls.train_xml_annots_filenames
	print(len(train_rgb_images_filenames))
	print(len(train_xml_annots_filenames))
	