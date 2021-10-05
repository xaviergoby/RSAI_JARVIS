import subprocess
import pyautogui
import win32gui, win32ui, win32con, win32api
import time
import cv2
import numpy as np
from src.ui_automation_tools.mouse_events_monitoring import key_check
# from getkeys import key_check
import ctypes
import os
import win32gui
import settings

ctypes.windll.user32.SetProcessDPIAware()



def get_client_pos_and_size(wndw_name="Old School RuneScape") -> "the 4-tuple (x, y, w, h), i.e. (8, 31, 783, 560)":
	"""
	:param wndw_name: The name of the window (applciation) for which to get the pos & size of
	Is "Old School RuneScape" by def (recall that settings.GAME_WNDW_NAME="Old School RuneScape")
	:return: The 4-tuple , i.e. (8, 31, 783, 560) where:
	- x: x coord of the top left corner of the client (area)**AKA** the client's top left coord axes origin pnt x coord
    - y: Same as the above, but for the y coord.
    - w: The (pixel) width of the client (area)
    - h: The (pixel) height of the client (area)
	# x, y, client_screen_width, client_screen_height <=> (8, 31, 791, 591)
	# Therefore, fix this by manually subtracting an add. 8 (=x) pxs from w=791 to get h=783
	# and subtract an add. 31 (=y) pxs from h=591 to get h=560.
	So reutnrs (8, 31, 783, 560) when window is pos. @ (0, 0) wrt to the screen w/ a size of (800, 600)
	---------------------------------------------------------------------------------------
	ClientToScreen
		Windows GDI documentatation: "The ClientToScreen function converts the client-area coordinates
		of a specified point to screen coordinates."
	"""
	hwnd = win32gui.FindWindow(None, wndw_name)
	win32gui.SetForegroundWindow(hwnd)
	x, y, x1, y1 = win32gui.GetClientRect(hwnd)
	print(f"win32gui.GetClientRect(hwnd): {x, y, x1, y1}")
	x, y = win32gui.ClientToScreen(hwnd, (x, y))
	print(f"win32gui.ClientToScreen(hwnd, (x, y)): {x, y}")
	x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
	print(f"win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y)): {x1, y1}")
	client_screen_width, client_screen_height = x1, y1
	w_old = client_screen_width
	h_old = client_screen_height
	x, y, w, h = x, y, w_old-x, h_old-y
	return x, y, w, h

# FUNC # 2
def get_window_screen_tl_br_coords(win_name):
	# //TODO: 1)Necessity/Redundacy Study  2)V&V (does what it is meant to do & does how it should be done)
	"""win32gui.GetClientRect(hwnd) returns the client coordinates of the window. left and top will be zero.
	(left, top, right, bottom) = GetClientRect()
				~~~ Schematic ~~~

	(left, top) = (0, 0)

			 left top
		     0, 0 - - - - - - - - - - > + x-axis direction
			 |                        |
			 |                        |
			 |                        |
			 |                      1919 right
			 v - - - - - - - - - -  1079 bottom
			 + local_y-axis direc.
			                                    (right, bottom) = (1919, 1079)
	So@
	width = right - left = 1919
	height = bottom - top = 1079
	Top Left, tp, point coords: (l, t)  <=> (x, local_y)
	Bottom Right, br, point coords: (r, b)  <=> (x1, y1)
	:param win_name: name of window i.e. "RuneScape"
	:return: a 4-tuple of (left, top, right, bottom)
	e.g. returned coords for X: (-8, -8, 1928, 1048)

	Note: win32gui.GetWindowRect(hwnd) returns the following for the window handle, hwnd:
		(lpRect.left, lpRect.top, lpRect.right, lpRect.bottom)
	"""
	hwnd = win32gui.FindWindow(None, win_name)
	coords = win32gui.GetWindowRect(hwnd)     # note: coords used to be called bbox
	return coords

