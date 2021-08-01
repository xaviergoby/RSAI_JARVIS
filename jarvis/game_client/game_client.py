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

	def set_wndw_pos_and_size(self) -> '(wx1, wy1, wx2, wy2), i.e. (0, 0, 800, 600)':
		"""
		Sets the game window position and dimensions using (wndw_pos, wndw_size)
		which by default will be (0, 0, 800, 600)
		:return:
		"""
		screen_tools.set_window_pos_and_size(hwnd=None, x_new=self.wndw_x_pos, y_new=self.wndw_y_pos,
		                                     new_width=self.wndw_width, new_height=self.wndw_height, wndw_name=self.wndw_name)

	def get_client_area_pos_and_size(self) -> '(lx, ty, rx, by), i.e. (8, 31, 791, 591)':
		"""
		:return: a 4-tuple consisting of (client_area_tl_pos_x, client_area_tl_pos_y, client_area_width, client_area_height)
		E.g. init this cls w/ the def args in its __init__ i.e. settings.GAME_WNDW_POS=(0,0) & settings.GAME_WNDW_SIZE=(800,600)
		will lead to this metod returning the tuple (8, 31, 791, 591) <=> (lx, ty, rx, by)
		Where (lx, ty, rx, by) ⩧ (Left Most x coord, Top Most y coord, Right Most x coord, Bottom Most y coord)
		"""
		return screen_tools.get_client_area_tl_pos_and_size()
