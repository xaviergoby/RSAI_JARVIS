import cv2
import itertools
import numpy as np


def draw_sq_grid_lines_on_img_v1(img, x_int_coords_list, y_int_coords_list,
                                 rgb_colour_code_tuple=(0, 0, 0), line_thickness=1):
	img = img
	x_min, x_max = min(x_int_coords_list), max(x_int_coords_list)
	y_min, y_max = min(y_int_coords_list), max(y_int_coords_list)
	num_of_pnts = len(x_int_coords_list)
	horizontal_line_left_edge_pnts = []
	horizontal_line_right_edge_pnts = []
	vertical_line_top_edge_pnts = []
	vertical_line_bottom_edge_pnts = []
	for pnt_idx in range(num_of_pnts):
		vertical_line_top_edge_pnts.append((x_int_coords_list[pnt_idx], y_min))
		horizontal_line_right_edge_pnts.append((x_int_coords_list[pnt_idx], y_max))
		vertical_line_bottom_edge_pnts.append((x_int_coords_list[pnt_idx], y_max))
		horizontal_line_left_edge_pnts.append((x_min, y_int_coords_list[pnt_idx]))
		horizontal_line_right_edge_pnts.append((x_max, y_int_coords_list[pnt_idx]))
		# draw vertical lines
		# img = cv2.line(img, (x_int_coords_list[pnt_idx], y_min), (x_int_coords_list[pnt_idx], y_max), rgb_colour_code_tuple, line_thickness)
		img = cv2.line(img, (x_int_coords_list[pnt_idx], y_min), (x_int_coords_list[pnt_idx], y_max), (255, 255, 255), line_thickness)
		# draw horizontal lines
		img = cv2.line(img, (x_min, y_int_coords_list[pnt_idx]), (x_max, y_int_coords_list[pnt_idx]), rgb_colour_code_tuple, line_thickness)
	return img


def draw_sq_grid_points(img, x_int_coords_list, y_int_coords_list,
                                 rgb_colour_code_tuple=(0, 0, 0), grid_pnts_thickness=-2, grid_pnts_radius=5):
	img = img
	num_of_pnts = len(x_int_coords_list)
	grid_pnts = []
	for pnt_x_coord_idx in range(num_of_pnts):
		for pnt_y_coord_idx in range(num_of_pnts):
			# print(f"type(pnt_x_coord): {type(x_int_coords_list[pnt_x_coord_idx])}")
			# print(f"pnt_x_coord: {x_int_coords_list[pnt_x_coord_idx]}")
			# print(f"type(pnt_y_coord): {type(y_int_coords_list[pnt_y_coord_idx])}")
			# print(f"pnt_y_coord: {y_int_coords_list[pnt_y_coord_idx]}")
			pnt_x_coord = x_int_coords_list[pnt_x_coord_idx] - 8
			pnt_y_coord = y_int_coords_list[pnt_y_coord_idx] - 31
			grid_pnts.append([pnt_x_coord, pnt_y_coord])
			img = cv2.circle(img, (pnt_x_coord, pnt_y_coord), grid_pnts_radius, rgb_colour_code_tuple, grid_pnts_thickness)
	return img


# def draw_sq_grid_points(img, x_int_coords_list, y_int_coords_list,
#                                  rgb_colour_code_tuple=(0, 0, 0), line_thickness=1):
# 	img = img
# 	x_min, x_max = min(x_int_coords_list), max(x_int_coords_list)
# 	y_min, y_max = min(y_int_coords_list), max(y_int_coords_list)
# 	num_of_pnts = len(x_int_coords_list)
# 	horizontal_line_left_edge_pnts = []
# 	horizontal_line_right_edge_pnts = []
# 	vertical_line_top_edge_pnts = []
# 	vertical_line_bottom_edge_pnts = []
# 	for pnt_idx in range(num_of_pnts):
# 		vertical_line_top_edge_pnts.append((x_int_coords_list[pnt_idx], y_min))
# 		horizontal_line_right_edge_pnts.append((x_int_coords_list[pnt_idx], y_max))
# 		vertical_line_bottom_edge_pnts.append((x_int_coords_list[pnt_idx], y_max))
# 		horizontal_line_left_edge_pnts.append((x_min, y_int_coords_list[pnt_idx]))
# 		horizontal_line_right_edge_pnts.append((x_max, y_int_coords_list[pnt_idx]))
# 		# draw vertical lines
# 		# img = cv2.line(img, (x_int_coords_list[pnt_idx], y_min), (x_int_coords_list[pnt_idx], y_max), rgb_colour_code_tuple, line_thickness)
# 		img = cv2.line(img, (x_int_coords_list[pnt_idx], y_min), (x_int_coords_list[pnt_idx], y_max), (255, 255, 255), line_thickness)
# 		# draw horizontal lines
# 		img = cv2.line(img, (x_min, y_int_coords_list[pnt_idx]), (x_max, y_int_coords_list[pnt_idx]), rgb_colour_code_tuple, line_thickness)
# 	return img