# win32gui.GetClientRect(hwnd) gets me the window size
# (left, top, right, bottom) = win32gui.GetClientRect(hwnd)
# Returns the rectangle of the client area of a window, in client coordinates

# FUNC # 3
def get_client_screen_tl_br_coords(win_name):
	"""
	Does the same thing as get_window_screen__tl_br_coords() BUT instead of coordinates of the
	windows, this function returns the coordinates for the client associated with win_name!
	This means that strictly on the client is used as the region, e.g. that usually white
	windows bar horizontally at the top with the esc, minimize and full screen buttons on the right top
	corner are not included in the region!

	NOTE KEY TAKEAWAY: The point of origin of the cartesian coordinate system this function relies on
	is such that it is located at the VERY/MOST TOP LEFT CORNER of the window , return e.g.: (0, 0, 731, 516).
	This means that the left most and top most coordinate points returned are ALWAYS 0!

	From the doc for win32gui.GetClientRect:
	(left, top, right, bottom) = GetClientRect(hwnd)
	Returns the rectangle of the client area of a window, in client coordinates
	:param win_name: str of the name of the window e.g. "RuneScape"
	:return: (left, top, right, bottom)
	e.g. (0, 0, 731, 516)
	"""
	hwnd = win32gui.FindWindow(None, win_name)
	win32gui.SetForegroundWindow(hwnd)
	x, y, x1, y1 = win32gui.GetClientRect(hwnd)
	# x, local_y = win32gui.ClientToScreen(hwnd, (x, local_y))
	# x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - local_y))
	return x, y, x1, y1

# FUNC # 4
def get_client_screen_tl_coord_and_size(win_name=settings.GAME_WNDW_NAME):
	"""
	Note that: w = width = x1 - x = r - l = right coord - left coord
	similarly h = height = y1 - local_y = b - t = bottom coord - top coord

	NOTE KEY TAKEAWAY: The left most and top most coordniate points are meaused w.r.t MY ACTULAL
	DEKSTOP, starting from the edge/border/rim of my desktop screen and then:
	    i) rightwards until the left side edge of the client screen of my window for the left most coord pnt.
	    ii) downwards until the top side edge of the client screen of my window for the top most coord pnt.

	NOTE KEY TAKEAWAY: The value of the width and height returned by this function are the width and height
	of SOLELY the client screen of the window - in other words, the width and height are measured w.r.t the
	TOP LEFT CORNER OF THE CLIENT SCREEN AS THE POINT OF ORIGIN (below the top left corner origin point used
	by the open window).

	NOTE KEY TAKEAWAY: The upper white horizontal bar across the top
	of a window (in which the minimize, fullscreen and close window options
	can be found) has a height/thickness of 30 pxs.

	NOTE KEY TAKEAWAY: Positioning a fullscreened open window in the top left corner/section
	via the keyboard shortcuts:
	Windows Button + Down Arrow Button | Windows Button + Left Arrow Button | Windows Button + Up Arrow Button
	Will result in the top most & left most coord pnts. having values of 1 and 31 respectively (recall the
	thickness of the top white horizontal window bar mentioned AND note that the left most edge of a client
	screen in an open window located at the top left corner of my desktop will start/be located a distance of
	1 pixel away from the very edge/rim of my desktop)
	:param win_name: str of the name of the window e.g. "RuneScape"
	:return: 4-tuple w/ (left, top, width, height)
	in other words: (wnd_screen_furthers_most_left_point, wnd_screen_upper_most_point,
					 wnd_client_screen_width, wnd_client_screen_height)
	e.g. return for X: (0, 43, 1920, 997) or (-2, 36, 853, 599)
	"""
	hwnd = win32gui.FindWindow(None, win_name)
	win32gui.SetForegroundWindow(hwnd)
	x, y, x1, y1 = win32gui.GetClientRect(hwnd)
	# print(f"win32gui.GetClientRect(hwnd)x: {x}")
	# print(f"win32gui.GetClientRect(hwnd)x1: {x1}")
	# print(f"win32gui.GetClientRect(hwnd)y: {y}")
	# print(f"win32gui.GetClientRect(hwnd)y1: {y1}")
	x, y = win32gui.ClientToScreen(hwnd, (x, y))
	# print(f"post win32gui.ClientToScreen(hwnd, (x, y))x: {x}")
	# print(f"post win32gui.ClientToScreen(hwnd, (x, y))y: {y}")
	x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
	# return x, y, x1, y1
	# print(f"x1: {x1}")
	# print(f"y1: {y1}")
	client_screen_width, client_screen_height = x1, y1
	return x, y, client_screen_width, client_screen_height

