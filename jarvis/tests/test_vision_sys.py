


if __name__ == "__main__":
	from jarvis.game_client.game_client import GameClient
	from jarvis.vision_sys.vision_cls import Vision
	from jarvis.utils.hardware_monitoring.hardware_events_listener import HardwareEventsListener
	from jarvis.utils.time_tools import StopWatchTimer
	import cv2
	import time
	import numpy as np

	# If set_window_pos_and_size() is called w/ def parameter args,
	# i.e. (0, 0, 800, 600) then game_client_area_roi should be (8, 31, 791, 591)
	game_client = GameClient()
	game_client.set_wndw_pos_and_size() # osrs game window pos & dims set to (0, 0, 800, 600)
	game_client_area_roi = game_client.get_client_area_pos_and_size() # -> (8, 31, 783, 560)

	hw_events_listener = HardwareEventsListener()
	hw_events_listener.init_all_states()

	# Specify the task which the object detection system will be responsible of
	max_detections = 3
	confidence_threshold = 0.1
	max_obj_frames_lost = 2
	vision = Vision(game_client_area_roi, max_detections, confidence_threshold, max_obj_frames_lost)
	vision.enable_manual_recording(True)

	bbox_c_pnt_colour = (0, 255, 0)
	text_colour = (0, 0, 0) # black

	stop_watch = StopWatchTimer()
	stop_watch.start()

	while True:
		print("\n")
		frame = vision.sensor.get_frame() # frame.shape -> (560, 783)

		current_detections = vision.detector.get_current_frame_detections(frame)
		current_obj_dect_img_res = current_detections["inf_res_img"] # current_obj_dect_img_res.shape -> (560, 783, 3)

		confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes = vision.detector.confident_detections(current_detections)
		
		confident_boxes_frame_coords = vision.detector.compute_boxes_frame_coords(confident_boxes_norm_coords)
		confident_boxes_frame_centroids = vision.detector.compute_boxes_frame_centroids(confident_boxes_frame_coords)

		vision.tracker.update_tracking(confident_boxes_frame_centroids, confident_boxes_scores, confident_boxes_classes)

		current_obj_centroids = vision.tracker.get_current_tracking_objs_centroids()
		
		obj_centroids_lrf_ds_vectors = vision.tracker.compute_lrf_ds_vectors()

		if hw_events_listener.R_clicked is True:
			elapsed_time = stop_watch.get_elapsed_time()
			vision.update_visual_memory(current_obj_centroids, elapsed_time, current_obj_dect_img_res)
			cv2.imwrite("obj_DT_frame_cap_At_{0}.PNG".format(str(elapsed_time)), cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
		else:
			pass

		step_i_obj2_ds_wrt_fc = []

		frame_ic = int(current_obj_dect_img_res.shape[0]//2) # 280
		frame_jc = int(current_obj_dect_img_res.shape[1]//2) #
		print(f"Frame shape (height, width, channels): {frame.shape}")
		print(f"Frame centre coordinates (pxy, pxx)↔(row i, col j): {(frame_ic, frame_jc)}")
		print(f"compute_lrf_ds_vectors: {vision.tracker.compute_lrf_ds_vectors()}")
		cv2_window_name = "{0} Object Detection | Image Dimen/sions: {1}".format("mining", current_obj_dect_img_res.shape)
		# cv2.moveWindow(cv2_window_name, 1080, 0)
		

		for (tracking_id_i, centroid_i) in current_obj_centroids.items():
			text = "Mine ID:{0}".format(tracking_id_i)
			obj_frame_centroid_pos = (centroid_i[0], centroid_i[1])
			obj_frame_centroid_pos_info = f"Obj Centroid: {(centroid_i[0], centroid_i[1])}"
			# obj_frame_centroid_pos_info = f"Obj Centroid (pxx, pxy)↔(col j, row i): {(centroid_i[0], centroid_i[1])}"
			print(f"Obj ID {tracking_id_i} screen centroid pos coords (pxy, pxx)↔(row i, col j): {(centroid_i[1], centroid_i[0])}")
			obj_frame_centroid_d2c_ds_vect = (obj_frame_centroid_pos[0]+current_obj_dect_img_res.shape[1]//2,
			                                  obj_frame_centroid_pos[1]+current_obj_dect_img_res.shape[0]//2)
			obj_frame_centroid_d2c_ds_vect_info = f"obj frame ds to centre vect: {obj_frame_centroid_d2c_ds_vect}"
			text_vertical_offset = 15
			cv2.putText(current_obj_dect_img_res, text, (centroid_i[0], centroid_i[1] + 0 * text_vertical_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_colour, 2)
			cv2.putText(current_obj_dect_img_res, obj_frame_centroid_pos_info, (centroid_i[0], centroid_i[1] + 1*text_vertical_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_colour, 2)
			cv2.circle(current_obj_dect_img_res, (centroid_i[0], centroid_i[1] + 0 * text_vertical_offset), 4, bbox_c_pnt_colour, -1)
			# cv2.circle(current_obj_dect_img_res, (centroid_i[0], centroid_i[1] + 1 * text_vertical_offset), 4, (0, 255, 0), -1)

		cv2.imshow(cv2_window_name, cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))

		if hw_events_listener.R_clicked is True:
			elapsed_time = stop_watch.get_elapsed_time()
			vision.update_visual_memory(current_obj_centroids, elapsed_time, frame)
			cv2.imwrite("obj_DT_frame_cap_At_{0}.PNG".format(str(elapsed_time)), cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
		else:
			pass

		hw_events_listener.update_all_states()


		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.imwrite("mining_with_obj_dect_sys_T1.PNG", cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
			cv2.destroyAllWindows()
			break
			
		time.sleep(0.6)