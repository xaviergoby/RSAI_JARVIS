from abc import ABC, abstractmethod
import numpy as np
from scipy.spatial import distance as dist
from collections import OrderedDict

class ObjDectTaskABC(ABC): # <-- Parent AKA Superclass

	@abstractmethod
	def update_task(self, inf_res):
		# self.evaluate_inf_res(inf_res)
		raise NotImplementedError

	@abstractmethod
	def evaluate_inf_res(self):
		raise NotImplementedError


class ObjDectMiningTask(ObjDectTaskABC): # <-- Child AKA Subclass
	# boxes, obj_scores, classes, num_detections, img
	# copper_mine: 1
	# tin_mine: 2
	# depleted_mine: 3

	def __init__(self):
		self.task_name = "mining"
		self.mining = False
		self.mines_history = []
		self.mining_history = []
		self.current_tracking = OrderedDict()
		self.current_inf_obj_unique_id = 0
		# self.task_active = False
		# self.current_inf_res_dict = None

	def update_task(self, inf_res):
		self.current_inf_res = inf_res
		if self.mining is False:
			if self.copper_mine_detected is True:
				inf_res_copper_mine_idxs = np.where(self.current_inf_res["classes"] == 1)[0]
				top_inf_res_copper_mine_score = self.current_inf_res["obj_scores"][inf_res_copper_mine_idxs[0]]
				top_inf_res_copper_mine_norm_bbox = self.current_inf_res["norm_boxes"][inf_res_copper_mine_idxs[0]]
				self.mining = "copper_mine"
				self.mines_history.append((self.mining, top_inf_res_copper_mine_norm_bbox, top_inf_res_copper_mine_score))
		elif self.mining is True:
			if self.depleted_mine_detected is True:
				inf_res_depleted_mine_idxs = np.where(self.current_inf_res["classes"] == 3)[0]
				inf_res_depleted_mine_norm_boxes = self.current_inf_res["norm_boxes"][inf_res_depleted_mine_idxs]

		self.evaluate_inf_res()
		pass

	def evaluate_inf_res(self,):
		pass

	@property
	def copper_mine_detected(self):
		if 1 in self.current_inf_res["classes"]:
			return True
		else:
			return False

	@property
	def tin_mine_detected(self):
		if 1 in self.current_inf_res["classes"]:
			return True
		else:
			return False

	@property
	def depleted_mine_detected(self):
		if 1 in self.current_inf_res["classes"]:
			return True
		else:
			return False

	def get_classes_top_inf_idxs(self, inf_res_classes):
		pass