# FUNC # 5
def set_window_pos_and_size(hwnd = None, x_new = 0, y_new = 0, new_width = 800, new_height = 600, wndw_name = settings.GAME_WNDW_NAME):
	"""
	NOTE (from: Microsoft Doc on MoveWindow function):
	" Changes the position and dimensions of the specified window. For a top-level window,
	the position and dimensions are relative to the upper-left corner of the screen.
	For a child window, they are relative to the upper-left corner of the parent window's client area."

	NOTE (regarding window alignment with true left & true top):
	" Windows 10 has an invisible border of 7 pixels. (Totaling to 8 pixels if you include the visible 1 pixel window border.)
	It is the border for resizing windows which is on the left, right and bottom edge of the window. "
	Notice how the resizing cursor reacts with the top edge. There is no invisible border there. An easy fix is to just offset the x in MoveWindow as seen below:
	win32gui.MoveWindow(hwnd, -7, 0, new_width, new_height, True)

	This therefore means that if I instruct this function to set the pos (of the top-left point) of the game client to be
	(located) at (x_new=0, y_new=0) and instruct the dimensions/size of this game client to be (new_width=800, new_height=600), this wil
	essentially mean that my game client will end up occupying all the:
		i) Horizontal pixels of my screen between & including x=0 & x=799 (since, just
		as when working with, e.g. numpy array indexing, I start at 0 instead of 1 & that is why 800 is exclueded!).
		ii) Vertical pixels of my screen between & including y=0 & x=599 (since, just
		as when working with, e.g. numpy array indexing, I start at 0 instead of 1 & that is why 600 is exclueded!).

	:param hwnd: A handle to the window. Is None by def.
	:param x_new: The new position of the left side of the window. Is 0 by def.
	:param y_new: The new position of the top of the window. Is 0 by def.
	:param new_width: The new width of the window. Is 800 by def.
	:param new_height: The new height of the window. Is 600 by def.
	:param wndw_name: str of the name of the window. Is "Old School RuneScape" by def.
	:return: None
	"""
	if hwnd is None and wndw_name is not None:
		hwnd = win32gui.FindWindow(None, wndw_name)
		win32gui.MoveWindow(hwnd, x_new, y_new, new_width, new_height, True)
	elif hwnd is not None and wndw_name is not None:
		win32gui.MoveWindow(hwnd, x_new, y_new, new_width, new_height, True)

# FUNC # 6
def adjust_wndw_pos_and_dims(hwnd=None, x_new=0, y_new=0,
                             new_width=800, new_height=600, window_name=settings.GAME_WNDW_NAME):
	"""
	NOTE/WARNING: REDUNDANT
	Kind of a redundant version of the above method set_window_pos_and_size(hwnd = None, x_new = 0, y_new = 0, new_width = 800,
																			new_height = 600, window_name = settings.GAME_WNDW_NAME)
	Takes the exact same arguments for the parameters as set_window_pos_and_size(...) and returns the exact same thing as well!
	"""
	return set_window_pos_and_size(hwnd=None, x_new=0, y_new=0,
	                               new_width=800, new_height=600, wndw_name=settings.GAME_WNDW_NAME)

