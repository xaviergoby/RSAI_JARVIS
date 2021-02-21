# if __name__ == "__main__":
import random
from jarvis.game_client.game_client import GameClient
from jarvis.vision_sys.vision_cls import Vision
from jarvis.utils.hardware_monitoring.hardware_events_listener import HardwareEventsListener
from jarvis.utils.time_tools import StopWatchTimer
from jarvis.utils.vision_sys_helper_util import VisionSysHelperUtil
from jarvis.hobbes_bot.hobbes import Hobbes
from jarvis.actuator_sys.mouse import Mouse
import cv2
import time
import PySimpleGUI as sg
import numpy as np
from GUI.vision_test_gui import VisionTestGUIHandler

# If set_window_pos_and_size() is called w/ def parameter args,
# i.e. (0, 0, 800, 600) then game_client_area_roi should be (8, 31, 791, 591)
game_client = GameClient()
game_client.set_wndw_pos_and_size() # osrs game window pos & dims set to (0, 0, 800, 600)
game_client_area_roi = game_client.get_client_area_pos_and_size() # -> (8, 31, 791, 591)

hw_events_listener = HardwareEventsListener()
hw_events_listener.init_all_states()

# Specify the task which the object detection system will be responsible of
max_detections = 3
confidence_threshold = 0.1
max_obj_frames_lost = 2
# screen_capture_opt = "PIL"
screen_capture_opt = "mss"
vision = Vision(game_client_area_roi, max_detections, confidence_threshold, max_obj_frames_lost, mode=screen_capture_opt)
vision.enable_manual_recording(True)

print(f"game_client_area_roi: {game_client_area_roi}")  # -> (8, 31, 791, 591)
print(f"vision.roi: {vision.roi}")  # -> (8, 31, 791, 591)
print(f"vision.img_dims: {vision.img_dims}") # -> (783, 560)

# display_util = VisionSysHelperUtil(show_all_overlaid_text_info=False)
display_util = VisionSysHelperUtil(show_obj_tracking_id=True, show_obj_centroid_coords=True)
# display_util = VisionSysHelperUtil(show_obj_tracking_id=True, show_obj_centroid_coords=False)

gui_window = VisionTestGUIHandler()

# Specify the task which the object detection system will be responsible of
task_name = "mining"
max_top_detections = 6
bot_hobbes = Hobbes(task_name, game_client_area_roi, max_detections=max_top_detections)
# obj_dect_sys.run_obj_dect()
# print(f"obj_dect.current_frame_detections_dict: {obj_dect_sys.current_frame_detections_dict}")

stop_watch = StopWatchTimer()
stop_watch.start()

stop_watch2 = StopWatchTimer()

while True:


	elapsed_time = stop_watch.get_elapsed_time()
	print(3*"\n".lstrip() + 15*"*".lstrip(), " "*5, f"Frame | Elapsed Time (Stamp): {elapsed_time}[s]", " "*5, "*"*15)
	frame = vision.sensor.get_frame() # frame.shape -> (560, 783)       //TODO###
	display_util.print_obj_dect_input_frame_info(obj_dect_input_frame = frame)

	current_detections = vision.detector.get_current_frame_detections(frame) # apparently I had removed this line in favour of the below, on 13/11/2020     //TODO####
	current_obj_dect_img_res = current_detections["inf_res_img"] # current_obj_dect_img_res.shape -> (560, 783, 3)

	confident_boxes_norm_coords, confident_boxes_scores, confident_boxes_classes = vision.detector.confident_detections(current_detections) #       //TODO####

	confident_boxes_frame_coords = vision.detector.compute_boxes_frame_coords(confident_boxes_norm_coords)  # //TODO####
	confident_boxes_frame_centroids = vision.detector.compute_boxes_frame_centroids(confident_boxes_frame_coords)  # //TODO####

	vision.tracker.update_tracking(confident_boxes_frame_centroids, confident_boxes_scores, confident_boxes_classes)  # //TODO####

	current_tracking = vision.tracker.get_current_tracking_objects() # //TODO
	current_dect_objs_centroids_dict = vision.tracker.get_current_tracking_objs_centroids()
	step_i_obj2_ds_wrt_fc = []

	# obj_centroids_lrf_ds_vectors = vision.tracker.compute_lrf_ds_vectors()
	obj_centroids_lrf_ds_vectors = vision.detector.compute_normed_bbox_lrf_ds_vectors(confident_boxes_frame_centroids)

	# cv2_window_name = "{0} Activity Object Detection\nDisplay Image Dimensions: {1}".format("Mining", current_obj_dect_img_res.shape)

	display_util.overlay_obj_dect_state_info(current_obj_dect_img_res, current_dect_objs_centroids_dict)

	# display_util.print_obj_dect_output_frame_info(obj_dect_output_frame=current_obj_dect_img_res)
	# display_util.print_tracked_lrf_centroid_ds_vectors(lrf_centroid_ds_vectors=obj_centroids_lrf_ds_vectors)
	# display_util.print_multiline_dect_objs_tracked_info(objs_tracked_dict=current_dect_objs_centroids_dict)

	print("\n"*3)

	"""
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
	"""




