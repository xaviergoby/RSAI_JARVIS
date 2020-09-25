import win32gui
import os
import numpy
import PIL
import cv2
import json
import pyautogui
from settings import DATA_DIR, mouse_nVirtKey_dict
from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import screen_tools
from pyclick import HumanClicker


class RSAgent:

	bot_client_size_wrt_screen = 784, 561 # width, height
	bot_client_center_pos_wrt_screen = 392, 281 # local_x, local_y

	def __init__(self, bot_client_size_wrt_screen = (784, 561), bot_client_center_pos_wrt_screen = (392, 281)):
		self.bot_client_size_wrt_screen = bot_client_size_wrt_screen
		self.bot_client_center_pos_wrt_screen = bot_client_center_pos_wrt_screen
		self.current_global_custom_loc_coords = (0, 0)
		# 702, 84
	# r = 84 - 8 = 76
# (l, t, w, h) = 626,


if __name__ == "__main__":
	import settings
	# win_name = "Old School RuneScape"
	win_name = settings.GAME_WNDW_NAME
	wndw_x_wrt_screen = 0  # -8
	wndw_y_wrt_screen = 0  # -31
	wndw_width_in_screen = 800
	wndw_height_in_screen = 600
	screen_tools.set_window_pos_and_size(hwnd = None, x_new = wndw_x_wrt_screen, y_new = wndw_y_wrt_screen,
	                                     new_width = wndw_width_in_screen, new_height = wndw_height_in_screen,
	                                     wndw_name= win_name)

	hwnd = win32gui.FindWindow(None, win_name)
	wndw_rect_pos_n_size = win32gui.GetWindowRect(hwnd)
	#  client rect does not include title bar, borders, scroll bars, status bar...
	client_rect_pos_n_size = win32gui.GetClientRect(hwnd)
	# client area width wrt screen coords = [8, 791]
	# client area height wrt screen coords = [31, 591] or alt [31, 590]

	# window area width wrt screen coords = [0, 799]
	# pyautogui.moveTo(local_x = 0, local_y=300)
	# pyautogui.click()

	# tile screen coords width = [371, 418]
	# tile_id = 0 MM CENTRE TILE
	# mm single tile width in screen coords = [708, 711]
	# mm single tile height in screen coords = [114, 117]


	print("Window left local_x, top local_y, width and height in screen coords: {0}".format(wndw_rect_pos_n_size))
	print("Client left local_x, top local_y, width and height (excl. title bar, borders etc): {0}".format(client_rect_pos_n_size))

	# CALCULATIONS
	# pyautogui.moveTo(708, 117-(4*19)-3) IS FIRST PX OUTSIDE OF TOP OF MINIMAP
	# 117-(4*19)-3 = 38
	# pyautogui.moveTo(708, 114+(4*19)+1) IS FIRST PX OUTSIDE OF BOTTOM OF MINIMAP
	# 114+(4*19)+1 = 191
	# SO MINIMAP RADIUS FROM TOP TO BOTTOM PNTS IS = [39, 190]
	# diameter: 191 - 38 = 151 pixels
	# radius: 151 / 2 = 75.5 = 76 pixels
	# 4 pixels = 1 square length and so therefore:
	# 76 / 4 = 19

	# FROM OSRS WIKI
	# The mini_map appears as an approximately circular area with a 19 square-length radius
	# 1 square-length equals 4 pixels so
	# 19 * 4 = 76

	# SO CORRECT