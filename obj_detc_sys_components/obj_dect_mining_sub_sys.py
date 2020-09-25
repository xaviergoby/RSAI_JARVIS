import settings
import numpy as np
import os



class ObjDectMiningSubSystem:
	
	def __init__(self):
		self.mining = False
		# self.current_mine_depletion_state = None
		### cls instance attributes for the mine which is in the process of being mined
		self.current_mine_obj_dect_inf_res = None
		self.current_mine_bbox_norm_coords = None
		self.current_mine_bbox_screen_centre_coords = None
		self.current_mine_score = None
		self.current_mine_class_label = None
		self.current_mine_class_label_name = None
		### cls instance attributes for the complete res of obj dect inf at a given "current" step
		self.current_step_obj_dect_inf_res = None
		self.current_step_bbox_norm_coords = None
		self.current_step_bbox_screen_centre_coords = None
		self.current_step_scores = None
		self.current_step_classes = None
		self.current_step_num_obj_dect_infered = None
		
	def update_current_step_obj_dect_inf_res(self, inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections):
		self.current_step_obj_dect_inf_res = (inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
		self.current_step_bbox_norm_coords = inf_obj_bbox_norm_coords
		self.current_step_bbox_screen_centre_coords = all_inf_obj_bbox_centre_screen_coords
		self.current_step_scores = inf_obj_scores
		self.current_step_classes = inf_obj_classes
		self.current_step_num_obj_dect_infered = inf_obj_num_detections
		
	def update_current_mine_info(self, inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections):
		self.current_mine_obj_dect_inf_res = (inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
		self.current_mine_bbox_norm_coords = inf_obj_bbox_norm_coords
		self.current_mine_bbox_screen_centre_coords = all_inf_obj_bbox_centre_screen_coords
		self.current_mine_score = inf_obj_scores
		self.current_mine_class_label = inf_obj_classes
		# self.current_mine_class_label_name = inf_obj_num_detections
	
	def mine(self, inf_obj_dect_res_bbox_norm_coords, all_inf_obj_dect_res_bbox_centre_screen_coords,
	         inf_obj_dect_res_scores, inf_obj_dect_res_classes, inf_obj_dect_res_num_detections):
		self.update_current_step_obj_dect_inf_res(inf_obj_dect_res_bbox_norm_coords, all_inf_obj_dect_res_bbox_centre_screen_coords,
		                                          inf_obj_dect_res_scores, inf_obj_dect_res_classes, inf_obj_dect_res_num_detections)
		if self.mining is False and self.mine_depleted is True:
			self.update_current_mine_info(inf_obj_dect_res_bbox_norm_coords[0], all_inf_obj_dect_res_bbox_centre_screen_coords[0],
			                              inf_obj_dect_res_scores[0], inf_obj_dect_res_classes[0], inf_obj_dect_res_num_detections)
			# self.mining = True
			return self.current_mine_bbox_screen_centre_coords
		elif self.mining is True and self.mine_depleted is True:
			self.update_current_mine_info(inf_obj_dect_res_bbox_norm_coords[0],
			                              all_inf_obj_dect_res_bbox_centre_screen_coords[0],
			                              inf_obj_dect_res_scores[0], inf_obj_dect_res_classes[0],
			                              inf_obj_dect_res_num_detections)
			self.mining = False
			# return self.current_mine_bbox_screen_centre_coords
		elif self.mining is False and self.mine_depleted is False:
			self.update_current_mine_info(inf_obj_dect_res_bbox_norm_coords[0],
			                              all_inf_obj_dect_res_bbox_centre_screen_coords[0],
			                              inf_obj_dect_res_scores[0], inf_obj_dect_res_classes[0],
			                              inf_obj_dect_res_num_detections)
			self.mining = True
			return self.current_mine_bbox_screen_centre_coords[0]
		elif self.mining is True and self.mine_depleted is False:
			pass
	
	@property
	def mine_depleted(self):
		current_norm_y_min, current_norm_x_min, current_norm_y_max, current_norm_x_max = self.current_mine_bbox_norm_coords
		current_norm_x_diff = (current_norm_x_max - current_norm_x_min)/2
		current_norm_y_diff = (current_norm_y_max - current_norm_y_min)/2
		current_norm_x_mid = current_norm_x_min + current_norm_x_diff
		current_norm_y_mid = current_norm_y_min + current_norm_y_diff
		# current_screen_y_min, current_screen_x_min, current_screen_y_max, current_screen_x_max = self.current_mine_bbox_screen_centre_coords
		depleted_mines_inf_objs_idx_list = []
		inf_depleted_mine_obj_bbox_norm_coords_list = []
		# depleted_mines_inf_objs_bbox_norm_coords_list = []
		inf_depleted_mine_obj_bbox_centre_screen_coords_list = []
		inf_depleted_mine_obj_scores_list = []
		inf_obj_classes_list = self.current_step_classes.tolist()
		for inf_obj_idx_i in range(len(inf_obj_classes_list)):
			inf_obj_idx_i_class_label = inf_obj_classes_list[inf_obj_idx_i]
			if inf_obj_idx_i_class_label == 3:
				depleted_mines_inf_objs_idx_list.append(inf_obj_idx_i)
		for inf_depleted_mine_obj_idx_i in depleted_mines_inf_objs_idx_list:
			inf_depleted_mine_obj_bbox_norm_coords_list.append(self.current_step_bbox_norm_coords[inf_depleted_mine_obj_idx_i])
			inf_depleted_mine_obj_bbox_centre_screen_coords_list.append(self.current_step_bbox_screen_centre_coords[inf_depleted_mine_obj_idx_i])
			inf_depleted_mine_obj_scores_list.append(self.current_step_scores[inf_depleted_mine_obj_idx_i])
		
		for inf_depleted_mine_obj_bbox_norm_coords_i in inf_depleted_mine_obj_bbox_norm_coords_list:
			inf_depleted_mine_obj_bbox_norm_y_min  = inf_depleted_mine_obj_bbox_norm_coords_i[0]
			inf_depleted_mine_obj_bbox_norm_x_min  = inf_depleted_mine_obj_bbox_norm_coords_i[1]
			inf_depleted_mine_obj_bbox_norm_y_max  = inf_depleted_mine_obj_bbox_norm_coords_i[2]
			inf_depleted_mine_obj_bbox_norm_x_max  = inf_depleted_mine_obj_bbox_norm_coords_i[3]
			
			inf_depleted_mine_obj_bbox_norm_x_diff = (inf_depleted_mine_obj_bbox_norm_x_max - inf_depleted_mine_obj_bbox_norm_x_min) / 2
			inf_depleted_mine_obj_bbox_norm_y_diff = (inf_depleted_mine_obj_bbox_norm_y_max - inf_depleted_mine_obj_bbox_norm_y_min) / 2
			inf_depleted_mine_obj_bbox_norm_x_mid = current_norm_x_min + inf_depleted_mine_obj_bbox_norm_x_diff
			inf_depleted_mine_obj_bbox_norm_y_mid = current_norm_y_min + inf_depleted_mine_obj_bbox_norm_y_diff
			
			if inf_depleted_mine_obj_bbox_norm_x_mid <= current_norm_x_mid + (current_norm_x_diff / 2) or inf_depleted_mine_obj_bbox_norm_x_mid <= current_norm_x_mid + (current_norm_x_diff):
				if inf_depleted_mine_obj_bbox_norm_y_mid <= current_norm_y_mid + (current_norm_y_diff / 2) or inf_depleted_mine_obj_bbox_norm_y_mid <= current_norm_y_mid + (current_norm_y_diff):
					return True
				else:
					pass
			else:
				return False
		# if self.mining is False:
		# 	return False
				
			# elif inf_depleted_mine_obj_bbox_norm_x_mid <= current_norm_x_mid + (current_norm_x_diff
			
			# if
			
		# if 3 in self.inf_obj_classes.tolist():
		# return False
	
	def check_mining_depletion_state(self):
		norm_y_min, norm_x_min, norm_y_max, norm_x_max = self.current_mine_bbox_norm_coords
		pass
		
	def mine(self, inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections):
		self.update_current_mine_info(inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
	
	def mine_inf_obj(self, highest_acc_inf_obj_bbox_norm_coords, highest_acc_inf_obj_class):
		return highest_acc_inf_obj_bbox_norm_coords, highest_acc_inf_obj_class
		
	def eval_task_inf_res_reaction(self, inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections):
		# self.current_mine_obj_dect_inf_res = (
		# inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes,
		# inf_obj_num_detections)
		# self.current_mine_bbox_norm_coords = inf_obj_bbox_norm_coords
		# self.current_mine_bbox_screen_centre_coords = all_inf_obj_bbox_centre_screen_coords
		# self.current_mine_score = inf_obj_scores
		# self.current_mine_class_label = inf_obj_classes
		self.update_current_mine_info(inf_obj_bbox_norm_coords, all_inf_obj_bbox_centre_screen_coords, inf_obj_scores, inf_obj_classes, inf_obj_num_detections)
		if self.mining is False:
			highest_acc_obj_inf_info = (self.inf_obj_bbox_norm_coords[0], self.all_inf_obj_bbox_centre_screen_coords[0], self.inf_obj_scores[0], self.inf_obj_classes[0])
			top_acc_score_inf_obj_class_label = highest_acc_obj_inf_info[3]
			if top_acc_score_inf_obj_class_label == 1:  # copper_mine
				self.current_mine_bbox_norm_coords = highest_acc_obj_inf_info[0]
				self.current_mine_bbox_screen_centre_coords = highest_acc_obj_inf_info[1]
				self.current_mine_score = highest_acc_obj_inf_info[2]
				self.current_mine_class_label = highest_acc_obj_inf_info[3]
				print(f"type(current_mine_class_label): {type(self.current_mine_class_label)}")
				print(f"self.current_mine_class_label==1: {self.current_mine_class_label==1}")
				self.mining = True
			else:
				pass
			# if self.current_mine_class_label == 1: # copper_mine
			# 	self.mining = True
			# 	return self.current_mine_bbox_screen_centre_coords[0], self.current_mine_bbox_screen_centre_coords[1]
		elif self.mining is True:
			if self.mine_depleted is True:
				print(f"self.mine_depleted: {self.mine_depleted}")
				print("THIS MINE HAS BEEN DEPLETED")
				self.mining = False
			else:
				pass
			
			
			# highest_acc_inf_obj_bbox_norm_coords = highest_acc_obj_inf_info[0]
			# highest_acc_inf_obj_bbox_centre_screen_coords = highest_acc_obj_inf_info[1]
			# highest_acc_inf_obj_score = highest_acc_obj_inf_info[2]
			# highest_acc_inf_obj_class = highest_acc_obj_inf_info[3]
			
		tot_num_objs_inf = inf_obj_num_detections
		if self.mining is False:
			highest_acc_obj_inf_info = (inf_obj_bbox_norm_coords[0], inf_obj_scores[0], inf_obj_classes[0])
			highest_acc_inf_obj_bbox_norm_coords = highest_acc_obj_inf_info[0]
			highest_acc_inf_obj_score = highest_acc_obj_inf_info[0]
			highest_acc_inf_obj_class = highest_acc_obj_inf_info[2]
			return self.mine_inf_obj(highest_acc_inf_obj_bbox_norm_coords, highest_acc_inf_obj_class)
			# return self.mine_inf_obj(highest_acc_inf_obj_bbox_norm_coords, highest_acc_inf_obj_class)
		elif self.mining is True:
			pass
		else:
			pass
		
		
		