# FUNC # 7
def get_client_specific_bounding_region_px_coords(wndw_name=None) -> 'i.e. (8, 31, 791, 591) when wndw_name="Old School RuneScape"':
	"""
	:param wndw_name: the name of the window handle. If the default arg, None, is left/unchanged
	then the name of the window handle which will be used is: wndw_name = settings.GAME_WNDW_NAME = "Old School RuneScape".
	This then means bounding_px_coords = settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT["Old School RuneScape"]
	where settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT["Old School RuneScape"] = {"left": 8, "top": 31 ,"right": 791, "bottom": 591}
	:return: a 4-tuple
	when wndw_name=None => (8, 31, 791, 591) (as seen in settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT), where:
	GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT = {"Old School RuneScape": {"left": 8, "top": 31 ,"right": 791, "bottom": 591},
                                              "RuneLite - PolarHobbes": {"left": 4, "top": 27 ,"right": 795, "bottom": 595}}
	"""
	if wndw_name is None:
		wndw_name = settings.GAME_WNDW_NAME
	bounding_px_coords = settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT[wndw_name]
	left = bounding_px_coords["left"]
	top = bounding_px_coords["top"]
	right = bounding_px_coords["right"]
	bottom = bounding_px_coords["bottom"]
	return left, top, right, bottom

# FUNC # 8
def get_client_tl_pos_and_area_dims(wndw_name=None):
	"""
	USE this function determines the correct coordinates of the region of interest of the main view of the client

	:param wndw_name: the name of the window handle. If the default arg, None, is left/unchanged
	then the name of the window handle which will be used is: wndw_name = settings.GAME_WNDW_NAME = "Old School RuneScape".
	This then means bounding_px_coords = settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT["Old School RuneScape"]
	where settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT["Old School RuneScape"] = {"left": 8, "top": 31 ,"right": 791, "bottom": 591}
	:return: a 4-tuple
	when wndw_name=None => (8, 31, 791, 591) (as seen in settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT)
	(leftmost included x px coord, topmost included y px coord, rightmost included x px coord, bottommost included y px coord)
	Every pixel coordinate point beyond this region is not clickable within the game and everything with, incl. the 4 coord returns, are clickable
	within the game.
	(8, 31, 791, 591) (as seen in the dict in settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT)
	"""
	if wndw_name is None:
		wndw_name = settings.GAME_WNDW_NAME
	unadjusted_client_main_view_roi_pos_and_dims = get_client_screen_tl_coord_and_size(wndw_name)
	pos_x, pos_y = unadjusted_client_main_view_roi_pos_and_dims[0], unadjusted_client_main_view_roi_pos_and_dims[1]
	# left_x, top_y = unadjusted_client_main_view_roi_pos_and_dims[0], unadjusted_client_main_view_roi_pos_and_dims[1]
	width = unadjusted_client_main_view_roi_pos_and_dims[2] + pos_x - 1
	# right_x = unadjusted_client_main_view_roi_pos_and_dims[2] + left_x - 1
	height = unadjusted_client_main_view_roi_pos_and_dims[3] + pos_y - 1
	# bottom_y = unadjusted_client_main_view_roi_pos_and_dims[3] + top_y - 1
	client_area_width = unadjusted_client_main_view_roi_pos_and_dims[2] - 1
	client_area_height = unadjusted_client_main_view_roi_pos_and_dims[3] - 1
	# print(f"pos_x: {pos_x}")
	# print(f"pos_y: {pos_y}")
	# print(f"client_screen_width: {unadjusted_client_main_view_roi_pos_and_dims[2]}")
	# print(f"width: {width}")
	# print(f"client_screen_height[3]: {unadjusted_client_main_view_roi_pos_and_dims[3]}")
	# print(f"height: {height}")
	return pos_x, pos_y, client_area_width, client_area_height
	# return pos_x, pos_y, unadjusted_client_main_view_roi_pos_and_dims[2], unadjusted_client_main_view_roi_pos_and_dims[3]
	# return pos_x, pos_y, width, height
	# return left_x, top_y, right_x, bottom_y


