import cv2
import numpy as np


class ImageOverlayTool:

	# roi = (8, 31, 791, 591)
	# (560, 783, 3)

	def __init__(self, roi):
		self.txt_font_colour = (255, 255, 255)
		self.txt_box_bg_colour = (0, 0, 0)
		self.txt_font = cv2.FONT_HERSHEY_SIMPLEX
		self.txt_scale = 0.3
		self.txt_thickness = 1
		self.txt_vertical_offset = 3
		self.txt_lower_padding = 3

	# @staticmethod
	def create_agent_state_info_txts(self, current_world_loc, prev_world_loc,
	                                 local_ds_vec=None, target_dest_world_loc=None):
		current_world_loc_info_txt = "Current World Loc.: {0}".format(current_world_loc)
		prev_world_loc_info_txt = "Previous World Loc.: {0}".format(prev_world_loc)
		local_ds_vec_info_txt = "Local Displacement Vector.: {0}".format(local_ds_vec)
		target_dest_world_loc_info_txt = "Target Destination World Loc.: {0}".format(target_dest_world_loc)
		return current_world_loc_info_txt, prev_world_loc_info_txt, local_ds_vec_info_txt, target_dest_world_loc_info_txt

	def get_agent_state_info_txt_sizes(self, current_world_loc_info_txt, prev_world_loc_info_txt,
	                                   local_ds_vec_info_txt, target_dest_world_loc_info_txt):
		current_world_loc_info_txt_size = cv2.getTextSize(current_world_loc_info_txt, self.txt_font,
		                                                  self.txt_scale, self.txt_thickness)
		prev_world_loc_info_txt_size = cv2.getTextSize(prev_world_loc_info_txt, self.txt_font,
		                                               self.txt_scale, self.txt_thickness)
		local_ds_vec_info_txt_size = cv2.getTextSize(local_ds_vec_info_txt, self.txt_font,
		                                             self.txt_scale, self.txt_thickness)
		target_dest_world_loc_info_txt_size = cv2.getTextSize(target_dest_world_loc_info_txt, self.txt_font,
		                                                      self.txt_scale, self.txt_thickness)
		return current_world_loc_info_txt_size, prev_world_loc_info_txt_size, \
		       local_ds_vec_info_txt_size, target_dest_world_loc_info_txt_size

	def get_agent_state_info_txt_box_height(self, agent_state_info_txt_sizes):
		# def get_agent_state_info_txt_box_height(self, current_world_loc_info_txt_size, prev_world_loc_info_txt_size,
		#                                  local_ds_vec_info_txt_size, target_dest_world_loc_info_txt_size):
		# 	state_info_txt_box_height = 0
		state_info_txt_box_height = self.txt_vertical_offset
		# state_info_txt_sizes = agent_state_info_txt_sizes_list
		# state_info_txt_sizes = [current_world_loc_info_txt_size, prev_world_loc_info_txt_size,
		#                         local_ds_vec_info_txt_size, target_dest_world_loc_info_txt_size]
		for state_info_txt_size_i in agent_state_info_txt_sizes:
			# for state_info_txt_size_i in state_info_txt_sizes:
			state_info_txt_size_i_height = state_info_txt_size_i[1]
			state_info_txt_box_height = state_info_txt_box_height + state_info_txt_size_i_height + self.txt_vertical_offset
			print(f"state_info_txt_size_i_height: {state_info_txt_size_i_height}")
			print(f"state_info_txt_box_height: {state_info_txt_box_height}")
		return state_info_txt_box_height

	def create_agent_state_info_txt_box(self, sensor_percept_array, current_world_loc, prev_world_loc,
	                                    local_ds_vec=None, target_dest_world_loc=None):
		agent_state_info_txts = self.create_agent_state_info_txts(current_world_loc, prev_world_loc,
		                                                          local_ds_vec, target_dest_world_loc)
		current_world_loc_info_txt = agent_state_info_txts[0]
		prev_world_loc_info_txt = agent_state_info_txts[1]
		local_ds_vec_info_txt = agent_state_info_txts[2]
		target_dest_world_loc_info_txt = agent_state_info_txts[3]
		agent_state_info_txt_sizes = self.get_agent_state_info_txt_sizes(current_world_loc_info_txt,
		                                                                 prev_world_loc_info_txt,
		                                                                 local_ds_vec_info_txt,
		                                                                 target_dest_world_loc_info_txt)

		agent_state_info_txt_box_height = self.get_agent_state_info_txt_box_height(agent_state_info_txt_sizes)
		txt_box_width = sensor_percept_array.shape[1]
		txt_box_height = agent_state_info_txt_box_height
		print(f"txt_box_height: {txt_box_height}")
		print(f"txt_box_width: {txt_box_width}")
		txt_box_place_holder = np.zeros([txt_box_height, txt_box_width, 3], dtype=np.uint8)
		txt_box_place_holder.fill(0)  # or img[:] = 255
		return txt_box_place_holder

	def overlay_agent_state_info(self, sensor_percept_array, current_world_loc, prev_world_loc,
	                             local_ds_vec=None, target_dest_world_loc=None):
		sensor_percept_array_copy = sensor_percept_array.copy()
		agent_state_info_txts = self.create_agent_state_info_txts(current_world_loc, prev_world_loc,
		                                                          local_ds_vec, target_dest_world_loc)
		current_world_loc_info_txt = agent_state_info_txts[0]
		prev_world_loc_info_txt = agent_state_info_txts[1]
		local_ds_vec_info_txt = agent_state_info_txts[2]
		target_dest_world_loc_info_txt = agent_state_info_txts[3]
		agent_state_info_txt_sizes = self.get_agent_state_info_txt_sizes(current_world_loc_info_txt,
		                                                                 prev_world_loc_info_txt,
		                                                                 local_ds_vec_info_txt,
		                                                                 target_dest_world_loc_info_txt)
		agent_state_info_txt_box = self.create_agent_state_info_txt_box(sensor_percept_array, current_world_loc,
		                                                                prev_world_loc, local_ds_vec=None,
		                                                                target_dest_world_loc=None)
		sensor_percept_array_height = sensor_percept_array.shape[1]
		sensor_percept_array_width = sensor_percept_array.shape[0]
		agent_state_info_txt_box_width = agent_state_info_txt_box.shape[1]
		agent_state_info_txt_box_height = agent_state_info_txt_box.shape[0] + sensor_percept_array_height
		txt_box_and_screen_shot_img_vstacked = np.vstack((sensor_percept_array_copy, agent_state_info_txt_box))
		# y = agent_state_info_txt_box_height - self.txt_vertical_offset
		x = 1
		for state_info_txt_i_idx in range(len(agent_state_info_txts)):
			state_info_txt_i = agent_state_info_txts[state_info_txt_i_idx]
			y = agent_state_info_txt_box_height - agent_state_info_txt_sizes[state_info_txt_i_idx][1]*state_info_txt_i_idx - self.txt_vertical_offset
			print(f"agent_state_info_txt_box_height: {agent_state_info_txt_box_height}")
			# y = agent_state_info_txt_box_height - state_info_txt_i_idx * self.txt_vertical_offset - self.txt_vertical_offset
			txt_box_and_screen_shot_img_vstacked = cv2.putText(txt_box_and_screen_shot_img_vstacked,
			                                                   state_info_txt_i, (x, y),
			                                                   self.txt_font, self.txt_scale, self.txt_font_colour,
			                                                   self.txt_thickness, cv2.LINE_AA)
		return txt_box_and_screen_shot_img_vstacked
		# sensor_percept_array.shape: (60, 60, 3)
		# pass

	def overlay_agent_state_info_txt(self, sensor_percept_array):
		# roi = (8, 31, 791, 591)
		# rgb_img_copy.shape: (560, 783, 3)
		img_px_width = sensor_percept_array[1]
		img_px_height = sensor_percept_array[0]
		pass


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
		img = cv2.line(img, (x_int_coords_list[pnt_idx], y_min), (x_int_coords_list[pnt_idx], y_max), (255, 255, 255),
		               line_thickness)
		# draw horizontal lines
		img = cv2.line(img, (x_min, y_int_coords_list[pnt_idx]), (x_max, y_int_coords_list[pnt_idx]),
		               rgb_colour_code_tuple, line_thickness)
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
			img = cv2.circle(img, (pnt_x_coord, pnt_y_coord), grid_pnts_radius, rgb_colour_code_tuple,
			                 grid_pnts_thickness)
	return img
