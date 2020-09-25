import random
import time

# verbosity levels:
# 0: show all logs
# 1: filter out INFO logs
# 2: filter out WARN logs
# TF verbosity levels AKA loggig mech. levels of severity:
# DEBUG (level: 0)
# INFO (level: 1)
# WARN (level: 2)
# My convetion:
# level 0: show all logs,   level 1: show some logs,    level 2: show no logs


def humanize_game_tile_click_loc_coords(x, y, verbosity = 2):
	"""
	:param x: The x pixel coordinate location determined for a click to be made
	:param y: The local_y pixel coordinate location determined for a click to be made
	:param verbosity: Level corresponding to the amount of info to be printed/displayed.
	Levels are:
	0 : All info
	1: Some info
	2: No info (the default level)
	:return:
	"""
	true_x = x
	true_y = y
	randomized_x_coord_sign = 1 if random.random() < 0.5 else -1
	randomized_y_coord_sign = 1 if random.random() < 0.5 else -1
	valid_main_view_tile_rand_ints = list(range(0, 20 + 1))
	randomized_x_signed_rand_int_choice = valid_main_view_tile_rand_ints[random.randint(0, len(valid_main_view_tile_rand_ints)-1)] * randomized_x_coord_sign
	randomized_y_signed_rand_int_choice = valid_main_view_tile_rand_ints[random.randint(0, len(valid_main_view_tile_rand_ints)-1)] * randomized_y_coord_sign
	randomized_x = true_x + randomized_x_signed_rand_int_choice
	randomized_y = true_y + randomized_y_signed_rand_int_choice
	humanized_click_loc_coords_res_msgs = ["\n"*1 + "Given true x & local_y coods: {0} & {1}\nHumanized x & local_y coords: {2} & {3}".format(true_x, true_y, randomized_x, randomized_y),
										   "\n"*1 + "Humanized x & local_y coords: {0} & {1}".format(randomized_x, randomized_y)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])
	return randomized_x, randomized_y


def humanize_inv_item_slot_click_loc_coords(x, y, verbosity = 2):
	"""
	:param x: The x pixel coordinate location determined for a click to be made
	:param y: The local_y pixel coordinate location determined for a click to be made
	:param verbosity: Level corresponding to the amount of info to be printed/displayed.
	Levels are:
	0 : All info
	1: Some info
	2: No info (the default level)
	:return:
	"""
	true_x = x
	true_y = y
	randomized_x_coord_sign = 1 if random.random() < 0.5 else -1
	randomized_y_coord_sign = 1 if random.random() < 0.5 else -1
	valid_main_view_tile_rand_ints = list(range(0, 5 + 1))
	randomized_x_signed_rand_int_choice = valid_main_view_tile_rand_ints[random.randint(0, len(valid_main_view_tile_rand_ints)-1)] * randomized_x_coord_sign
	randomized_y_signed_rand_int_choice = valid_main_view_tile_rand_ints[random.randint(0, len(valid_main_view_tile_rand_ints)-1)] * randomized_y_coord_sign
	randomized_x = true_x + randomized_x_signed_rand_int_choice
	randomized_y = true_y + randomized_y_signed_rand_int_choice
	humanized_click_loc_coords_res_msgs = ["\n"*1 + "Given true x & local_y coods: {0} & {1}\nHumanized x & local_y coords: {2} & {3}".format(true_x, true_y, randomized_x, randomized_y),
										   "\n"*1 + "Humanized x & local_y coords: {0} & {1}".format(randomized_x, randomized_y)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])
	return randomized_x, randomized_y


def humanize_click_pos_coords(x, y, valid_width_interval, valid_height_interval, verbosity = 2):
	"""

	:param x: The x pixel coordinate location determined for a click to be made
	:param y: The local_y pixel coordinate location determined for a click to be made
	:param valid_width_interval: The width of the inverval in which the px coord of x is at the centre
	:param valid_height_interval: The height of the inverval in which the px coord of local_y is at the centre
	:param verbosity:
	:return: 2 ints each corresponding to a randomly generated new click loc coord for x and local_y
	"""
	true_x = x
	true_y = y
	rand_dx_sign = 1 if random.random() < 0.5 else -1
	rand_dy_sign = 1 if random.random() < 0.5 else -1
	# valid_main_view_tile_rand_ints = list(range(0, 5 + 1))
	reduced_valid_width_interval = valid_width_interval - 2
	reduced_valid_height_interval = valid_height_interval - 2
	rand_dx_mag = random.randint(0, reduced_valid_width_interval//2)
	rand_dy_mag = random.randint(0, reduced_valid_height_interval//2)
	rand_signed_dx = rand_dx_mag * rand_dx_sign
	rand_signed_dy = rand_dy_mag * rand_dy_sign
	rand_x = true_x + rand_signed_dx
	rand_y = true_y + rand_signed_dy
	humanized_click_loc_coords_res_msgs = ["\n"*1 + "Given true x & local_y coods: {0} & {1}\nHumanized x & local_y coords: {2} & {3}\nUse Width: {4} & Height: {5}".format(true_x, true_y,
	                                                                                                                                                            rand_x, rand_y,
	                                                                                                                                                            reduced_valid_width_interval,
	                                                                                                                                                            reduced_valid_height_interval),
										   "\n"*1 + "Humanized x & local_y coords: {0} & {1}".format(rand_x, rand_y)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])
	return int(rand_x), int(rand_y)




def humanize_mm_click_pos_coords(left_most_px, top_most_y, right_most_x, bottom_most_y, verbosity = 2):
	x_click_coords_bound = list(range(left_most_px, right_most_x+1))
	y_click_coords_bound = list(range(top_most_y, bottom_most_y+1))
	rand_x_click_coord = random.randint(left_most_px, right_most_x)
	rand_y_click_coord = random.randint(top_most_y, bottom_most_y)
	humanized_click_loc_coords_res_msgs = ["\n"*1 + "Bounding intervals of x & local_y coords: {0} & {1}\nRandomly chosen x & local_y coords: {2} & {3}".format(x_click_coords_bound,
	                                                                                                                                                y_click_coords_bound,
	                                                                                                                                                rand_x_click_coord,
	                                                                                                                                                rand_y_click_coord),
										   "\n"*1 + "Randomly chosenx & local_y coords: {0} & {1}".format(rand_x_click_coord, rand_y_click_coord)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])
	return int(rand_x_click_coord), int(rand_y_click_coord)


