from src.path_manipulation_tools import file_path_tools
import os
from research_and_dev.event_driven_system.actuators import actuators_cls
from src.data_tools.obj_dect_data_tools.abc_obj_dect_data_collector import ObjDectABCDataCollector
import pyautogui
import settings


class TaskObjDectDataCollector(ObjDectABCDataCollector):
	
	def __init__(self, task_name, roi):
		self.task_name = task_name
		self.roi = roi
		self.paused = False
		self.task_obj_dect_data_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}\all".format(self.task_name))
		self.task_obj_dect_rgb_imgs_dir = os.path.join(self.task_obj_dect_data_dir, "rgb_images")
		self.task_obj_dect_grey_imgs_dir = os.path.join(self.task_obj_dect_data_dir, "grey_images")
		self.task_obj_dect_npy_arrays_dir = os.path.join(self.task_obj_dect_data_dir, "npy_arrays")
		self.actuators = actuators_cls.Actuators()
		self.current_num_rgb_images_captured = 0
		self.current_num_grey_images_captured = 0
		self.current_num_npy_arrays_captured = 0
		
	def _get_num_of_rgb_images(self):
		num_rgb_images = os.listdir(self.task_obj_dect_rgb_imgs_dir)
		return len(num_rgb_images)
	
	def _get_num_of_grey_images(self):
		num_grey_images = os.listdir(self.task_obj_dect_grey_imgs_dir)
		return len(num_grey_images)
	
	def _get_num_of_npy_arrays(self):
		num_npy_arrays = os.listdir(self.task_obj_dect_npy_arrays_dir)
		return len(num_npy_arrays)
	
	@property
	def tot_num_rgb_images(self):
		return self._get_num_of_rgb_images()
	
	@property
	def tot_num_grey_images(self):
		return self._get_num_of_grey_images()
	
	@property
	def tot_num_npy_arrays(self):
		return self._get_num_of_npy_arrays()
	
	def run_data_collector(self):
		self.actuators.init_all_states()
		last_saved_rgb_img_file_name = file_path_tools.get_most_recent_data_file_name(self.task_obj_dect_rgb_imgs_dir)
		if last_saved_rgb_img_file_name is False:
			rgb_img_cnt_idx = 0
		else:
			last_saved_rgb_img_file_idx_int = int(last_saved_rgb_img_file_name.split(".")[0].split("_")[-1])
			rgb_img_cnt_idx = last_saved_rgb_img_file_idx_int
			
		while True:
			
			if self.paused is False:
				
				if self.actuators.C_clicked is True:
					
					rgb_img_cnt_idx = rgb_img_cnt_idx + 1
					self.current_num_rgb_images_captured = self.current_num_rgb_images_captured + 1
					rgb_img_file_name = "{0}_{1}.png".format(self.task_name, rgb_img_cnt_idx)
					rgb_img_file_path = os.path.join(self.task_obj_dect_rgb_imgs_dir, rgb_img_file_name)
					pyautogui.screenshot(rgb_img_file_path, region=self.roi)
					print("Total number of rgb img screen shots captured: {0}".format(self.tot_num_rgb_images))
					print("Current run number of screen shots captured: {0}".format(self.current_num_rgb_images_captured))
					
				elif self.actuators.P_clicked is True:
					print("paused...")
					self.paused = True
				
				elif self.actuators.T_clicked is True:
					print("Terminating {0} task data collection...".format(self.task_name))
					print("Total number of rgb img screen shots captured: {0}".format(self.tot_num_rgb_images))
					print("Current run number of screen shots captured: {0}".format(self.current_num_rgb_images_captured))
					break
					
				else:
					continue
			
			elif self.paused is True:
				if self.actuators.P_clicked is True:
					print("unpaused...")
					self.paused = False
						
			self.actuators.update_all_states()
			print("Updating keyboard key states...")
		
		
		
	
	
		
		
if __name__ == "__main__":
	from src.utils.time_tools import delay_timer
	from src.ui_automation_tools import screen_tools
	task_name = "mining"
	delay_timer(3)
	screen_tools.set_window_pos_and_size()
	roi = screen_tools.get_client_tl_pos_and_area_dims()
	task_obj_data_collector = TaskObjDectDataCollector(task_name="mining", roi=roi)
	task_obj_data_collector.run_data_collector()
	
	#
