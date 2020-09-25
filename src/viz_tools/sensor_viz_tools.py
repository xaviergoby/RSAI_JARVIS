import numpy as np
# from models.research.object_detection.utils import label_map_util
# from models.research.object_detection.utils import visualization_utils as vis_util
import matplotlib
matplotlib.use("TkAgg")  # Do this before importing pyplot!
# matplotlib.use('module://backend_interagg')
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt

class StaticROISensor:

	def __init__(self, starting_coords=None, origin_coords=None, roi_name="grid", region_dimensions=None):
		self.starting_coords = starting_coords
		self.region_dimensions = region_dimensions
		self.origin_coords = origin_coords
		self.roi_name = roi_name
		self.roi_dims_dict = {"grid":[64, 64]}
		self.roi_origin_coords_dict = {"grid":[00, 00]}
		self.i = None
		self.x_path_points = []
		self.y_path_points = []


	def create_static_roi_array(self):
		if self.region_dimensions is None:
			roi_dims = self.roi_dims_dict[self.roi_name]
			roi_width = roi_dims[0]
			roi_height = roi_dims[1]
			# origin_coords = self.roi_origin_coords_dict[self.roi_name]
		elif self.region_dimensions is not None and self.roi_name is None:
			roi_width = self.region_dimensions[0]
			roi_height = self.region_dimensions[1]
		# elif self.roi_name is not None and self.region_dimensions is not None:
		else:
			roi_width = self.region_dimensions[0]
			roi_height = self.region_dimensions[1]

		i = np.ones((roi_width, roi_height), dtype="float")
		self.i = i
		origin_x = self.origin_coords[0]
		origin_y = self.origin_coords[1]
		self.update_roi_square(origin_x, origin_y)
		# self.i[origin_x, origin_y] = 0.
		# self.i = i
		return i


	def update_roi_square(self, x, y):
		self.i[x,y] = 0.
		# self.x_path_points.append(local_y)
		# self.y_path_points.append(x)


	def update_path_pnt_coords(self, x, y):
		self.x_path_points.append(y)
		self.y_path_points.append(x)

	def viz_static_roi(self):
		# plt.gca().invert_yaxis()
		# print("x: {0}".format(self.i))
		plt.imshow(self.i, cmap="gray")
		plt.tick_params(which='minor', length=2, color='r')
		# plt.grid(True)
		plt.grid(b=True, which='both')
		plt.xlabel("Columns")
		plt.ylabel("Rowss")
		plt.gca().invert_yaxis()
		plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.8)

		# Show the minor grid lines with very faint and almost transparent grey lines
		# plt.minorticks_on()
		plt.xticks(np.arange(-0.5, 64, 0.25))
		# plt.xticks(np.arange(64+1)-0.5)
		plt.yticks(np.arange(-0.5, 64, 0.25))
		# plt.yticks(np.arange(64+1)-0.5)
		# plt.xticks(np.arange(256+1)-0.5, minor=True)
		# plt.yticks(np.arange(256+1)-0.5, minor=True)
		plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
		plt.plot(self.x_path_points, self.y_path_points, "r")
		# plt.tick_params(which='minor', length=4, color='r')
		plt.show()