def humanize_mm_jitter_pos_coords(left_most_x, top_most_y, right_most_x, bottom_most_y,
                                  jitter_bufer=0.05, verbosity = 2):

	left_most_jitter_x = round(left_most_x-left_most_x*jitter_bufer)
	top_most_jitter_y = round(top_most_y-top_most_y*jitter_bufer)
	right_most_jitter_x = round(right_most_x+right_most_x*jitter_bufer)
	bottom_most_jitter_y = round(bottom_most_y+bottom_most_y*jitter_bufer)

	x_jitter_coords_bound = list(range(left_most_jitter_x, right_most_jitter_x + 1))
	y_jitter_coords_bound = list(range(top_most_jitter_y, bottom_most_jitter_y+1))
	rand_x_jitter_coord = random.randint(left_most_jitter_x, right_most_jitter_x)
	rand_y_jitter_coord = random.randint(top_most_jitter_y, bottom_most_jitter_y)
	humanized_click_loc_coords_res_msgs = ["\n"*1 + "Bounding intervals of jittered x & local_y coords: {0} & {1}"
	                                                "\nRandomly chosen jittered x & local_y coords: {2} & {3}".format(x_jitter_coords_bound, y_jitter_coords_bound,
	                                                                                                            rand_x_jitter_coord, rand_y_jitter_coord),
										   "\n"*1 + "Randomly chosenx jittered x& local_y coords: {0} & {1}".format(rand_x_jitter_coord, rand_y_jitter_coord)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])

	return int(rand_x_jitter_coord), int(rand_y_jitter_coord)


def humanize_mm_jitter_x_y_coords(x_coord, y_coord,
                                  jitter_bufer=0.01, verbosity=2):

	# left_most_jitter_x = round(left_most_x - left_most_x * jitter_bufer)
	# top_most_jitter_y = round(top_most_y - top_most_y * jitter_bufer)
	# right_most_jitter_x = round(right_most_x + right_most_x * jitter_bufer)
	# bottom_most_jitter_y = round(bottom_most_y + bottom_most_y * jitter_bufer)

	# x_jitter_coords_bound = list(range(left_most_jitter_x, right_most_jitter_x + 1))
	# y_jitter_coords_bound = list(range(top_most_jitter_y, bottom_most_jitter_y + 1))
	rand_x_jitter_coord = random.randint(round(x_coord-x_coord*jitter_bufer), round(x_coord*jitter_bufer+x_coord))
	rand_y_jitter_coord = random.randint(round(y_coord-y_coord*jitter_bufer), round(y_coord*jitter_bufer+y_coord))
	# rand_y_jitter_coord = random.randint(top_most_jitter_y, bottom_most_jitter_y)
	humanized_click_loc_coords_res_msgs = ["\n" * 1 + "Randomly chosenx jittered x& local_y coords: {0} & {1}".format(rand_x_jitter_coord, rand_y_jitter_coord)]

	if verbosity is not 2:
		print(humanized_click_loc_coords_res_msgs[verbosity])

	return int(rand_x_jitter_coord), int(rand_y_jitter_coord)


if __name__ == "__main__":
	pass
	# import itertools
	# inv_item_slot_x_centre_coords = [615, 655, 695, 735]
	# inv_item_slot_y_centre_coords = [275, 315, 350, 385, 420, 455, 490]
	# dyx = +/- 10
	# dyy = +/- 10
	# inv_item_slot_centre_coords = list(itertools.product(inv_item_slot_x_centre_coords, inv_item_slot_y_centre_coords))
	# iron_mine_coords = [[390, 280], [345, 320], [400, 360]]
	# for click_coords in inv_item_slot_centre_coords:
		# print(humanize_game_tile_click_loc_coords(click_coords[0], click_coords[1], verbosity=0))
		# print(humanize_click_pos_coords(click_coords[0], click_coords[1], 35, 31, verbosity=0))

	# left_most_px = 716
	# top_most_y = 114
	# right_most_x = 719
	# bottom_most_y = 117
	# rand_coords1 = humanize_mm_click_pos_coords(left_most_px, top_most_y, right_most_x, bottom_most_y, verbosity=0)
	# rand_coords2 = humanize_mm_click_pos_coords(left_most_px, top_most_y, right_most_x, bottom_most_y)
	# rand_coords3 = humanize_mm_click_pos_coords(left_most_px, top_most_y, right_most_x, bottom_most_y)
	# print("rand_coords1: ", rand_coords1)
	# print("rand_coords2: ", rand_coords2)
	# print("rand_coords3: ", rand_coords3)
	humanize_mm_jitter_x_y_coords(708, 114)
