import settings
from jarvis.utils import screen_tools
import win32gui
import time
from collections import namedtuple


class FederatedGameClient:

	def __init__(self, wndw_name="Old School RuneScape", init_wndw_rect=(0, 0, 800, 600)):
		self.wndw_name = wndw_name
		self.init_wndw_rect = init_wndw_rect
		self.wndw_hndl = win32gui.FindWindow(None, self.wndw_name)
		self._init_wndw_rect_setup()

	def _init_wndw_rect_setup(self):
		if self.init_wndw_rect is not None:
			# # Window pos (left, top) relative to the upper-left corner of the screen
			init_wndw_pos = (self.init_wndw_rect[0], self.init_wndw_rect[1])
			# Window size (width, height) relative to the upper-left corner of the screen
			init_wndw_size = (self.init_wndw_rect[2], self.init_wndw_rect[3])
			# win32gui.SetForegroundWindow(self.wndw_hndl)
			win32gui.MoveWindow(self.wndw_hndl, init_wndw_pos[0], init_wndw_pos[1],
			                    init_wndw_size[0], init_wndw_size[1], True)

	@property
	def wndw_coords(self):
		"""
		# NOTE:  the border width reports 16 pixels, so 8 pixels a side. However, only 1 of those pixels are visible.
		# 7 of them are transparent. So your window has a transparent 7 pixels to the left, right, and bottom.
		:return: Screen coordinates of the upper-left and lower-right corners of the window, (left, top, right, bottom)
		"""
		wndw_coords = win32gui.GetWindowRect(self.wndw_hndl)
		return wndw_coords

	@property
	def wndw_left(self):
		"""
		:return: Left side screen coordinate of the window
		"""
		wndw_left = self.wndw_coords[0]
		return wndw_left

	@property
	def wndw_top(self):
		"""
		:return: Top side screen coordinate of the window
		"""
		wndw_top = self.wndw_coords[1]
		return wndw_top

	@property
	def wndw_right(self):
		"""
		:return: Right side screen coordinate of the window
		"""
		wndw_right = self.wndw_coords[2]
		return wndw_right

	@property
	def wndw_bottom(self):
		"""
		:return: Bottom side screen coordinate of the window
		"""
		wndw_bottom = self.wndw_coords[3]
		return wndw_bottom

	@property
	def wndw_width(self):
		"""
		:return: Pixel width of the window (= wndw_right - wndw_left)
		"""
		wndw_width = self.wndw_right - self.wndw_left
		return wndw_width

	@property
	def wndw_height(self):
		"""
		:return: Pixel height of the window (= wndw_bottom - wndw_top)
		"""
		wndw_height = self.wndw_bottom - self.wndw_top
		return wndw_height

	@property
	def wndw_size(self):
		"""
		:return: Pixel width and height of the window
		"""
		wndw_width = self.wndw_width
		wndw_height = self.wndw_height
		return wndw_width, wndw_height

	@property
	def client_rect(self):
		"""
		NOTE: The client coordinates are relative to the upper-left corner of a window's client area, the
		coordinates of the upper-left corner are (0,0).
		NOTE: The bottom-right coordinates of the returned rectangle are EXCLUSIVE. In other words,
		the pixel at (right, bottom) lies immediately outside the rectangle.
		:return: The window's client area 'client' coordinates
		"""
		client_rect = win32gui.GetClientRect(self.wndw_hndl)
		return client_rect

	@property
	def client_local_left(self):
		"""
		:return: Always 0
		"""
		client_local_left = self.client_rect[0]
		return client_local_left

	@property
	def client_local_top(self):
		"""
		:return: Always 0
		"""
		client_local_top = self.client_rect[1]
		return client_local_top

	@property
	def client_px_width(self):
		"""
		NOTE: The bottom-right coordinates of the returned rectangle are EXCLUSIVE. In other words,
		the pixel at (right, bottom) lies immediately outside the rectangle.
		:return: The pixel width of the client area w/ the left & right pixels being INCLUSIVE,
		i.e. horizontal scrren px coords incl. within the client area (valid mouse click's within the game client area) are:
		[left, left+1, ..., right-1, right]
		"""
		client_px_width = self.client_rect[2] - 1
		return client_px_width

	@property
	def client_px_height(self):
		"""
		NOTE: The bottom-right coordinates of the returned rectangle are EXCLUSIVE. In other words,
		the pixel at (right, bottom) lies immediately outside the rectangle.
		:return: The pixel height of the client area w/ the top & bottom pixels being INCLUSIVE,
		i.e. vertical scrren px coords incl. within the client area (valid mouse click's within the game client area) are:
		[top, left+1, ..., bottom-1, bottom]
		"""
		client_px_height = self.client_rect[3] - 1
		return client_px_height

	@property
	def client_scr_left(self):
		"""
		The left side border is 8 pixels in total (1 visible px + 7 transparent pxs)
		:return: The clients left side scr px coord
		"""
		client_scr_left = self.wndw_left + 8
		return client_scr_left

	@property
	def client_scr_top(self):
		"""
		The title bar border is 31 pxs
		:return: The clients top side scr px coord
		"""
		client_scr_top = self.wndw_top + 31
		return client_scr_top

	@property
	def client_scr_right(self):
		"""
		:return: The clients right side scr px coord
		"""
		client_scr_right = self.client_px_width + 8 + self.wndw_left
		# client_scr_right = self.client_px_width - 1 + 8 + self.wndw_left
		return client_scr_right

	@property
	def client_scr_bottom(self):
		"""
		:return: The clients bottom side scr px coord
		"""
		client_scr_bottom = self.client_px_height + 31 + self.wndw_top
		# client_scr_bottom = self.client_px_height - 1 + 31 + self.wndw_top
		return client_scr_bottom

	@property
	def centre(self):
		scr_centre_x = 8 + self.client_px_width // 2 - 8 + self.wndw_left
		scr_centre_y = 31 + self.client_px_height // 2 - 7 + 31 + self.wndw_top
		return scr_centre_x, scr_centre_y