######################################################
	if bot_hobbes.mining is False:
		mine_2_mine_unique_id = list(current_tracking.keys())[0]
		current_tracking_bbox_mines_unique_ids = list(current_tracking.keys())
		for current_tracking_bbox_mines_unique_id_i in list(current_tracking.keys()):
			if current_tracking[current_tracking_bbox_mines_unique_id_i][2] == 1:
				mine_2_mine_unique_id = current_tracking_bbox_mines_unique_id_i
				break
			else:
				continue
		bot_hobbes.currently_mining_mine_unique_id = mine_2_mine_unique_id
		currently_mining_mine_bbox_frame_centroid_coords = current_tracking[mine_2_mine_unique_id][0]
		# print(f"currently_mining_mine_bbox_frame_centroid_coords: {currently_mining_mine_bbox_frame_centroid_coords}")
		currently_mining_mine_bbox_screen_centroid_coords = vision.detector.compute_bbox_screen_centroid(
			currently_mining_mine_bbox_frame_centroid_coords)
		lmc_x_c, lmc_y_c = currently_mining_mine_bbox_screen_centroid_coords
		Mouse.lmc(lmc_y_c, lmc_x_c)
		print("Mining Copper Mine {0}".format(bot_hobbes.currently_mining_mine_unique_id))
		bot_hobbes.mines_mined = bot_hobbes.mines_mined + 1
		bot_hobbes.tot_mined_mined = bot_hobbes.tot_mined_mined + 1
		stop_watch2.start()
		bot_hobbes.mining = True
	elif bot_hobbes.mining is True:
		if bot_hobbes.currently_mining_mine_unique_id in list(current_tracking.keys()):
			if current_tracking[bot_hobbes.currently_mining_mine_unique_id][2] == 3:
				print("Copper Mine {0} has been DEPLETED".format(bot_hobbes.currently_mining_mine_unique_id))
				bot_hobbes.mining = False
				bot_hobbes.currently_mining_mine_unique_id = None
				stop_watch2.reset()
		elif bot_hobbes.currently_mining_mine_unique_id not in list(current_tracking.keys()):
			bot_hobbes.mining = False
			bot_hobbes.currently_mining_mine_unique_id = None
			stop_watch2.reset()
	rand_num_items_2_drop = random.randint(8, 16)
	if bot_hobbes.mines_mined == rand_num_items_2_drop:
		print("Randomly dropping {0} copper ores".format(rand_num_items_2_drop))
		bot_hobbes.inv.drop_all_inv_item_by_name("copper_ore")
		bot_hobbes.mines_mined = 0
	if stop_watch2.start_time is not None:
		if stop_watch2.get_current_time_seconds_diff() >= 10:
			if bot_hobbes.mining is True:
				bot_hobbes.tot_mined_mined = bot_hobbes.tot_mined_mined - 1
				bot_hobbes.mines_mined = bot_hobbes.mines_mined - 1
			bot_hobbes.mining = False
			bot_hobbes.currently_mining_mine_unique_id = None
			stop_watch2.reset()
######################################################

	current_obj_dect_rgb_img_res = cv2.cvtColor(current_obj_dect_img_res, cv2.COLOR_BGR2RGB)

	gui_window.read()

	gui_window.update_screen_cast(screen_shot_img=current_obj_dect_rgb_img_res)

	try:
		obj_dect_info = list(current_dect_objs_centroids_dict.items())[0]  ##################################################################################
	except IndexError:
		obj_dect_info = None

	detected_objects_info_list = list(current_dect_objs_centroids_dict.items())
	lrf_ds_vectors_list_key = list(obj_centroids_lrf_ds_vectors)

	gui_window.update_objs_info(list(current_dect_objs_centroids_dict.items()))
	print(f"gui_window.update_objs_lrf_ds_vectors({list(current_dect_objs_centroids_dict.items())})")
	objs_centroid_ds_vectors = vision.tracker.compute_objs_centroid_ds_vectors()
	print(f"objs_centroid_ds_vectors: {objs_centroid_ds_vectors}")
	print(f"objs_centroid_ds_vectors.values(): {objs_centroid_ds_vectors.values()}")
	print(f"objs_centroid_ds_vectors.items(): {objs_centroid_ds_vectors.items()}")
	print(f"objs_centroid_ds_vectors type: {type(objs_centroid_ds_vectors)}")
	gui_window.update_objs_lrf_ds_vectors(list(vision.tracker.compute_objs_centroid_ds_vectors().items()))
	print(f"gui_window.update_objs_lrf_ds_vectors({list(vision.tracker.compute_objs_centroid_ds_vectors().items())})")

	# print(f"len(confident_boxes_frame_centroids): {len(confident_boxes_frame_centroids)}")
	print(f"obj_dect_info: {obj_dect_info}")
	print(f"confident_boxes_frame_centroids: {confident_boxes_frame_centroids}")
	all_inf_obj_bbox_centre_screen_coords = vision.detector.compute_all_inf_obj_bbox_centre_screen_coords(
		confident_boxes_norm_coords)
	print(f"type(all_inf_obj_bbox_centre_screen_coords): {type(all_inf_obj_bbox_centre_screen_coords)}")
	print(f"all_inf_obj_bbox_centre_screen_coords: {all_inf_obj_bbox_centre_screen_coords}")
	print(f"type(obj_centroids_lrf_ds_vectors): {type(obj_centroids_lrf_ds_vectors)}")
	# print(f"obj_centroids_lrf_ds_vectors.shape: {obj_centroids_lrf_ds_vectors.shape}")
	print(f"obj_centroids_lrf_ds_vectors: {obj_centroids_lrf_ds_vectors}")


#################

	if hw_events_listener.R_clicked is True:
		# elapsed_time = stop_watch.get_elapsed_time()
		####
		# vision.update_visual_memory(current_dect_objs_centroids_dict, elapsed_time, frame)
		# cv2.imwrite("obj_dect_frame_at_{0}.PNG".format(str(elapsed_time)), current_obj_dect_rgb_img_res)
		####
		# cv2.destroyAllWindows()
		break
	else:
		pass

	hw_events_listener.update_all_states()

# event, values = gui_window.Read(timeout=20, timeout_key='timeout')  # get events for the window with 20ms max wait
# gui_window.FindElement('screen_shot_image').Update(data=cv2.imencode('.png', frame)[1].tobytes())  # Update image in window
