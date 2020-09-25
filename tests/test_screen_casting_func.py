import screen_casting_func
import tiledb



if __name__ == "__main__":
	import screen_casting_func
	from src.ui_automation_tools import screen_tools
	screen_tools.set_window_pos_and_size()
	roi = screen_tools.get_client_specific_bounding_region_px_coords()  # returns (8, 31, 791, 591)
	screen_casting_func.screen_caster(roi)