if __name__ == "__main__":
	from src.ui_automation_tools import screen_tools
	import settings


	def test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
	                                 window_name=settings.GAME_WNDW_NAME):

		return screen_tools.set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
		                                            wndw_name=settings.GAME_WNDW_NAME)


	# true_lmd_castle_door_to_gs_door_path_coords
	# Xis = [3216, 3225, 3234, 3235, 3229, 3223, 3219, 3214]
	# Yis = [3219, 3219, 3219, 3226, 3233, 3239, 3244, 3245]

	# true_lmd_castle_door_to_al_kharid_gate
	# Xis = [3216, 3224, 3230, 3234, 3235, 3240, 3245, 3252, 3257, 3262, 3267]
	# Xis = [3216, 3224, 3230, 3234, 3235, 3240, 3245, 3252, 3257, 3262]
	# Yis = [3219, 3219, 3218, 3219, 3223, 3225, 3226, 3225, 3228, 3228, 3227]
	# Yis = [3219, 3219, 3218, 3219, 3223, 3225, 3226, 3225, 3228, 3228]
	Xis = [3215, 3215, 3216, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3226, 3227, 3228, 3229, 3230, 3231,
	     3232, 3233, 3234, 3235, 3235, 3234, 3234, 3233, 3232, 3231, 3231, 3231, 3231, 3230, 3229, 3228, 3227, 3227,
	     3227, 3227, 3227, 3227, 3226, 3226, 3225, 3224, 3223, 3222, 3221, 3220, 3220, 3220, 3219, 3219, 3218, 3217,
	     3216, 3215, 3214, 3213, 3212, 3211, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218, 3219, 3220, 3221, 3222,
	     3223, 3224, 3225, 3225, 3225, 3225, 3224, 3223, 3222, 3221, 3220, 3219, 3218, 3217, 3216, 3215, 3214, 3213,
	     3212, 3211, 3210, 3209, 3208, 3207, 3206, 3205, 3204, 3203, 3203, 3203, 3203, 3203, 3203, 3204, 3205, 3206,
	     3207, 3208, 3209, 3210, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224,
	     3225, 3226, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3233, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3241,
	     3242, 3243, 3244, 3245, 3246, 3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3254, 3254, 3255, 3256, 3257,
	     3258, 3259, 3260, 3261, 3261, 3260, 3260, 3259, 3259, 3259, 3259, 3259, 3259, 3259, 3259, 3259, 3259, 3259,
	     3259, 3259, 3258, 3257, 3256, 3255, 3254, 3253, 3252, 3252, 3252, 3252, 3252, 3252, 3252, 3252, 3252, 3252,
	     3251, 3250, 3250, 3249, 3248, 3247, 3246, 3245, 3244, 3243, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235,
	     3234, 3233, 3232, 3231, 3230, 3229, 3228, 3227, 3226, 3225, 3224, 3223, 3222, 3221, 3220, 3219, 3218, 3217,
	     3216, 3216, 3217, 3217, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3219,
	     3219, 3220, 3220, 3221, 3222, 3223, 3224, 3225, 3225, 3225, 3226, 3227, 3228, 3229, 3230, 3231, 3231, 3231,
	     3232, 3233, 3234, 3235, 3235, 3236, 3237, 3238, 3239, 3240, 3241, 3242, 3243, 3243, 3243, 3243, 3243, 3243,
	     3243, 3243, 3243, 3243, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235, 3234, 3233, 3233, 3233, 3233, 3232,
	     3231, 3230, 3229, 3228, 3227, 3226, 3225, 3224, 3223, 3222, 3221, 3220, 3219, 3218, 3217, 3216, 3215, 3215,
	     3215, 3215, 3215, 3215, 3215, 3215, 3214, 3213, 3212, 3211, 3210, 3209, 3208, 3207, 3206, 3205, 3205, 3206,
	     3207, 3208, 3209, 3210, 3211, 3212, 3213, 3214, 3215, 3215, 3215, 3215, 3215, 3215, 3215, 3215, 3216, 3217,
	     3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3226, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3234, 3235,
	     3236, 3237, 3238, 3239, 3239, 3240, 3241, 3242, 3243, 3244, 3245, 3246, 3247, 3248, 3249, 3250, 3251, 3252,
	     3253, 3254, 3255, 3256, 3257, 3258, 3258, 3258, 3257, 3256, 3255, 3254, 3253, 3252, 3251, 3250, 3250, 3249,
	     3248, 3247, 3246, 3245, 3244, 3244, 3243, 3243, 3243, 3242, 3242, 3242, 3242, 3242, 3242, 3242, 3242, 3242,
	     3241, 3241, 3240, 3240, 3239, 3239, 3239, 3239, 3239, 3239, 3240, 3241, 3242, 3243, 3244, 3244, 3244, 3244,
	     3244, 3243, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235, 3234, 3233, 3232, 3231, 3230, 3229, 3229, 3230,
	     3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3230, 3229, 3228, 3228, 3228, 3228, 3228,
	     3228, 3229, 3230, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3231, 3230, 3229, 3229, 3230,
	     3231, 3232, 3233, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3241, 3242, 3243, 3244, 3244, 3244, 3245, 3246,
	     3247, 3248, 3248, 3248, 3249, 3250, 3250, 3250, 3251, 3252, 3253, 3254, 3255, 3255, 3256, 3256, 3255, 3254,
	     3253, 3252, 3251, 3250, 3249, 3248, 3248, 3248, 3248, 3248, 3248, 3247, 3247, 3247, 3247, 3246, 3246, 3245,
	     3244, 3243, 3243, 3243, 3242, 3242, 3242, 3242, 3242, 3242, 3242, 3242, 3242, 3243, 3244, 3244, 3244, 3244,
	     3244, 3244, 3244, 3244, 3244, 3244, 3244, 3243, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235, 3234, 3233,
	     3232, 3231, 3230, 3229, 3228, 3227, 3226, 3225, 3224, 3223, 3222, 3221, 3220, 3219, 3218, 3217, 3216, 3215,
	     3214, 3214, 3213, 3212, 3211, 3210, 3209, 3208, 3207, 3206, 3205, 3204, 3203, 3202, 3201, 3201, 3201, 3201,
	     3201, 3201, 3202, 3202, 3202, 3202, 3203, 3203, 3203, 3203, 3203]
	Yis = [3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218,
	     3218, 3218, 3218, 3218, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3226, 3227, 3228, 3229, 3229, 3230,
	     3231, 3232, 3233, 3234, 3234, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3241, 3241, 3242, 3243, 3244, 3244,
	     3244, 3245, 3245, 3245, 3246, 3247, 3247, 3246, 3245, 3245, 3245, 3246, 3247, 3248, 3249, 3249, 3249, 3249,
	     3249, 3250, 3251, 3252, 3252, 3251, 3250, 3249, 3248, 3247, 3246, 3245, 3244, 3244, 3243, 3242, 3241, 3241,
	     3241, 3241, 3241, 3241, 3241, 3242, 3242, 3242, 3242, 3242, 3241, 3240, 3240, 3239, 3238, 3238, 3238, 3238,
	     3238, 3238, 3238, 3238, 3238, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3237, 3236,
	     3236, 3236, 3235, 3234, 3233, 3232, 3231, 3230, 3229, 3228, 3227, 3227, 3226, 3225, 3225, 3225, 3225, 3225,
	     3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3225, 3226, 3226, 3227, 3227,
	     3228, 3228, 3228, 3228, 3228, 3229, 3230, 3231, 3232, 3233, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3241,
	     3242, 3243, 3244, 3245, 3246, 3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3257, 3258, 3259,
	     3260, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261,
	     3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3262, 3262, 3262, 3262, 3262, 3261,
	     3261, 3261, 3260, 3259, 3258, 3257, 3256, 3255, 3254, 3253, 3252, 3251, 3250, 3249, 3248, 3247, 3247, 3246,
	     3245, 3244, 3243, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235, 3234, 3233, 3232, 3232, 3231, 3230, 3229,
	     3228, 3227, 3226, 3225, 3224, 3223, 3222, 3221, 3220, 3219, 3218, 3217, 3216, 3215, 3214, 3213, 3212, 3211,
	     3210, 3209, 3209, 3210, 3210, 3210, 3210, 3210, 3210, 3210, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218,
	     3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3217,
	     3216, 3215, 3214, 3213, 3212, 3211, 3211, 3211, 3211, 3211, 3210, 3209, 3209, 3209, 3209, 3209, 3209, 3209,
	     3210, 3210, 3211, 3211, 3211, 3211, 3211, 3211, 3211, 3212, 3213, 3214, 3215, 3216, 3217, 3218, 3218, 3218,
	     3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3218, 3219, 3220, 3221,
	     3222, 3223, 3223, 3224, 3225, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226, 3226,
	     3226, 3226, 3226, 3227, 3227, 3228, 3229, 3230, 3230, 3230, 3231, 3231, 3231, 3231, 3231, 3231, 3232, 3233,
	     3233, 3233, 3234, 3235, 3236, 3237, 3238, 3239, 3240, 3240, 3240, 3241, 3242, 3243, 3244, 3245, 3246, 3247,
	     3248, 3249, 3250, 3251, 3251, 3251, 3252, 3253, 3254, 3255, 3256, 3256, 3256, 3256, 3257, 3258, 3259, 3260,
	     3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3260, 3260,
	     3259, 3258, 3257, 3256, 3255, 3254, 3253, 3252, 3251, 3250, 3249, 3248, 3247, 3246, 3245, 3244, 3244, 3245,
	     3246, 3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3257, 3258, 3259, 3260, 3260, 3261, 3261,
	     3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3260, 3259, 3258, 3258,
	     3258, 3258, 3257, 3256, 3255, 3254, 3253, 3252, 3251, 3250, 3249, 3248, 3247, 3246, 3245, 3245, 3244, 3244,
	     3243, 3243, 3243, 3242, 3242, 3241, 3240, 3239, 3238, 3237, 3236, 3235, 3234, 3233, 3233, 3234, 3235, 3236,
	     3237, 3238, 3239, 3240, 3241, 3242, 3243, 3244, 3245, 3246, 3247, 3248, 3249, 3250, 3251, 3252, 3253, 3254,
	     3255, 3256, 3257, 3258, 3259, 3260, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261,
	     3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3261, 3262, 3262, 3262, 3262, 3261, 3260, 3259,
	     3258, 3257, 3256, 3256, 3255, 3255, 3255, 3255, 3255, 3255, 3255, 3255, 3255, 3254, 3253, 3253, 3252, 3251,
	     3250, 3249, 3248, 3247, 3246, 3245, 3245, 3244, 3243, 3242, 3241]


	def world_path_coords_generator(Xis, Yis, wm_square_info_dict=None):
		# wm_coords = []
		for xi, yi in zip(Xis, Yis):
			wm_square_info_dict = wm_square_info_dict
			if wm_square_info_dict is None:
				yield (xi, yi)
				# wm_coords.append((xi, yi))
			else:
				info = wm_square_info_dict[(xi, yi)]
				yield (xi, yi, info)
				# wm_coords.append((xi, yi, info))
		# wm_coords.append([xi, yi])
		# return wm_coords


	def get_world_path_coords(Xis, Yis):
		world_coords_list = []
		coords_gen = world_path_coords_generator(Xis, Yis, wm_square_info_dict=None)
		for coords in coords_gen:
			world_coords_list.append(coords)
		return world_coords_list


	def get_grid_path_coords(Xis, Yis, grid_x_origin=3200, grid_y_origin=3200):
		grid_coords_list = []
		coords_gen = world_path_coords_generator(Xis, Yis, wm_square_info_dict=None)
		for coords in coords_gen:
			x_coord = coords[0] - grid_x_origin
			y_coord = coords[1] - grid_y_origin
			grid_coords_list.append((x_coord, y_coord))
		return grid_coords_list


	grid_path_coords = get_grid_path_coords(Xis, Yis)

	test_set_window_pos_and_size()

	rad = 12
	# s = 64
	s = 64
	static_roi_sensor = StaticROISensor(origin_coords=(0, 0))
	static_roi_sensor.create_static_roi_array()
	# static_roi_sensor.viz_static_roi()

	for grid_path_coord in grid_path_coords[1:]:
		print(grid_path_coord[1], grid_path_coord[0])
		static_roi_sensor.update_roi_square(grid_path_coord[1], grid_path_coord[0])
		static_roi_sensor.update_path_pnt_coords(grid_path_coord[1], grid_path_coord[0])

	static_roi_sensor.viz_static_roi()


	# mm = MiniMapGrid(mm_rad_sq_len=mm_rad_sq_len)
	# mm.create_mm_grid_cells_coords()
	# x = mm.reshape_cells_coords_list_to_array(mm.cells_coords_list, (25, 25, 2))
	# # i = np.ones((25, 25, 1), dtype="float")
	# i = np.ones((s, s), dtype="float")
	# float_img = np.random.random((4, 4))
	# im = np.array(float_img * 255, dtype=np.uint8)
	# # threshed = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)
	# i[12,12] = 0.
	# i[16,19] = 0.
	# # i[,s-19] = 0.
	# a = i
	# plt.gca().invert_yaxis()
	# print("x: {0}".format(a))
	# plt.imshow(a, cmap="gray")
	# plt.gca().invert_yaxis()
	# plt.show()


