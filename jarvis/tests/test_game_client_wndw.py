import time
from jarvis.game_client.game_client import GameClient

# If set_window_pos_and_size() is called w/ def parameter args,
# i.e. (0, 0, 800, 600) then game_client_area_roi should be (8, 31, 791, 591)
wndw_pos = (0, 0)
wndw_size = (800, 600)
game_client = GameClient(wndw_pos=wndw_pos, wndw_size=wndw_size)
game_client.set_wndw_pos_and_size()  # osrs game window pos & dims set to (0, 0, 800, 600)


game_client_area_roi = game_client.get_client_tl_br_coords_wrt_screen()  # -> (8, 31, 783, 560)

print(f"Window position (l, t) & size (w, h): {wndw_pos} & {wndw_size}")
print(f"Game Client Area ROI (l, t, w, h): {game_client_area_roi}")

