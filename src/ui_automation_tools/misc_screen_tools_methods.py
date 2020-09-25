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


def grab_screen(region=None):
	"""
	:param region:  if an arg for the screen region of interest is passed then it should
	be done so using a 4-tuple consisting of the following left, top, right &
	bottom x & local_y coordinate points/positions:
	(left_x, top_y,
	:return:
	"""
	hwin = win32gui.GetDesktopWindow()
	if region:
		left, top, x2, y2 = region
		width = x2 - left + 1
		height = y2 - top + 1
	else:
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
		left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
		top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
	signedIntsArray = bmp.GetBitmapBits(True)
	img = np.fromstring(signedIntsArray, dtype='uint8')
	img.shape = (height, width, 4)
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)
	win32gui.DeleteObject(bmp.GetHandle())
	return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

def grab_screen_v2(region=None):
	"""
	:param region: if an arg for the screen region of interest is passed then it should
	be done so using a 4-tuple consisting of the following values:
	(left_x, top_y, width, height)
	In this case then the provided values will be used for screen capture/grabbing. Else,
	if no argument is provided then
	:return: The ndarray of the image which has been converted from BGRA to RGB colour space. This
	just basically removes the "alpha channel" from the image and then converts the OG BGR colour space
	of the image into an RGB colour space.
	"""
	hwin = win32gui.GetDesktopWindow()
	if region:
		width = region[2]
		height = region[3]
		left = region[0]
		top = region[1]
	else:
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
		left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
		top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
	signedIntsArray = bmp.GetBitmapBits(True)
	img = np.fromstring(signedIntsArray, dtype='uint8')
	img.shape = (height, width, 4)
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)
	win32gui.DeleteObject(bmp.GetHandle())
	rgb_img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
	return rgb_img


def grab_screen_v3(region=None):
	"""
	NOTE/WARNING: Currently/so far/at the moment this method seems to be bloody useless
	:param region: if an arg for the screen region of interest is passed then it should
	be done so using a 4-tuple consisting of the following values:
	(left_x, top_y, width, height)
	In this case then the provided values will be used for screen capture/grabbing. Else,
	if no argument is provided then
	:return: At the moment simply returns the pos & dims of my main screen, i.e. (0, 0, 1960, 1080) where:
	position (top left position coordinates): left=0 & top=0
	dimensions: width=1960 & height=1080
	"""
	hwin = win32gui.GetDesktopWindow()
	if region:
		width = region[2]
		height = region[3]
		left = region[0]
		top = region[1]
	else:
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
		left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
		top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
	hwindc = win32gui.GetWindowDC(hwin)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	bmp = win32ui.CreateBitmap()
	bmp.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(bmp)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
	signedIntsArray = bmp.GetBitmapBits(True)
	img = np.fromstring(signedIntsArray, dtype='uint8')
	img.shape = (height, width, 4)
	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(hwin, hwindc)
	win32gui.DeleteObject(bmp.GetHandle())
	# print("grab_screen_v3() func.\nleft: {0}\ntop: {1}\nwidth: {2}\nheight: {3}".format(left, top, width, height))
	return left, top, width, height


def adjust_wndw_pos_and_dims(hwnd=None, x_new=0, y_new=0,
                             new_width=800, new_height=600, window_name=settings.GAME_WNDW_NAME):
	"""
	NOTE/WARNING:
	Kind of a redundant version of the above method set_window_pos_and_size(hwnd = None, x_new = 0, y_new = 0, new_width = 800,
																			new_height = 600, window_name = settings.GAME_WNDW_NAME)
	Takes the exact same arguments for the parameters as set_window_pos_and_size(...) and returns the exact same thing as well!
	"""

	def set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
	                            window_name=settings.GAME_WNDW_NAME):
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
		:param hwnd: A handle to the window. Is None by def.
		:param x_new: The new position of the left side of the window. Is 0 by def.
		:param y_new: The new position of the top of the window. Is 0 by def.
		:param new_width: The new width of the window. Is 800 by def.
		:param new_height: The new height of the window. Is 600 by def.
		:param window_name: str of the name of the window. Is "Old School RuneScape" by def.
		:return: None
		"""
		if hwnd is None and window_name is not None:
			hwnd = win32gui.FindWindow(None, window_name)
			win32gui.MoveWindow(hwnd, x_new, y_new, new_width, new_height, True)
		elif hwnd is not None and window_name is not None:
			win32gui.MoveWindow(hwnd, x_new, y_new, new_width, new_height, True)

	return set_window_pos_and_size(hwnd=None, x_new=0, y_new=0,
	                               new_width=800, new_height=600, window_name=settings.GAME_WNDW_NAME)
