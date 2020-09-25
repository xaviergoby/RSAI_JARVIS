import numpy as np
import time
from PIL import ImageGrab
import random
from pyclick import HumanClicker


class ObjDectSensorSubSystem:

	def __init__(self, roi):
		self.roi = roi
		self.current_ss_img = None

	def update_current_game_client_roi_area_ss(self):
		ss_img = np.array(ImageGrab.grab(bbox=self.roi))
		self.current_ss_img = ss_img

	def update_sensor(self):
		self.update_current_game_client_roi_area_ss()

	def get_current_game_client_roi_area_ss(self):
		return self.current_ss_img

	def update_and_get_current_game_client_roi_area_ss(self):
		self.update_current_game_client_roi_area_ss()
		return self.get_current_game_client_roi_area_ss()

	def get_current_game_client_roi_area_ss_dims(self):
		current_ss_img = self.get_current_game_client_roi_area_ss()
		current_ss_img_height = current_ss_img.shape[0]
		current_ss_img_width = current_ss_img.shape[1]
		return current_ss_img_height, current_ss_img_width

	def get_frame(self):
		self.update_current_game_client_roi_area_ss()
		return self.get_current_game_client_roi_area_ss()

	def compute_bbox_frame_coords(self, bbox_norm_coords: "numpy array w/ shape (1,4)") -> "list [top, left, bottom, right]":
		"""
		NOTE:
		# [y_min, x_min, y_max, x_max] <=> [top, left, bottom, right] <=> [startY, startX, endY, endX]
		:param bbox_norm_coords: numpy array w/ shape (1,4)
		:return: list [top, left, bottom, right]
		"""
		frame_height = self.current_ss_img.shape[0]
		frame_width = self.current_ss_img.shape[1]
		norm_bbox_coords_tuple = tuple(bbox_norm_coords.tolist())
		y_norm_min, x_norm_min, y_norm_max, x_norm_max = norm_bbox_coords_tuple
		y_min, y_max = int(y_norm_min * frame_height), int(y_norm_max * frame_height)
		x_min, x_max = int(x_norm_min * frame_width), int(x_norm_max * frame_width)
		# y_min, x_min, y_max, x_max <= > [top, left, bottom, right]
		# y_min, x_min, y_max, x_max <= > [startY, startX, endY, endX]
		top, left, bottom, right = y_min, x_min, y_max, x_max
		bbox_frame_coords = [top, left, bottom, right]
		return bbox_frame_coords

	def compute_boxes_frame_coords(self, boxes_norm_coords: "numpy array w/ shape (len(boxes_norm_coords), 4)") -> "list of nested [top, left, bottom, right] list":
		"""
		:param boxes_norm_coords: "numpy array w/ shape (len(boxes_norm_coords),4)"
		:return: list of nested [top, left, bottom, right] lists
		"""
		boxes_frame_coords_list = []
		for bbox_i_norm_coords in boxes_norm_coords:
			bbox_i_frame_coords = self.compute_bbox_frame_coords(bbox_i_norm_coords)
			boxes_frame_coords_list.append(bbox_i_frame_coords)
		return boxes_frame_coords_list
	

	def compute_bbox_frame_centroid(self, bbox_frame_coords: "list [top, left, bottom, right]"):
		top, left, bottom, right = bbox_frame_coords
		fy_c = (bottom - top) // 2 + top
		fx_c = (right - left) // 2 + left
		print(f"(top, left, bottom, right): {(top, left, bottom, right)}")
		print(f"(fy_c, fx_c): {(fy_c, fx_c)}")
		bbox_centroid_in_frame = [fx_c, fy_c]
		return bbox_centroid_in_frame

	def compute_boxes_frame_centroids(self, boxes_frame_coords: "list of nested [top, left, bottom, right] lists"):
		boxes_centroids_in_frame_list = []
		for bbox_i_frame_coords in boxes_frame_coords:
			bbox_i_centroid_in_frame = self.compute_bbox_frame_centroid(bbox_i_frame_coords)
			boxes_centroids_in_frame_list.append(bbox_i_centroid_in_frame)
		return boxes_centroids_in_frame_list

	def compute_bbox_screen_centroid(self, bbox_frame_centroid: "list [fx_c, fy_c]"):
		fx_c, fy_c = bbox_frame_centroid
		pxx_c = fx_c + self.roi[0]
		pxy_c = fy_c + self.roi[1]
		bbox_centroid_on_screen = [pxx_c, pxy_c]
		return bbox_centroid_on_screen

	def compute_boxes_screen_centroids(self, boxes_true_coords):
		boxes_centroids_on_screen_list = []
		for bbox_i_true_coords in boxes_true_coords:
			fx_c_i, fy_c_i = self.compute_bbox_frame_centroid(bbox_i_true_coords)
			pxx_c_i = fx_c_i + self.roi[0]
			pxy_c_i = fy_c_i + self.roi[1]
			boxes_centroids_on_screen_list.append([pxx_c_i, pxy_c_i])
		return boxes_centroids_on_screen_list







	def compute_single_inf_obj_bbox_centre_screen_coords(self, obj_bbox_norm_coords):
		"""
		:param obj_bbox_norm_coords: np arra, [norm_y_min, norm_x_min, norm_y_max, norm_x_max]
		:return: 2-tuple (inf_obj_bbox_screen_centre_y_coord, inf_obj_bbox_screen_centre_x_coord)
		"""
		img_height = self.current_ss_img.shape[0]
		img_width = self.current_ss_img.shape[1]
		obj_bbox_norm_coords_tuple = tuple(obj_bbox_norm_coords.tolist())
		norm_y_min, norm_x_min, norm_y_max, norm_x_max = obj_bbox_norm_coords_tuple
		y_min, y_max = int(norm_y_min * img_height), int(norm_y_max * img_height)
		x_min, x_max = int(norm_x_min * img_width), int(norm_x_max * img_width)
		y_c = (y_max - y_min) // 2 + y_min + self.roi[1]
		x_c = (x_max - x_min) // 2 + x_min + self.roi[0]
		return y_c, x_c

	# @staticmethod
	def compute_all_inf_obj_bbox_centre_screen_coords(self, obj_bbox_norm_coords) -> "list of nested [x, y] lists":
		obj_bbox_norm_coords_list = []
		for obj_bbox_norm_coords_i_array in obj_bbox_norm_coords:
			obj_bbox_norm_coords_i = self.compute_single_inf_obj_bbox_centre_screen_coords(obj_bbox_norm_coords_i_array)
			obj_bbox_norm_coords_list.append([obj_bbox_norm_coords_i[0], obj_bbox_norm_coords_i[1]])
		return obj_bbox_norm_coords_list
