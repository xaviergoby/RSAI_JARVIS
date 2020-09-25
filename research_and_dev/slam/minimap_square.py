import settings


class MiniMapSquare:

	settings.MM_PX_SQ_LEN = 4

	def __init__(self, x, y):
		self.local_x = x
		self.local_y = y
		# self.left_most_px = 708 + self.local_x * self.MM_PX_SQ_LEN
		self.left_most_px = settings.MM_CENTRE_SQ_LEFT_PXX + self.local_x * settings.MM_PX_SQ_LEN

		# self.top_most_px = 114 + self.local_y * self.MM_PX_SQ_LEN
		self.top_most_px = settings.MM_CENTRE_SQ_TOP_PXY + self.local_y * settings.MM_PX_SQ_LEN

		# self.right_most_px = 711 + self.local_x * self.MM_PX_SQ_LEN
		self.right_most_px = settings.MM_CENTRE_SQ_RIGHT_PXX + self.local_x * settings.MM_PX_SQ_LEN

		# self.bottom_most_px = 117 + self.local_y * self.MM_PX_SQ_LEN
		self.bottom_most_px = settings.MM_CENTRE_SQ_BOTTOM_PXY + self.local_y * settings.MM_PX_SQ_LEN
