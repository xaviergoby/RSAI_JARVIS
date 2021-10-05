import settings
from src.ui_automation_tools import screen_tools

class GameClient:

	def __init__(self, wndw_pos=settings.GAME_WNDW_POS, wndw_size=settings.GAME_WNDW_SIZE, wndw_name=settings.GAME_WNDW_NAME, wndw_auto_setup=False):
		self.wndw_pos = wndw_pos # i.e. (0, 0)
		self.wndw_x_pos, self.wndw_y_pos = self.wndw_pos[0], self.wndw_pos[1]
		self.wndw_size = wndw_size # i.e. (800, 600)
		self.wndw_width, self.wndw_height = self.wndw_size[0], self.wndw_size[1]
		self.wndw_name = wndw_name # i.e. = "Old School RuneScape"
		if wndw_auto_setup is True:
			self.set_wndw_pos_and_size()
		else:
			pass

	def set_wndw_pos_and_size(self):
		screen_tools.set_window_pos_and_size(hwnd=None, x_new=self.wndw_x_pos, y_new=self.wndw_y_pos,
		                                     new_width=self.wndw_width, new_height=self.wndw_height, wndw_name=self.wndw_name)

	def get_client_area_pos_and_size(self):
		"""
		:return: a 4-tuple consisting of (client_area_tl_pos_x, client_area_tl_pos_y, client_area_width, client_area_height)
		If a window was set with out specifying its specific desired position or dimensions this will mean that
		the window will have been set using the def settings (0, 0, 800, 600) found in settings.py
		If this is the case then the value of the elements in the tuple returned are: (8, 31, 560, 783)
		"""
		return screen_tools.get_client_tlxy_brxy_wrt_screen()