# def get_game_bbox_region():
# 	main_game_view_roi_bbox_co


# FUNC # 9
def get_client_area_pos_and_dims(wndw_name=None) -> "(left most x, top most y, width, height)":
	"""
	:param wndw_name:
	:return: 4-tuple (lx, ty, w, h)
	where: lx & ty are the left and top most x & y coords respectively.
	(left most x, top most y, width, height)
	"""
	if wndw_name is None:
		wndw_name = settings.GAME_WNDW_NAME
	x1, y1, x2, y2 = get_client_tl_pos_and_area_dims(wndw_name)
	leftmost_x = x1
	topmost_y = y1
	width = x2 - x1
	height = y2 - y1
	return leftmost_x, topmost_y, width, height

# FUNC # 10
def get_client_tlxy_brxy_wrt_screen(wndw_name=settings.GAME_WNDW_NAME):
	# if wndw_name is None:
	# 	wndw_name = settings.GAME_WNDW_NAME
	unadjusted_client_main_view_roi_pos_and_dims = get_client_screen_tl_coord_and_size(wndw_name) # i.e. (8, 31, 784, 561)
	client_area_tl_pos_x, client_area_tl_pos_y = unadjusted_client_main_view_roi_pos_and_dims[0], unadjusted_client_main_view_roi_pos_and_dims[1]
	client_area_width = unadjusted_client_main_view_roi_pos_and_dims[2] + client_area_tl_pos_x - 1
	client_area_height = unadjusted_client_main_view_roi_pos_and_dims[3] + client_area_tl_pos_y - 1
	return client_area_tl_pos_x, client_area_tl_pos_y, client_area_width, client_area_height



