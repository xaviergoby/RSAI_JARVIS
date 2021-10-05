import settings
from jarvis.utils import screen_tools
import win32gui

class GameClient:

	# GAME_WNDW_POS = (0, 0)
	# GAME_WNDW_SIZE = (800, 600)
	# settings.GAME_WNDW_NAME = "Old School RuneScape"
	# Setting/moving the game wndw to the init pos of (0, 0) w/ an init size of (800, 600)
	# will then return the following for the following func calls:
	# >>> print(win32gui.GetWindowRect(handle))
	#       (0, 0, 800, 600)
	# >>> print(win32gui.GetClientRect(handle))
	#       (0, 0, 784, 561)
	# handle = win32gui.FindWindow(None, "Old School RuneScape")
	# wndw_rect = win32gui.GetWindowRect(handle)

	def __init__(self, wndw_pos=(0, 0), wndw_size=(800, 600), wndw_name="Old School RuneScape", wndw_auto_setup=False):
		# Window position
		self.wndw_pos = wndw_pos # i.e. (0, 0)
		self.__init_wndw_pos = wndw_pos # i.e. (0, 0)
		self.wndw_x_pos, self.wndw_y_pos = self.wndw_pos[0], self.wndw_pos[1]
		self.__init_wx, self.__init_wy = self.__init_wndw_pos[0], self.__init_wndw_pos[1]
		####
		self.wndw_size = wndw_size # i.e. (800, 600)
		self.__init_wndw_size = wndw_size # i.e. (800, 600)
		self.wndw_width, self.wndw_height = self.wndw_size[0], self.wndw_size[1]
		self.__init_ww, self.__init_wh = self.__init_wndw_size[0], self.__init_wndw_size[1]
		###

		self.wndw_name = wndw_name # i.e. = "Old School RuneScape"
		if wndw_auto_setup is True:
			self.set_wndw_pos_and_size()
		else:
			pass
		self.client_area_pos_wrt_screenj_and_size = None
		self.client_xo = None
		self.client_yo = None
		self.client_origin_wrt_screen = None
		self.client_width = None
		self.client_height = None
		self.client_size = None
		self.client_tlxy_brxy_wrt_screen = None
		self.client_brx = None
		self.client_bry = None


	def __init_game_client_hwnd(self):
		self.__hwnd = win32gui.FindWindow(None, self.wndw_name)

	def __resize_and_move_2_init_pos(self):
		win32gui.SetForegroundWindow(self.__hwnd)
		win32gui.MoveWindow(self.__hwnd, self.self.__init_wx, self.__init_wy,
		                    self.__init_ww, self.__init_wh, bRepaint=True)


	def __get_current_wndw_rect(self):
		__current_wndw_rect = win32gui.GetWindowRect(self.__hwnd)
		return __current_wndw_rect

	def __get_current_client_rect(self):
		__current_client_rect = win32gui.GetClientRect(self.__hwnd)
		return __current_client_rect

	def __get_current_left_top_right_bottom(self):
		__current_client_rect = self.__get_current_client_rect()
		__current_cx, __current_cy, __current_cw, __current_ch = __current_client_rect
		sx, sy = win32gui.ClientToScreen(self.__hwnd, (__current_cx, __current_cy))
		__current_client_wx, __current_client_wy = win32gui.ClientToScreen(self.__hwnd, (cx1 - sx, cy1 - sy))
		sx1, sy1 = win32gui.ClientToScreen(hwnd, (cx1 - sx, cy1 - sy))
		# win32gui.ScreenToClient(self.__hwnd, (win32gui.GetWindowRect(self.__hwnd)[0], win32gui.GetWindowRect(self.__hwnd)[1]))
		# __current_wndw_rect = self.__get_current_wndw_rect()
		# __current_wndw_left, __current_wndw_top =

	# def __current_client_rect(self):
	# 	__current_client_rect = win32gui.GetClientRect(self.__hwnd)
	# 	return __current_client_rect

	# @property
	# def current_client_rect(self):
	# 	current_client_rect = win32gui.GetClientRect(self.__hwnd)
	# 	return current_client_rect


	def __repr__(self):
		game_client_properties_info = f"Window name: {self.wndw_name}" \
		                              f"Window top left (x,y) origin pnt wrt screen: {(self.wndw_x_pos, self.wndw_y_pos)}" \
		                              f"Window size (width, height): {(self.wndw_width, self.wndw_height)}" \
		                              f"Client top left (x,y) wrt to screen: {(self.client_xo, self.client_yo)}" \
		                              f"Client area (width, height): {(self.client_width, self.client_height)}"
		return game_client_properties_info





	def __set_game_client_properties(self):
		self.client_area_pos_wrt_screenj_and_size = screen_tools.get_client_pos_and_size(self.wndw_name)
		self.client_xo, self.client_yo = self.client_area_pos_wrt_screenj_and_size[0], self.client_area_pos_wrt_screenj_and_size[1]
		self.client_origin_wrt_screen = (self.client_xo, self.client_yo)
		self.client_width, self.client_height = self.client_area_pos_wrt_screenj_and_size[2], self.client_area_pos_wrt_screenj_and_size[3]
		self.client_size = (self.client_width, self.client_height)
		self.client_tlxy_brxy_wrt_screen = screen_tools.get_client_tlxy_brxy_wrt_screen(self.wndw_name)
		self.client_brx, self.client_bry = (self.client_tlxy_brxy_wrt_screen[2], self.client_tlxy_brxy_wrt_screen[3])

	def set_wndw_pos_and_size(self) -> '(wx1, wy1, wx2, wy2), i.e. (0, 0, 800, 600)':
		"""
		Sets the game window position and dimensions using (wndw_pos, wndw_size)
		which by default will be (0, 0, 800, 600)
		:return:
		"""
		screen_tools.set_window_pos_and_size(hwnd=None, x_new=self.wndw_x_pos, y_new=self.wndw_y_pos,
		                                     new_width=self.wndw_width, new_height=self.wndw_height, wndw_name=self.wndw_name)


	def set_and_init_game_client(self):
		self.set_wndw_pos_and_size()
		self.__set_game_client_properties()


	def update_game_client(self):
		wndw_tl_br_coords = screen_tools.get_window_screen_tl_br_coords(self.wndw_name)
		self.wndw_x_pos, self.wndw_y_pos, = wndw_tl_br_coords[0], wndw_tl_br_coords[1]
		self.wndw_pos = (self.wndw_x_pos, self.wndw_y_pos)
		# self.wndw_size = (wndw_tl_br_coords[0]+1, wndw_tl_br_coords[1]+1)
		if self.wndw_x_pos == 0:
			self.wndw_width = self.wndw_x_pos[0] + wndw_tl_br_coords[2] + 1
		elif self.wndw_x_pos != 0:
			self.wndw_width = wndw_tl_br_coords[2] - self.wndw_x_pos[0]

		if self.wndw_y_pos == 0:
			self.wndw_height = self.wndw_y_pos[1] + wndw_tl_br_coords[3] + 1
		elif self.wndw_y_pos != 0:
			self.wndw_height = wndw_tl_br_coords[3] - self.wndw_y_pos[1]


		if self.wndw_x_pos == 0 and self.wndw_y_pos == 0:
			self.wndw_width, self.wndw_height = wndw_tl_br_coords[0]+1,  wndw_tl_br_coords[1]+1
		# elsif
		self.wndw_width, self.wndw_height = wndw_tl_br_coords[0] + 1, wndw_tl_br_coords[1] + 1
		self.wndw_size = (wndw_tl_br_coords[0] + 1, wndw_tl_br_coords[1] + 1)


	def update_game_client_properties(self):
		pass

	def get_client_tl_br_coords_wrt_screen(self) -> '(tlx, tly, brx, bry), i.e. (8, 31, 791, 591)':
		"""
		:return: a 4-tuple consisting of (client_area_tl_pos_x, client_area_tl_pos_y, client_area_width, client_area_height)
		E.g. init this cls w/ the def args in its __init__ i.e. settings.GAME_WNDW_POS=(0,0) & settings.GAME_WNDW_SIZE=(800,600)
		will lead to this metod returning the tuple (8, 31, 791, 591) <=> (lx, ty, rx, by)
		Where (lx, ty, rx, by) ⩧ (Left Most x coord, Top Most y coord, Right Most x coord, Bottom Most y coord)
		"""
		return screen_tools.get_client_tlxy_brxy_wrt_screen()