if __name__ == "__main__":
	time.sleep(3)
	game_client = FederatedGameClient(wndw_name="Old School RuneScape", init_wndw_rect=(0, 0, 800, 600))
	while True:
		print("\nSleeping for 3 seconds")
		time.sleep(3)
		print(
			f"wndw rect (l, t, r, b): {(game_client.wndw_left, game_client.wndw_top, game_client.wndw_right, game_client.wndw_bottom)}")
		print(f"wndw size (width, height): {(game_client.wndw_width, game_client.wndw_height)}")
		print(f"client local pos (l, t): {(game_client.client_local_left, game_client.client_local_top)}")
		print(f"client px size (width, height): {(game_client.client_px_width, game_client.client_px_height)}")
		print(
			f"client scr incl coords (l, t, r, b): {(game_client.client_scr_left, game_client.client_scr_top, game_client.client_scr_right, game_client.client_scr_bottom)}")
		print(f"centre scr coords (x, y): {(game_client.centre)}")
# print(f"wndw_left: {game_client.wndw_left}")
# print(f"wndw_top: {game_client.wndw_top}")
# print(f"wndw_right: {game_client.wndw_right}")
# print(f"wndw_bottom: {game_client.wndw_bottom}")
# print(f"wndw_width: {game_client.wndw_width}")
# print(f"wndw_height: {game_client.wndw_height}")
# print(f"client_local_left: {game_client.client_local_left}")
# print(f"client_local_top: {game_client.client_local_top}")
# print(f"client_px_width: {game_client.client_px_width}")
# print(f"client_px_height: {game_client.client_px_height}")
# print(f"client_scr_left: {game_client.client_scr_left}")
# print(f"client_scr_top: {game_client.client_scr_top}")
# print(f"client_scr_right: {game_client.client_scr_right}")
# print(f"client_scr_bottom: {game_client.client_scr_bottom}")

# time.sleep(3)
# game_client = GameClient(wndw_name="Old School RuneScape", init_wndw_rect=(0, 0, 800, 600), init_setup=True)
# print(f"game_client.current_wndw_rect: {game_client.wndw_properties}")
# print(f"game_client.current_client_rect{game_client.client_properties}")
# print(win32gui.ClientToScreen(game_client.wndw_hndl, (game_client.wndw_left, game_client.wndw_top)))
# wndw_name = "Old School RuneScape"
# wndw_hndl = win32gui.FindWindow(None, wndw_name)
# time.sleep(3)
# win32gui.SetForegroundWindow(wndw_hndl)
# win32gui.MoveWindow(wndw_hndl, 0, 0,
#                     800, 600, True)
# wndw_rect = win32gui.GetWindowRect(wndw_hndl)
# print(f"wndw_rect: {wndw_rect}")
# wndw_rect_client_coords_tl = win32gui.ScreenToClient(wndw_hndl, (wndw_rect[0], wndw_rect[1]))
# wndw_rect_client_coords_rb = win32gui.ScreenToClient(wndw_hndl, (wndw_rect[2], wndw_rect[3]))
# print(f"wndw_rect_client_coords_tl: {wndw_rect_client_coords_tl}")
# print(f"wndw_rect_client_coords_rb: {wndw_rect_client_coords_rb}")
# wndw_rect_client_coords_tl = win32gui.ScreenToClient(wndw_hndl, (wndw_rect[0], wndw_rect[1]))
# wndw_rect_client_coords_rb = win32gui.ScreenToClient(wndw_hndl, (wndw_rect[2], wndw_rect[3]))
# print(f"wndw_rect_client_coords_tl: {wndw_rect_client_coords_tl}")
# print(f"wndw_rect_client_coords_rb: {wndw_rect_client_coords_rb}")