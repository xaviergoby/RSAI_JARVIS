






class GameSquare:

	def __init__(self, vissited, grid_sq_coords, wm_sq_coords):

		self.vissited = vissited
		self.grid_sq_coords = grid_sq_coords
		self.grid_sq_x_coord = self.grid_sq_coords[0]
		self.grid_sq_y_coord = self.grid_sq_coords[1]
		self.wm_sq_coords = wm_sq_coords
		self.wm_sq_x_coord = self.wm_sq_coords[0]
		self.wm_sq_y_coord = self.wm_sq_coords[1]