import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import ImageGrab
from jarvis.game_client.game_client import GameClient
from jarvis.vision_sys.vision_cls import Vision
from jarvis.utils.vision_sys_helper_util import VisionSysHelperUtil


# def get_roi_ss() -> "(h, w, c) shaped array":
#     """
#     :return: game client area screen shot img numpy array w/ shape (h, w, c)
#     """
#     roi_screen_shot = np.array(ImageGrab.grab(bbox=roi))
#     return roi_screen_shot



# If set_window_pos_and_size() is called w/ def parameter args,
# i.e. (0, 0, 800, 600) then game_client_area_roi should be (8, 31, 791, 591)
game_client = GameClient()
game_client.set_wndw_pos_and_size() # osrs game window pos & dims set to (0, 0, 800, 600)
game_client_area_roi = game_client.get_client_area_pos_and_size() # -> (8, 31, 783, 560)
max_detections = 3
confidence_threshold = 0.1
max_obj_frames_lost = 2
vision = Vision(game_client_area_roi, max_detections, confidence_threshold, max_obj_frames_lost)
vision.enable_manual_recording(True)
display_util = VisionSysHelperUtil(show_all_overlaid_text_info=False)

window = sg.Window('OSRS_JARVIS Vision System Testing GUI', [[sg.Image(filename='', key='image')], ], location=(800, 400))
# window = sg.Window('Demo Application - OpenCV Integration', [[sg.Image(filename='', key='image')], ], location=(800, 400))

# cap = cv2.VideoCapture(0)  # Setup the camera as a capture device


while True:  # The PSG "Event Loop"
    bgr_frame = vision.sensor.get_frame()  # frame.shape -> (560, 783)
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)

    frame = rgb_frame
    # ret, frame = cap.read()

    display_util.print_obj_dect_input_frame_info(obj_dect_input_frame=frame)

    event, values = window.Read(timeout=20, timeout_key='timeout')  # get events for the window with 20ms max wait

    if event is None:
        break  # if user closed window, quit

    window.FindElement('image').Update(data=cv2.imencode('.png', frame)[1].tobytes())  # Update image in window
    # window.FindElement('image').Update(data=cv2.imencode('.png', cap.read()[1])[1].tobytes())  # Update image in window
