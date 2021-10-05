from jarvis.utils import screen_tools
from time import sleep

def test_get_window_screen_tl_br_coords(win_name="Old School RuneScape"):
	window_screen_tl_br_coords = screen_tools.get_window_screen_tl_br_coords(win_name)
	print(f"window_screen_tl_br_coords: {window_screen_tl_br_coords}")

def test_get_client_screen_tl_br_coords(win_name="Old School RuneScape"):
	client_screen_tl_br_coords = screen_tools.get_client_screen_tl_br_coords(win_name)
	print(f"client_screen_tl_br_coords: {client_screen_tl_br_coords}")

def test_get_client_screen_tl_coord_and_size(win_name="Old School RuneScape"):
	client_screen_tl_coord_and_size = screen_tools.get_client_screen_tl_coord_and_size(win_name)
	print(f"client_screen_tl_coord_and_size: {client_screen_tl_coord_and_size}")

def test_get_client_tlxy_brxy_wrt_screen():
	client_area_tl_pos_and_size = screen_tools.get_client_tlxy_brxy_wrt_screen()
	print(f"client_tlxy_brxy_wrt_screen: {client_area_tl_pos_and_size}")

def test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600, wndw_name="Old School RuneScape"):
	screen_tools.set_window_pos_and_size(hwnd, x_new, y_new, new_width, new_height, wndw_name)

def test_get_client_pos_and_size(wndw_name="Old School RuneScape"):
	client_pos_and_size = screen_tools.get_client_pos_and_size(wndw_name)
	print(f"client_pos_and_size: {client_pos_and_size}")





if __name__ == "__main__":
	wndw_name = "Old School RuneScape"
	# Seq of func steps 1
	print("1st Step: Set WNDW TOP LEFT POS. to (0,0) and set WNDW WIDTH & HEIGHT to (800,600)")
	# 1st Step: Set WINDOW TOP LEFT POS. to (0,0) and set WINDOW WIDTH & HEIGHT to (800,600)
	test_set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600, wndw_name=wndw_name)
	print("2nd Step: Get the WNDW TOP LEFT POS. & the WNDW WIDTH & HEIGHT -> (wndw_tlx, wndw_tly, wndw_width, wndw_height)")
	# 2nd Step: Get the WINDOW TOP LEFT POS. & the WINDOW WIDTH & HEIGHT -> (wndw_tl_x, wndw_tl_y, wndw_width, wndw_height)
	test_get_window_screen_tl_br_coords(wndw_name) # -> (0, 0, 800, 600) Gets the wndw tl x & y w.r.t the screen tp x & y
	print("3rd Step: Get the CLIENT TOP LEFT POS. & the CLIENT WIDTH & HEIGHT -> (client_tlx, client_tly, client_width, client_height)")
	# 3rd Step: Get the CLIENT TOP LEFT POS. & the CLIENT WIDTH & HEIGHT -> (client_tl_x, client_tl_y, client_width, client_height)
	test_get_client_screen_tl_br_coords(wndw_name) # -> (0, 0, 784, 561)
	print("Test Step")
	# Test step
	test_get_client_screen_tl_coord_and_size(wndw_name) # -> (8, 31, 784, 561) gets the client tl x & y w.r.t the screen tp x & y
	test_get_client_area_tl_pos_and_size() # -> (8, 31, 791, 591) gets the client tl x & y w.r.t the screen tp x & y
	# test_get_window_screen_tl_br_coords(wndw_name)
	# test_get_client_screen_tl_br_coords(wndw_name)
