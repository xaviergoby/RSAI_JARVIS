# if __name__ == "__main__":
from jarvis.game_client.game_client import GameClient
from jarvis.vision_sys.vision_cls import Vision
from jarvis.utils.hardware_monitoring.hardware_events_listener import HardwareEventsListener
from jarvis.utils.time_tools import StopWatchTimer
from jarvis.utils.vision_sys_helper_util import VisionSysHelperUtil
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

display_util = VisionSysHelperUtil(show_all_overlaid_text_info=False)

stop_watch = StopWatchTimer()
stop_watch.start()

while True:
	elapsed_time = stop_watch.get_elapsed_time()
	print(3*"\n".lstrip() + 5*"*".lstrip(), " "*5, f"Frame | Elapsed Time (Stamp): {elapsed_time}", " "*5, "*"*5)
	frame = vision.sensor.get_frame() # frame.shape -> (560, 783)
	display_util.print_obj_dect_input_frame_info(obj_dect_input_frame = frame)

	current_detections = vision.detector.get_current_frame_detections(frame) # apparently I had removed this line in favour of the below, on 13/11/2020
	current_obj_dect_img_res = current_detections["inf_res_img"] # current_obj_dect_img_res.shape -> (560, 783, 3)

	confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes = vision.detector.confident_detections(current_detections)

	confident_boxes_frame_coords = vision.detector.compute_boxes_frame_coords(confident_boxes_norm_coords)
	confident_boxes_frame_centroids = vision.detector.compute_boxes_frame_centroids(confident_boxes_frame_coords)

	vision.tracker.update_tracking(confident_boxes_frame_centroids, confident_boxes_scores, confident_boxes_classes)

	current_dect_objs_centroids_dict = vision.tracker.get_current_tracking_objs_centroids()

	step_i_obj2_ds_wrt_fc = []

	display_util.print_obj_dect_output_frame_info(obj_dect_output_frame=current_obj_dect_img_res)

	obj_centroids_lrf_ds_vectors = vision.tracker.compute_lrf_ds_vectors()
	display_util.print_tracked_lrf_centroid_ds_vectors(lrf_centroid_ds_vectors=obj_centroids_lrf_ds_vectors)

	display_util.print_multiline_dect_objs_tracked_info(objs_tracked_dict=current_dect_objs_centroids_dict)

	cv2_window_name = "{0} Activity Object Detection\nDisplay Image Dimensions: {1}".format("Mining", current_obj_dect_img_res.shape)

	display_util.overlay_obj_dect_state_info(current_obj_dect_img_res, current_dect_objs_centroids_dict)

	print("\n"*3)

	cv2.imshow(cv2_window_name, cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))

	if hw_events_listener.R_clicked is True:
		# elapsed_time = stop_watch.get_elapsed_time()
		vision.update_visual_memory(current_dect_objs_centroids_dict, elapsed_time, frame)
		cv2.imwrite("obj_DT_frame_cap_At_{0}.PNG".format(str(elapsed_time)), cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
		cv2.destroyAllWindows()
		break
	else:
		pass

	hw_events_listener.update_all_states()


	if cv2.waitKey(1) & 0xFF == ord('q'):
		# cv2.imwrite("mining_with_obj_dect_sys_T1.PNG", cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
		cv2.imwrite("obj_DT_frame_cap_At_{0}.PNG".format(str(elapsed_time)), cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB))
		cv2.destroyAllWindows()
		break

	time.sleep(0.6)