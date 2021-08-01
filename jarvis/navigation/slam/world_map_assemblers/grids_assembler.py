import os
import cv2
import numpy as np
from os import listdir
from os.path import isdir, join
from jarvis.navigation.slam import cv_nav_settings
from jarvis.navigation.slam import navigability_mapper_func


class GridsAssembler:

	def __init__(self):
		self.map_data_dir_path = cv_nav_settings.RSAI_CV_NAV_MAPPING_DATA_DIR
		self.map_grids_rgb_imgs_dir_path = os.path.join(self.map_data_dir_path, r"grids\rgb_imgs")
		self.grid_file_names = os.listdir(self.map_grids_rgb_imgs_dir_path)
		self.grid_labels = [grid_file_name.split(".")[0] for grid_file_name in self.grid_file_names]
		self._world_grid_size()
		self._world_grids_assembly_file_name()

	def _world_grid_size(self):
		labels_ints_list = [int(label_i_str) for label_i_str in self.grid_labels]
		labels_array = np.array(labels_ints_list)
		labels_diff_array = np.diff(labels_array)
		num_vertical_grids = 1  # AKA number of rows of grids
		for labels_diff_i in labels_diff_array:
			if labels_diff_i == 1:
				num_vertical_grids = num_vertical_grids + 1
			else:
				break
		num_horizontal_grids = int(len(self.grid_labels) / num_vertical_grids)  # AKA # of cols of grids
		self.world_grid_size = num_vertical_grids, num_horizontal_grids

	def _world_grids_assembly_file_name(self):
		bottom_left_grid_label = self.grid_labels[-1]
		num_grid_rows = self.world_grid_size[0]
		num_grid_cols = self.world_grid_size[1]
		mapped_file_name = "bottom_left_{0}_size_{1}_by_{2}_array".format(bottom_left_grid_label, num_grid_rows, num_grid_cols)
		rgb_file_name = "bottom_left_{0}_size_{1}_by_{2}_rgb.png".format(bottom_left_grid_label, num_grid_rows, num_grid_cols)
		self.assembled_mapped_world_file_name = mapped_file_name
		self.assembled_rgb_world_file_name = rgb_file_name


	def assemble_grids(self):
		rgb_grid_col_arrays_list = []
		mapped_grid_col_arrays_list = []
		num_grid_rows = self.world_grid_size[0]
		num_grid_cols = self.world_grid_size[1]
		for grids_col_i in range(num_grid_cols):
			mapped_col_i_grid_arrays_list = []
			rgb_col_i_grid_arrays_list = []
			col_i_grid_file_names = self.grid_file_names[0 + grids_col_i * num_grid_rows:num_grid_rows + grids_col_i * num_grid_rows]
			col_i_grid_file_names.reverse()
			for col_i_grid_file_name_j in col_i_grid_file_names:
				col_i_row_j_grid_file_path = os.path.join(self.map_grids_rgb_imgs_dir_path, col_i_grid_file_name_j)
				col_i_row_j_grid_rgb_img_array = cv2.imread(col_i_row_j_grid_file_path, cv2.IMREAD_UNCHANGED)
				rgb_col_i_grid_arrays_list.append(col_i_row_j_grid_rgb_img_array)
				col_i_row_j_grid_mapping = navigability_mapper_func.img_navigability_mapper(col_i_row_j_grid_rgb_img_array, 4)
				mapped_col_i_grid_arrays_list.append(col_i_row_j_grid_mapping)
			col_i_grids_vstacked = np.vstack(mapped_col_i_grid_arrays_list)
			rgb_col_i_grid_arrays_list_vstacked = np.vstack(rgb_col_i_grid_arrays_list)
			mapped_grid_col_arrays_list.append(col_i_grids_vstacked)
			rgb_grid_col_arrays_list.append(rgb_col_i_grid_arrays_list_vstacked)
		assembled_mapped_grids = np.hstack(mapped_grid_col_arrays_list)
		assembled_rgb_imgs = np.hstack(rgb_grid_col_arrays_list)
		np.save(os.path.join(self.map_data_dir_path, self.assembled_mapped_world_file_name), assembled_mapped_grids)
		cv2.imwrite(self.assembled_rgb_world_file_name, assembled_rgb_imgs)
		return assembled_mapped_grids


if __name__ == "__main__":
	grids_assembler = GridsAssembler()
	print(grids_assembler.grid_file_names)
	print(grids_assembler.grid_labels)
	print(grids_assembler.world_grid_size)
	res = grids_assembler.assemble_grids()
	wndw_name = "Assembled World"
	cv2.namedWindow(wndw_name, cv2.WINDOW_NORMAL)
	cv2.imshow(wndw_name, res)
	cv2_close_key = cv2.waitKey(0) & 0xFF
	if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
		cv2.waitKey(0)
		cv2.destroyAllWindows()

