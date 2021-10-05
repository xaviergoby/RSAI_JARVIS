import numpy as np
from PIL import Image
import datetime
from research_and_dev.slam import minimap_grid
import pyautogui
from src.ui_automation_tools import screen_tools
import settings
import time
import cv2
from PIL import ImageGrab
from src.ui_automation_tools import mouse_events_monitoring
# from research_and_dev.misc_slam import mini_map


# mm_rad_sq_len = 10 # OG px mm_rad_sq_len choice
# mm_rad_sq_len = 14 # max possible
mm_radius_sq_len = 6
# mm = mini_map.MiniMap(mm_radius_sq_len=mm_radius_sq_len)
mm = minimap_grid.MiniMapGrid(mm_radius_sq_len=mm_radius_sq_len)
mm.create_mm_grid_cells_coords()
x = mm.reshape_cells_coords_list_to_array()
print("local_x: {0}".format(x))
mm_coords = mm.convert_mouse_click_screen_coords_2_mm_local_grid_coords(726, 110)
print(mm_coords)

print("mm_side_sq_len: {0}".format(mm.mm_side_sq_len))
print("grid_leftmost_cell_x: {0}".format(mm.grid_leftmost_cell_x))
print("grid_topmost_cell_y: {0}".format(mm.grid_topmost_cell_y))
print("grid_righttmost_cell_x: {0}".format(mm.grid_righttmost_cell_x))
print("grid_bottomtmost_cell_y: {0}".format(mm.grid_bottomtmost_cell_y))
print("grid_coords_cell_objs_key_value_pair_dict: {0}".format(mm.grid_coords_cell_objs_key_value_pair_dict))
print(mm.grid_coords_cell_objs_key_value_pair_dict[(-mm_radius_sq_len, 0)].left_most_px)
print(mm.grid_coords_cell_objs_key_value_pair_dict[(0, -mm_radius_sq_len)].top_most_px)
print(mm.grid_coords_cell_objs_key_value_pair_dict[(mm_radius_sq_len, 0)].right_most_px)
print(mm.grid_coords_cell_objs_key_value_pair_dict[(0, mm_radius_sq_len)].bottom_most_px)

mm_left = mm.grid_coords_cell_objs_key_value_pair_dict[(-mm_radius_sq_len, 0)].left_most_px
mm_top = mm.grid_coords_cell_objs_key_value_pair_dict[(0, -mm_radius_sq_len)].top_most_px
mm_right = mm.grid_coords_cell_objs_key_value_pair_dict[(mm_radius_sq_len, 0)].right_most_px
mm_bottom = mm.grid_coords_cell_objs_key_value_pair_dict[(0, mm_radius_sq_len)].bottom_most_px

width = mm_right - mm_left
height = mm_bottom - mm_top


# Adjust the OSRS window's position on the screen and the dimensions of the window
# screen_tools.adjust_wndw_pos_and_dims()
screen_tools.set_window_pos_and_size()
time.sleep(2)
mm_screen_region = (mm_left, mm_top, width+1, height+1)
mm_screen_dims = (mm_left, mm_top, mm_right+1, mm_bottom+1)

img_width = mm_right+1 - mm_left
img_height = mm_bottom+1 - mm_top
og_dim = (img_width, img_height)

print(f"mm_screen_region: {mm_screen_region}")
print(f"mm_screen_dims: {mm_screen_dims}")
init_key_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
while True:
	# print("Displaying screen cast")
	time.sleep(0.618)
	printscreen = np.array(ImageGrab.grab(bbox=mm_screen_dims))
	rgb_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
	grey_scale = cv2.cvtColor(printscreen, cv2.COLOR_BGR2GRAY)

	og_dim_display_img = grey_scale

	scale_percent = 220  # percent of original size
	new_width = int(img_height * scale_percent / 100)
	new_height = int(img_width * scale_percent / 100)
	new_dim = (new_width, new_height)
	resized = cv2.resize(og_dim_display_img, new_dim, interpolation=cv2.INTER_AREA)

	# w/ threshold1 = 190 other players are represented by a reasonable shape made of pixels!
	ret, thresholded_img = cv2.threshold(og_dim_display_img, 125, 255, cv2.THRESH_BINARY) # optimal#1: 190, 225

	display_img = thresholded_img
	current_time_in_sec = datetime.datetime.now().strftime('%S')
	im = Image.fromarray(display_img)
	im.save("altered_mm_img_{0}_{1}_{2}.PNG".format(display_img.shape[0], display_img.shape[1], current_time_in_sec))


	img_wndw_name = 'Mm w/ {0} side px len sq scrnshoot'.format(mm_radius_sq_len * 2 + 1)
	cv2.namedWindow(img_wndw_name, cv2.WINDOW_NORMAL)

	cv2.imshow(img_wndw_name, display_img)
	# print("print statement after cv2.imshow(img_wndw_name, display_img)")

	coords = pyautogui.position()
	mouse_click_events = mouse_events_monitoring.get_mouse_click_events(init_key_states, settings.mouse_nVirtKey_dict)
	print("current loc: {0}".format(mm.current_world_grid_coords))
	if mouse_events_monitoring.mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
		print("\nMouse Click Event Detected")
		clicked_mouse_button = mouse_events_monitoring.get_mouse_button_clicked_str(mouse_click_events)
		print("Mouse Button Clicked: {0}".format(clicked_mouse_button))
		print("{0} Click Location Coordinates: {1}".format(clicked_mouse_button, coords))
		# wm_grid = mm.get_mm_coords_from_mouse_click_coords(coords[0], coords[1])
		mouse_click_world_grid = mm.get_world_grid_coords_from_mouse_click_coords(coords)
		mm.update_current_world_grid_coords(mouse_click_world_grid)
		# print("current loc: {0}".format(mm.current_wg_coords))
		# init current_wg_coords is = 3216, 3219
		print("World map grid coords: {0}, {1}".format(mouse_click_world_grid[0], mouse_click_world_grid[1]))
		print("Current grid coords loc: {0}".format(mouse_click_world_grid))
		print("Updating LMB & RMB initial key states...\n")
		init_key_states = mouse_events_monitoring.update_mouse_states(init_key_states, mouse_click_events)
		# print("key press monitoring code block reached")
	# else:
	# 	print("pass hit")
	# 	pass
		# print("No Click Event Detected")
	# cv2.imshow(img_wndw_name, cv2.cvtColor(display_img, cv2.COLOR_GRAY2RGB))
	k = cv2.waitKey(25)
	if k & 0xFF == ord('q'):
		cv2.imwrite("altered_mm_img_{0}_{1}.PNG".format(display_img.shape[0], display_img.shape[1]), display_img)
		cv2.imwrite("grey_scale_mm_img_{0}_{1}.PNG".format(grey_scale.shape[0], grey_scale.shape[1]), grey_scale)
		pyautogui.screenshot("og_mm_img_{0}_{1}.PNG".format(img_width, img_height), region=mm_screen_region)
		cv2.destroyAllWindows()
		break

# 	print("while loop code block end reached")
# print("while loop end reached")
