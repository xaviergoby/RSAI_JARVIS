from research_and_dev.event_driven_system.game_client.game_client import GameClient
from jarvis.vision_sys.vision_cls import Vision




game_client = GameClient()
game_client.set_wndw_pos_and_size()
game_client_area_roi = game_client.get_client_area_pos_and_size()


max_detections = 10
confidence_threshold = 0.1
max_obj_frames_lost = 5