if __name__ == "__main__":
	print("1st Step")
	import win32gui
	wndw_name = "Old School RuneScape"
	hwnd = win32gui.FindWindow(None, wndw_name)
	print(f"{wndw_name} Window Handle (Window Found?={hwnd!=0}): hwnd={hwnd}")
	print("\n2nd Step")
	import time
	print("Sleeping for 3 seconds...")
	time.sleep(3)
	print(f"Please CLICK NOW on your {wndw_name} window and wait")
	win32gui.SetForegroundWindow(hwnd)
	print("\n3rd Step")
	x = 0
	y = 0
	width = 800
	height = 600
	bRepaint = True
	win32gui.MoveWindow(hwnd, x, y, width, height, bRepaint)
	print("\n4th Step")
	x, y, x1, y1 = win32gui.GetClientRect(hwnd)
	print(x, y, x1, y1)  # (0, 0, 784, 561)
	print("\n5th Step")
	x, y = win32gui.ClientToScreen(hwnd, (x, y))
	print(x, y)  # (8, 31)
	print("\n6th Step")
	x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
	print(x1, y1)  # (784, 561)
	print("\n7th Step")
	wndw_rect = win32gui.GetWindowRect(hwnd)
	print(wndw_rect)  # (0, 0, 800, 600)
	print("\n7th Step")
	client_coord = win32gui.ScreenToClient(hwnd, (wndw_rect[0], wndw_rect[1]))
	print(client_coord) # (0, 0, 784, 561)

	print("\nClient To Screen Coordinates Transformation Demo")
	print("Starding demo in 3 seconds...")
	time.sleep(3)
	wx1, wy1, ww1, wh1 = 0, 0, 800, 600
	print(wx1, wy1, ww1, wh1)
	print(f"Moving Window to Pos{(wx1, wy1)} with size {(ww1, wh1)}")
	win32gui.MoveWindow(hwnd, wx1, wy1, ww1, wh1, True)
	wx2, wy2, ww2, wh2 = win32gui.GetWindowRect(hwnd)
	print(wx2, wy2, ww2, wh2)
	cx, cy, cx1, cy1 = win32gui.GetClientRect(hwnd)
	print(f"Client Rect: {cx, cy, cx1, cy1}")
	sx, sy = win32gui.ClientToScreen(hwnd, (cx, cy))
	sx1, sy1 = win32gui.ClientToScreen(hwnd, (cx1 - sx, cy1 - sy))
	print(f"Screen Rect from Client Rect: {sx, sy, sx1, sy1}")
	print(f"Current Window Rect: {win32gui.GetWindowRect(hwnd)}")
	print(f"Current Client Rect: {win32gui.GetClientRect(hwnd)}")
	print(f"Current Screen Rect to Client: {win32gui.ScreenToClient(hwnd, (win32gui.GetWindowRect(hwnd)[0], win32gui.GetWindowRect(hwnd)[1]))}")
	# new_wndw_rect = (sx, sy, sx1, sy1)
	# print(new_wndw_rect)






	# # hwnd = win32gui.FindWindow(None, 'Old School RuneScape')
	# # import win32gui
	# wndw_name = settings.GAME_WNDW_NAME
	# # 765x503
	# wndw_x_wrt_screen = 0  # -8
	# wndw_y_wrt_screen = 0  # -31
	# wndw_width_in_screen = 800
	# # wndw_width_in_screen = 765+8
	# wndw_height_in_screen = 600
	# # wndw_height_in_screen = 503+30
	# set_window_pos_and_size(hwnd = None, x_new = wndw_x_wrt_screen, y_new = wndw_y_wrt_screen,
	#                         new_width = wndw_width_in_screen, new_height = wndw_height_in_screen, wndw_name= wndw_name)
	#
	# # win32gui.MoveWindow(hwnd, 0, 0, 800, 600, True)
	# # Changes the position and dimensions of the specified window. For a top-level window,
	# # the position and dimensions are relative to the upper-left corner of the screen.
	# # For a child window, they are relative to the upper-left corner of the parent window's client area.
	# # win32gui.MoveWindow(hwnd, -7, 0, 800, 600, True)
	# # win32gui.MoveWindow(hwnd, 0, 0, 800, 600, True)
	# coords1 = get_client_screen_tl_br_coords(wndw_name) # returns: (0, 0, 784, 561)
	# coords2 = get_client_screen_tl_coord_and_size(wndw_name) # returns: (8, 31, 784, 561)
	# # coords3 = grab_screen_v3()
	# print("OSRS Client screen top-left & bottom-right coords('Old School RuneScape')coords: {0}".format(coords1))
	# print("OSRS Client screen top-left coords & dims('Old School RuneScape')coords: {0}".format(coords2))
	# # Coordinates of the centre of the client screen of the open window w/ the origin located
	# # top left most corner of the CLIENT SCREEN of the open window
	# client_centre_width_center = round(coords2[2]/2) + coords2[0]
	# # client_centre_height_center = round((coords2[3]+coords2[1]+8)/2)
	# client_centre_height_center = round((coords2[3]-coords2[1]+8)/2)
	# print("Client area width, client_centre_width_center : {0}".format(client_centre_width_center))
	# print("Client area height client_centre_height_center : {0}".format(client_centre_height_center))
	# # x_c = coords2[2] - coords2[0]
	# # y_c = coords[3] - coords2[1]
	# # print("grab_screen_v3()coords: {0}".format(coords3))
	# print(f"get_client_specific_bounding_region_px_coords(): {get_client_specific_bounding_region_px_coords()}") # returns --> (8, 31, 791, 591)
	#
	#
	# # get_client_specific_bounding_region_px_coords() returns --> (8, 31, 791, 591)
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
	# print(f"get_client_tl_pos_and_area_dims: {get_client_tl_pos_and_area_dims()}")
	#
	# # import win32gui
	# game_client_wndw_name = "Old School RuneScape"
	# game_client_wndw_handle = win32gui.FindWindow(None, game_client_wndw_name)
	# win_32_gui_get_wndw_rect = win32gui.GetWindowRect(game_client_wndw_handle)
	# print(f"Result of win32gui.GetWindowRect(game_client_wndw_name): {win_32_gui_get_wndw_rect}")
