import numpy as np
import settings


class TrajectorySceneDataHandler:
	
	# Trajectory Data Representation: A trajectory is defined as a sequence of x & y positions w.r.t time.
	# Scene DataRepresentation: A cene is represented by a N ×N grid with three channels.
	# Each grid position stores the RGB pixel values of a BEV map of the environment.
	
	def __init__(self):
		self.all_trajectories_list = []
		self.all_scenes_list = []
		self.current_traj_scene_data_list = []
		self.record_traj_scene_data = False
		
	def start_recording(self):
		self.record_traj_scene_data = True
		
	def stop_recording(self):
		self.record_traj_scene_data = False
		
	def update_traj_scene_data(self, current_scene, current_traj_pos):
		# current_scene = rgb_imgs
		# current_traj_pos = [grid_pnt_x, grid_pnt_y]
		if self.record_traj_scene_data is True:
			self.current_traj_scene_data_list.append([current_scene, current_traj_pos])
			self.all_scenes_list.append(current_scene)
			self.all_trajectories_list.append(current_traj_pos)
			
		