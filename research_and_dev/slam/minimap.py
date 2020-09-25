from research_and_dev.slam import minimap_grid
from research_and_dev.slam import minimap_screen_region
import settings


class MiniMap:

	def __init__(self, current_world_grid_coords=(3216, 3219), mm_radius_sq_len=10):
		self.mm_rad_sq_len = mm_radius_sq_len
		self.current_wg_coords = current_world_grid_coords
		self.minimap_grid = minimap_grid.MiniMapGrid(current_world_grid_coords=self.current_wg_coords,
		                                             mm_radius_sq_len=mm_radius_sq_len)
		self.mm_screen_region = minimap_screen_region.MiniMapScreenRegion(current_world_grid_coords=self.current_wg_coords,
		                                                                  mm_radius_sq_len=mm_radius_sq_len)



if __name__ == "__main__":
	mm = MiniMap(current_world_grid_coords=(3216, 3219), mm_radius_sq_len=6)
	print(mm.mm_screen_region.left_top_coord)
	print(mm.mm_screen_region.right_bottom_coord)
	print(mm.mm_screen_region.lt_rb_boundary_coords)