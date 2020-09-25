from obj_detc_sys_components.obj_dect_actuator_sub_sys import ObjDectActuatorSubSystem
from obj_detc_sys_components.obj_dect_inf_gen_sub_sys import ObjDectInferenceGenSubSystem
from obj_detc_sys_components.obj_dect_sensor_sub_sys import ObjDectSensorSubSystem
from obj_detc_sys_components.obj_dect_mining_sub_sys import ObjDectMiningSubSystem
from obj_detc_sys_components.obj_dect_trackers.obj_centroid_tracker import CentroidTracker
from src.game.inv_handler import InventoryHandler
from src.utils.time_tools import StopWatchTimer
import cv2
import random
import numpy as np
import time


class ObjDectMainSystem(ObjDectInferenceGenSubSystem, ObjDectActuatorSubSystem, ObjDectMiningSubSystem):
	"""
	# copper_mine: 1
	# tin_mine: 2
	# depleted_mine: 3
	"""
	
	# //TODO: Refactor ObjDectMainSystem so that it only inherits from ObjDectInferenceGenSubSystem and CentroidTracker
	# //TODO: Make ObjDectMainSystem a facade so that it becomes an API/simple interface to the subsystems classes ObjDectSensorSubSystem, ObjDectActuatorSubSystem
	
	def __init__(self, task_name, roi, confidence_threshold=0.1, max_detections=None):
		self.task_name = task_name
		self.roi = roi
		self.confidence_threshold = confidence_threshold
		self.max_detections = max_detections
		self.detections = None
		self.tracker = CentroidTracker()
		self.mining = False
		self.currently_mining_mine_unique_id = None
		self.mines_mined = 0
		self.inv = InventoryHandler()
		self.stop_watch = StopWatchTimer()
		self.tot_mined_mined = 0
		self.sensor = ObjDectSensorSubSystem(self.roi)
		self.current_frame_detections_dict = None
		self.current_detections = None
		self.current_confident_detections = None
		
		
		ObjDectInferenceGenSubSystem.__init__(self, self.task_name, self.max_detections, self.confidence_threshold)
		ObjDectActuatorSubSystem.__init__(self, self.roi)
		# ObjDectSensorSubSystem.__init__(self, self.roi)
		ObjDectMiningSubSystem.__init__(self)
		# CentroidTracker.__init__(self)

	def init_obj_dect_system(self):
		self.prepare_infer_sess()
		
	# def init_inf_gen_sub_sys(self):
	# 	self.prepare_infer_sess()
		
	def confident_detections(self, detections):
		confident_detections_idxs = np.where(detections["obj_scores"] >= self.confidence_threshold)
		confident_boxes_norm_coords = detections["norm_boxes"][confident_detections_idxs]
		confident_boxes_scores = detections["obj_scores"][confident_detections_idxs]
		confident_boxes_classes = detections["classes"][confident_detections_idxs]
		return confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes

	def run_obj_dect(self):
		iter = 0
		while True:
			print("\n")
			# print("\nCurrent Iteration Number: {0}".format(iter))
			# frame = self.get_frame()
			frame = self.sensor.get_frame()
			frame_ic = int(frame.shape[0]/2)
			frame_jc = int(frame.shape[1]/2)
			print(f"Frame shape (height, width, channels): {frame.shape}")
			print(f"Local (frame) centre coordinates (pxy, pxx)↔(row i, col j): {(frame_ic, frame_jc)}")
			# print(f"Frame shape: {frame.shape}")
			# self.detections = self.get_frame_inf_dict(frame, max_detections=self.max_detections)
			self.current_frame_detections_dict = self.get_frame_inf_dict(frame)
			self.current_detections = self.get_detections(frame)
			self.current_confident_detections = self.confident_detections(self.current_detections)
			
			acceptable_detections_idxs = np.where(self.current_frame_detections_dict["obj_scores"] >= 0.1)
			acceptable_boxes_norm_coords = self.current_frame_detections_dict["norm_boxes"][acceptable_detections_idxs]
			acceptable_boxes_scores = self.current_frame_detections_dict["obj_scores"][acceptable_detections_idxs]
			acceptable_boxes_classes = self.current_frame_detections_dict["classes"][acceptable_detections_idxs]
			# boxes_norm_coords = acceptable_norm_boxes
			# boxes_norm_coords = self.current_frame_detections_dict["norm_boxes"]
			acceptable_boxes_frame_coords = self.sensor.compute_boxes_frame_coords(acceptable_boxes_norm_coords)
			acceptable_boxes_frame_centroids = self.sensor.compute_boxes_frame_centroids(acceptable_boxes_frame_coords)
			# self.tracker.update_tracking(boxes_frame_centroids)
			self.tracker.update_tracking(acceptable_boxes_frame_centroids, acceptable_boxes_scores, acceptable_boxes_classes)

			# acceptable_detections_idxs = np.where(self.current_frame_detections_dict["obj_scores"] >= 0.1)
			# acceptable_norm_boxes = self.current_frame_detections_dict["norm_boxes"][acceptable_detections_idxs]
			# acceptable_scores = self.current_frame_detections_dict["obj_scores"][acceptable_detections_idxs]
			# acceptable_classes = self.current_frame_detections_dict["classes"][acceptable_detections_idxs]
			# num_detections = self.current_frame_detections_dict["num_detections"]
			inf_res_img = self.current_frame_detections_dict["inf_res_img"]
			# detections_norm_boxes = acceptable_norm_boxes
			# detections_centroids_screen_coords = self.compute_all_inf_obj_bbox_centre_screen_coords(detections_norm_boxes)
			# self.tracker.update_tracking(detections_centroids_screen_coords)

			current_tracking = self.tracker.get_current_tracking_objects()
			current_tracking_objs_centroids = self.tracker.get_current_tracking_objs_centroids()

			# acceptable_detections = self.current_frame_detections_dict["obj_scores"] >= 0.1
			# num_acceptable_detections = len(acceptable_detections[acceptable_detections == True])
			# for acceptable_detection_i_idx in range(num_acceptable_detections):
			for (tracking_id_i, centroid_i) in current_tracking_objs_centroids.items():
				obj_screen_centroid_pos = (centroid_i[0], centroid_i[1])
				text = "Mine ID:{}".format(tracking_id_i)
				print(f"Obj ID {tracking_id_i} screen centroid pos coords: {obj_screen_centroid_pos}")
				cv2.putText(inf_res_img, text, (centroid_i[0] - 10, centroid_i[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				cv2.circle(inf_res_img, (centroid_i[0], centroid_i[1]), 4, (0, 255, 0), -1)

			cv2_window_name = "{0} Object Detection | Image Dimensions: {1}".format(self.task_name.upper(),
			                                                                        inf_res_img.shape)

			cv2.moveWindow(cv2_window_name, 1080, 31)
			cv2.imshow(cv2_window_name, cv2.cvtColor(inf_res_img, cv2.COLOR_BGR2RGB))
			# print(f"self.tracker.obj_centroids: {self.tracker.obj_centroids}")
			# print(f"self.tracker.obj_scores: {self.tracker.obj_scores}")
			# print(f"self.tracker.obj_cls_labels: {self.tracker.obj_cls_labels}")
			# print(f"len(list(self.tracker.obj_centroids.keys())): {len(list(self.tracker.obj_centroids.keys()))}")
			# print(f"len(list(self.tracker.obj_scores.keys())): {len(list(self.tracker.obj_scores.keys()))}")
			# print(f"len(list(self.tracker.obj_cls_labels.keys())): {len(list(self.tracker.obj_cls_labels.keys()))}")
			# print("~"*20)
			# print("Objects Currently Being Tracked: {0}".format(current_tracking))
			
			if self.mining is False:
				mine_2_mine_unique_id = list(current_tracking.keys())[0]
				current_tracking_bbox_mines_unique_ids = list(current_tracking.keys())
				for current_tracking_bbox_mines_unique_id_i in list(current_tracking.keys()):
					if current_tracking[current_tracking_bbox_mines_unique_id_i][2] == 1:
						mine_2_mine_unique_id = current_tracking_bbox_mines_unique_id_i
						break
					else:
						continue
				self.currently_mining_mine_unique_id = mine_2_mine_unique_id
				currently_mining_mine_bbox_frame_centroid_coords = current_tracking[mine_2_mine_unique_id][0]
				# print(f"currently_mining_mine_bbox_frame_centroid_coords: {currently_mining_mine_bbox_frame_centroid_coords}")
				currently_mining_mine_bbox_screen_centroid_coords = self.sensor.compute_bbox_screen_centroid(currently_mining_mine_bbox_frame_centroid_coords)
				lmc_x_c, lmc_y_c = currently_mining_mine_bbox_screen_centroid_coords
				self.perform_lmc(lmc_y_c, lmc_x_c)
				print("Mining Copper Mine {0}".format(self.currently_mining_mine_unique_id))
				self.mines_mined = self.mines_mined + 1
				self.tot_mined_mined = self.tot_mined_mined + 1
				self.stop_watch.start()
				self.mining = True
			elif self.mining is True:
				if self.currently_mining_mine_unique_id in list(current_tracking.keys()):
					if current_tracking[self.currently_mining_mine_unique_id][2] == 3:
						print("Copper Mine {0} has been DEPLETED".format(self.currently_mining_mine_unique_id))
						self.mining = False
						self.currently_mining_mine_unique_id = None
						self.stop_watch.reset()
				elif self.currently_mining_mine_unique_id not in list(current_tracking.keys()):
					self.mining = False
					self.currently_mining_mine_unique_id = None
					self.stop_watch.reset()
			rand_num_items_2_drop = random.randint(8, 16)
			if self.mines_mined == rand_num_items_2_drop:
				print("Randomly dropping {0} copper ores".format(rand_num_items_2_drop))
				self.inv.drop_all_inv_item_by_name("copper_ore")
				self.mines_mined = 0
			if self.stop_watch.start_time is not None:
				if self.stop_watch.get_current_time_seconds_diff() >= 10:
					if self.mining is True:
						self.tot_mined_mined = self.tot_mined_mined - 1
						self.mines_mined = self.mines_mined - 1
					self.mining = False
					self.currently_mining_mine_unique_id = None
					self.stop_watch.reset()
				
				
					
			
					
					
					
				
				# compute_bbox_screen_centroid

			# time.sleep(0.1)
			iter = iter + 1

			if cv2.waitKey(1) & 0xFF == ord('q'):
				
				# cv2.imwrite("mining_with_obj_dect_sys.PNG", cv2.cvtColor(inf_res_img, cv2.COLOR_BGR2RGB))
				# print(f"inf_res_img.shape: {inf_res_img}")
				# print(f"acceptable_boxes_norm_coords: {acceptable_boxes_norm_coords}")
				# print(f"acceptable_boxes_scores: {acceptable_boxes_scores}")
				# print(f"acceptable_boxes_classes: {acceptable_boxes_classes}")
				# print(f"acceptable_boxes_frame_coords: {acceptable_boxes_frame_coords}")
				# print(f"acceptable_boxes_frame_centroids: {acceptable_boxes_frame_centroids}")
				
				cv2.destroyAllWindows()
				break
			# time.sleep(0.6)
		
			# print("\nCurrent Iteration Number: {0}".format(iter))
			# img_2_infer = self.update_and_get_current_game_client_roi_area_ss()
			# img_2_infer = self.get_frame()
			# img_height = img_2_infer.shape[0]
			# img_width = img_2_infer.shape[1]
			# current_inf_res_dict = self.current_inf_res_dict(img_2_infer, max_detections=self.max_detections)
			# self.current_inf_res_dict = self.gen_inf_res_dict(img_2_infer, max_detections=self.max_detections)
			# obj_inf_res = self.visual_img_inference(img_2_infer)
			# norm_boxes, obj_scores, classes, num_detections, inf_res_img = self.current_inf_res_dict.values()
			# print(f"norm_boxes: {norm_boxes}")
			# print(f"obj_scores: {obj_scores}")
			# print(f"classes: {classes}")
			# print(f"num_detections: {num_detections}")
			# print(f"inf_res_img: {inf_res_img}")

			# self.current_inf_res_dict = current_inf_res_dict





			# inf_obj_bbox_norm_coords = current_inf_res_dict[0]
			# inf_obj_scores = current_inf_res_dict[1]
			# inf_obj_classes = current_inf_res_dict[2]
			# inf_obj_num_detections = current_inf_res_dict[3]
			# inf_res_img = current_inf_res_dict[4]
			# inf_obj_bbox_superimposed_img = img_inf_res[-1]
			
			# cv2_window_name = "{0} Object Detection | Image Dimensions: {1}".format(self.task_name.upper(), inf_res_img.shape)
			# cv2.imshow(cv2_window_name, cv2.cvtColor(inf_res_img, cv2.COLOR_BGR2RGB))

			# boxes_screen_pos_coords = self.compute_all_inf_obj_bbox_centre_screen_coords(norm_boxes)

			# time.sleep(0.1)

			# iter = iter + 1
			
			# single_rand_top_3_bbox_norm_coords = img_inf_res[0][random.randint(1, 3)]
			# top_3_inf_obj_bbox = boxes[:num_inf_objs_to_use]
			# top_3_inf_obj_bbox_norm_coords = boxes[:num_inf_objs_to_use]
			# obj_bbox_norm_coords = single_rand_top_3_bbox_norm_coords
			
			# single_highest_acc_inf_obj_bbox = boxes[0]
			# single_highest_acc_inf_obj_bbox_norm_coords = norm_boxes[0]
			
			# all_inf_obj_bbox_norm_coords = inf_obj_bbox_norm_coords
			# all_inf_obj_classes = inf_obj_classes
			
			# single_obj_bbox_centre_coords_wrt_screen = self.compute_single_inf_obj_bbox_centre_screen_coords(single_highest_acc_inf_obj_bbox_norm_coords)

			# all_obj_bbox_centre_coords_wrt_screen = self.compute_all_inf_obj_bbox_centre_screen_coords(all_inf_obj_bbox_norm_coords)
			# print(f"len(all_obj_bbox_centre_coords_wrt_screen): {len(all_obj_bbox_centre_coords_wrt_screen)}")
			# self.all_obj_bbox_centre_coords_wrt_screen = all_obj_bbox_centre_coords_wrt_screen
			# print("Highest acc inferred object screen centre coords: {0}".format(self.all_obj_bbox_centre_coords_wrt_screen[0]))
			# self.all_inf_obj_classes = all_inf_obj_classes
			# print(f"self.all_inf_obj_classes[:10]: {self.all_inf_obj_classes[:10]}")
			# self.eval_task_inf_res_reaction(inf_obj_bbox_norm_coords, all_obj_bbox_centre_coords_wrt_screen, inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
			# top_obj_bbox_screen_y_c, top_obj_bbox_screen_x_c = single_obj_bbox_centre_coords_wrt_screen

			# top_3_obj_bbox_screen_centre_coords = all_obj_bbox_centre_coords_wrt_screen[:3]
			
			# lmc_y_c = self.current_mine_bbox_screen_centre_coords[0]
			# lmc_x_c = self.current_mine_bbox_screen_centre_coords[1]
			# print("sleeping for 1 second...")
			# time.sleep(1)
			# print("slept for 1 second!")
			# if self.mining is False or self.mine_depleted is True:
			# 	self.perform_lmc(lmc_y_c, lmc_x_c)
			# else:
			# 	pass

			# self.perform_lmc(lmc_y_c, lmc_x_c)
			# self.update_current_mine_info(inf_obj_bbox_norm_coords, all_obj_bbox_centre_coords_wrt_screen,
			#                              inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
			
			# if cv2.waitKey(1) & 0xFF == ord('q'):
			# 	cv2.destroyAllWindows()
			# 	break
		
#
# if __name__ == "__main__":
# 	from src.ui_automation_tools import screen_tools
#
# 	screen_tools.set_window_pos_and_size()
#
# 	task_name = "mining"
#
# 	client_main_view_roi_coords = (8, 31, 791, 591)
# 	roi = client_main_view_roi_coords
#
# 	obj_dect = ObjDectMainSystem(task_name, roi)
# 	obj_dect.run_obj_dect()
# 	print(f"obj_dect.inf_obj_classes: {obj_dect.inf_obj_classes}")
