import settings
from research_and_dev.event_driven_system.utils.data_storage_tools import get_bot_current_loc
# from research_and_dev.slam import



class MiniMapScreenRegion:
	"""
	Check Minimap class located @
	from research_and_dev.event_driven_system.mini_map.minimap import Minimap
	for information
	"""
	def __init__(self, nav_grid_side_len):
		self.local_nav_sq_grid_side_len = nav_grid_side_len
		self.mm_radius_sq_len = int(self.local_nav_sq_grid_side_len / 2)

	@property
	def left(self):
		left_most_px_coord = settings.MM_CENTRE_SQ_LEFT_PXX - self.mm_radius_sq_len * 4
		return left_most_px_coord

	@property
	def top(self):
		top_most_coord = settings.MM_CENTRE_SQ_TOP_PXY - self.mm_radius_sq_len * 4
		return top_most_coord

	@property
	def right(self):
		right_most_coord = settings.MM_CENTRE_SQ_LEFT_PXX + self.mm_radius_sq_len * 4 + 3
		# right_most_coord = settings.MM_CENTRE_SQ_RIGHT_PXX + self.mm_radius_sq_len * 4
		return right_most_coord

	@property
	def bottom(self):
		bottom_most_coord = settings.MM_CENTRE_SQ_TOP_PXY + self.mm_radius_sq_len * 4 + 3
		# bottom_most_coord = settings.MM_CENTRE_SQ_BOTTOM_PXY + self.mm_radius_sq_len * 4
		return bottom_most_coord

	@property
	def left_top_coord(self):
		left_top_coord = (self.left, self.top)
		return left_top_coord

	@property
	def right_bottom_coord(self):
		right_bottom_coord = (self.right, self.bottom)
		return right_bottom_coord

	@property
	def lt_rb_boundary_coords(self):
		lt_rb_boundary_coords = (self.left_top_coord[0], self.left_top_coord[1],
		                         self.right_bottom_coord[0], self.right_bottom_coord[1])
		return lt_rb_boundary_coords

	@property
	def x1y1_x2y2(self):
		return self.lt_rb_boundary_coords

	@property
	def bbox_coords(self):
		bbox_coords = (self.left, self.top, self.right+1, self.bottom+1)
		return bbox_coords

	@property
	def minimap_roi_img_bbox_coords(self):
		return self.bbox_coords

	@property
	def width(self):
		# bbox_coords = self.bbox_coords
		# x1, y1, x2, y2 = bbox_coords
		width = (self.right + 1) - self.left
		return width

	@property
	def height(self):
		height = (self.bottom + 1) - self.top
		return height

	@property
	def dimensions(self):
		width = self.width
		height = self.height
		dimensions = [width, height]
		return dimensions




# if __name__ == "__main__":
# 	mm = MiniMapScreenRegion(current_world_grid_loc=(3216, 3219), mm_radius_sq_len=7)
# 	print(mm.left_top_coord)
# 	print(mm.right_bottom_coord)
# 	print(mm.lt_rb_boundary_coords)