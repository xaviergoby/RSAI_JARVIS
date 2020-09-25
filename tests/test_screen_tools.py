from src.ui_automation_tools import screen_tools
import settings


if __name__ == "__main__":

	# hwnd = win32gui.FindWindow(None, 'Old School RuneScape')
	# import win32gui
	wndw_name = settings.GAME_WNDW_NAME
	wndw_x_wrt_screen = 0  # -8
	wndw_y_wrt_screen = 0  # -31
	wndw_width_in_screen = 800
	wndw_height_in_screen = 600
	screen_tools.set_window_pos_and_size(hwnd=None, x_new=wndw_x_wrt_screen, y_new=wndw_y_wrt_screen,
	                                     new_width=wndw_width_in_screen, new_height=wndw_height_in_screen, wndw_name=wndw_name)



	# for OSRS: (8, 31, 791, 591) (as seen in the dict in settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT)
	client_bbox_reg_px_coords = screen_tools.get_client_specific_bounding_region_px_coords()
	print(f"client_bbox_reg_px_coords: {client_bbox_reg_px_coords}")

	# (leftmost included x px coord, topmost included y px coord, rightmost included x px coord, bottommost included y px coord)
	# 	Every pixel coordinate point beyond this region is not clickable within the game and everything with, incl. the 4 coord returns, are clickable
	# 	within the game.
	client_main_view_roi_coords = screen_tools.get_client_tl_pos_and_area_dims()
	print(f"client_main_view_roi_coords: {client_main_view_roi_coords}")

	client_area_pos_and_size = screen_tools.get_client_area_pos_and_dims()
	print(f"client_main_view_roi_coords: {client_area_pos_and_size}")



	# # win32gui.MoveWindow(hwnd, 0, 0, 800, 600, True)
	# # Changes the position and dimensions of the specified window. For a top-level window,
	# # the position and dimensions are relative to the upper-left corner of the screen.
	# # For a child window, they are relative to the upper-left corner of the parent window's client area.
	# # win32gui.MoveWindow(hwnd, -7, 0, 800, 600, True)
	# # win32gui.MoveWindow(hwnd, 0, 0, 800, 600, True)
	# coords1 = screen_tools.get_client_screen_tl_br_coords(wndw_name)  # returns: (0, 0, 784, 561)
	# coords2 = screen_tools.get_client_screen_tl_coord_and_size(wndw_name)  # returns: (8, 31, 784, 561)
	# # coords3 = grab_screen_v3()
	# print("OSRS Client screen top-left & bottom-right coords('Old School RuneScape')coords: {0}".format(coords1))
	# print("OSRS Client screen top-left coords & dims('Old School RuneScape')coords: {0}".format(coords2))
	# # Coordinates of the centre of the client screen of the open window w/ the origin located
	# # top left most corner of the CLIENT SCREEN of the open window
	# client_centre_width_center = round(coords2[2] / 2) + coords2[0]
	# # client_centre_height_center = round((coords2[3]+coords2[1]+8)/2)
	# client_centre_height_center = round((coords2[3] - coords2[1] + 8) / 2)
	# print("client_centre_width_center : {0}".format(client_centre_width_center))
	# print("client_centre_height_center : {0}".format(client_centre_height_center))
	# # x_c = coords2[2] - coords2[0]
	# # y_c = coords[3] - coords2[1]
	# # print("grab_screen_v3()coords: {0}".format(coords3))
	# print(screen_tools.get_client_specific_bounding_region_px_coords()) # returns (8, 31, 791, 591)
	# # print(get_client_specific_bounding_region_px_coords(wndw_name="RuneLite - PolarHobbes"))
	# # print("get_client_screen_tl_br_coords('Old School RuneScape')coords: {0}".format(coords1))
	# # print(coords2)
	# # print(coords3)
	# # r 528
	# # l 432
	# #
	# # b 377
	# # t 258
	# # client_centre_width_center: 480
	# # client_centre_height_center: 289
	# # hwnd = win32gui.FindWindow(None, 'Old School RuneScape')
	# # import win32gui
	#
	# # win32gui.MoveWindow(hwnd, 0, 0, 800, 600, True)
	# # x_c = ((800 - 8) / 2) = 396
	# # y_c = ((600 - 30 - 8) / 2) + 30 = 311
	# print(f"get_client_main_view_roi_pos_and_dims: {screen_tools.get_client_tl_pos_and_area_dims()}")