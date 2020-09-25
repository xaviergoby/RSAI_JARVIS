import cv2
from research_and_dev.rsai_cv_navigability_mapping.world_map_assemblers.subgrids_assembler import SubgridsAssembler


class NavMapCoordsToolKit:
	pass







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
