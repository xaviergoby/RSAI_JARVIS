from src.game.inv_handler import InventoryHandler


class BasicSelfContainedBot:

    def __init__(self, vision_cls):
        self.vision_cls = vision_cls
        self.inv = InventoryHandler()




if __name__ == "__main__":
    from jarvis.vision_sys.vision_cls import Vision
    from jarvis.game_client.game_client import GameClient

    game_client = GameClient()
    game_client.set_wndw_pos_and_size() # osrs game window pos & dims set to (0, 0, 800, 600)
    game_client_area_roi = game_client.get_client_area_pos_and_size() # -> (8, 31, 783, 560)

    max_detections = 3
    confidence_threshold = 0.1
    max_obj_frames_lost = 2
    vision = Vision(game_client_area_roi, max_detections, confidence_threshold, max_obj_frames_lost)
    vision.enable_manual_recording(True)

    bot = BasicSelfContainedBot(vision)