

if __name__ == "__main__":
	from obj_detc_sys_components.obj_dect_main_sys import ObjDectMainSystem
	from research_and_dev.event_driven_system.game_client.game_client import GameClient


	# If set_window_pos_and_size() is called w/ def parameter args,
	# i.e. (0, 0, 800, 600) then game_client_area_roi should be (8, 31, 791, 591)
	game_client = GameClient()
	game_client.set_wndw_pos_and_size()
	game_client_area_roi = game_client.get_client_area_pos_and_size()


	# Specify the task which the object detection system will be responsible of
	task_name = "mining"
	max_top_detections = 10

	obj_dect_sys = ObjDectMainSystem(task_name, game_client_area_roi, max_detections=max_top_detections)
	obj_dect_sys.run_obj_dect()
	print(f"obj_dect.current_frame_detections_dict: {obj_dect_sys.current_frame_detections_dict}")

	# //TODO: separate detections frame centroids and sceen centroids calculations
	# //TODO: add detections scores, class labels and frame centroids tracking ability in tracker

	# a = np.array([True, True, True, True, True, True, False, False, False, False])
	# acceptable_detections_idxs = np.where(a==True)
	# res = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
	# acceptable_res = res[acceptable_detections_idxs]