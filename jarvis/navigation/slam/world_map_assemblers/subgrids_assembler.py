import os
import cv2
import numpy as np
from os import listdir
from os.path import isdir, join
from jarvis.navigation.slam import cv_nav_settings
from jarvis.navigation.slam import navigability_mapper_func


class SubgridsAssembler:

	def __init__(self):
		self.grids_data_dir_path = cv_nav_settings.RSAI_CV_NAV_MAPPING_DATA_DIR
		self.grid_dir_labels = [i for i in listdir(self.grids_data_dir_path) if
		                        isdir(join(self.grids_data_dir_path, i))]
		self.subgrids_assembly_order_list = ["top_left", "top_right", "bottom_left", "bottom_right"]
		self.top_row_subgrids_assembly_order_list = ["top_left", "top_right"]
		self.bottom_row_subgrids_assembly_order_list = ["bottom_left", "bottom_right"]

	def assemble_grid_subgrids(self, grid_label):
		top_row_nav_mapped_subgrid_arrays_list = []
		bottom_row_nav_mapped_subgrid_arrays_list = []
		grid_label_dir_path = os.path.join(self.grids_data_dir_path, str(grid_label))
		for top_row_subgrid_i_name in self.top_row_subgrids_assembly_order_list:
			top_row_subgrid_i_path = os.path.join(grid_label_dir_path, "{0}.png".format(top_row_subgrid_i_name))
			top_row_subgrid_i_img_array = cv2.imread(top_row_subgrid_i_path, cv2.IMREAD_UNCHANGED)
			top_row_subgrid_i_mapped_img_array = navigability_mapper_func.img_navigability_mapper(
				top_row_subgrid_i_img_array)
			top_row_nav_mapped_subgrid_arrays_list.append(top_row_subgrid_i_mapped_img_array)
		for bottom_row_subgrid_i_name in self.bottom_row_subgrids_assembly_order_list:
			bottom_row_subgrid_i_path = os.path.join(grid_label_dir_path, "{0}.png".format(bottom_row_subgrid_i_name))
			bottom_row_subgrid_i_img_array = cv2.imread(bottom_row_subgrid_i_path, cv2.IMREAD_UNCHANGED)
			bottom_row_subgrid_i_mapped_img_array = navigability_mapper_func.img_navigability_mapper(
				bottom_row_subgrid_i_img_array)
			bottom_row_nav_mapped_subgrid_arrays_list.append(bottom_row_subgrid_i_mapped_img_array)
		top_row_mapped_array = np.hstack(top_row_nav_mapped_subgrid_arrays_list)
		bottom_row_mapped_array = np.hstack(bottom_row_nav_mapped_subgrid_arrays_list)
		mapped_grid_array = np.vstack([top_row_mapped_array, bottom_row_mapped_array])
		return mapped_grid_array


if __name__ == "__main__":
	assembler = SubgridsAssembler()
	subgrid_label = 12850
	mapped_grid_array = assembler.assemble_grid_subgrids(12850)
	print(f"mapped_grid_array.shape: {mapped_grid_array.shape}")
	wndw_name = "Assemblage of grid labelled: {0}".format(str(subgrid_label))
	cv2.imshow(wndw_name, mapped_grid_array)
	cv2_close_key = cv2.waitKey(0) & 0xFF
	if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
		cv2.waitKey(0)
		cv2.destroyAllWindows()

#
# filenames= os.listdir (".") # get all files' and folders' names in the current directory
#
# result = []
# for filename in filenames: # loop through all the files and folders
#     if os.full_path.isdir(os.full_path.join(os.full_path.abspath("."), filename)): # check whether the current object is a folder or not
#         result.append(filename)
