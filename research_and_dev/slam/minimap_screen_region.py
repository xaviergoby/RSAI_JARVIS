import settings
# from research_and_dev.misc_slam import



class MiniMapScreenRegion:


	def __init__(self, current_world_grid_coords=(3216, 3219), mm_radius_sq_len=10):
		self.mm_radius_sq_len = mm_radius_sq_len
		self.current_world_grid_coords = current_world_grid_coords


	@property
	def left(self):
		left_most_coord = settings.MM_CENTRE_SQ_LEFT_PXX - self.mm_radius_sq_len * 4
		return left_most_coord

	@property
	def top(self):
		top_most_coord = settings.MM_CENTRE_SQ_TOP_PXY - self.mm_radius_sq_len * 4
		return top_most_coord

	@property
	def right(self):
		right_most_coord = settings.MM_CENTRE_SQ_RIGHT_PXX + self.mm_radius_sq_len * 4
		return right_most_coord

	@property
	def bottom(self):
		bottom_most_coord = settings.MM_CENTRE_SQ_BOTTOM_PXY + self.mm_radius_sq_len * 4
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
		bbox_coords = (self.left, self.top, self.right + 1, self.bottom + 1)
		return bbox_coords

	@property
	def width(self):
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
		dimensions = {width, height}
		return dimensions




if __name__ == "__main__":
	mm = MiniMapScreenRegion(current_world_grid_coords=(3216, 3219), mm_radius_sq_len=7)
	print(mm.left_top_coord)
	print(mm.right_bottom_coord)
	print(mm.lt_rb_boundary_coords)
