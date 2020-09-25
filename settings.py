import os
import numpy as np

# Primary/Major dir paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   # returns 'C:\\Users\\XGOBY\\RSAIBot'
DATA_DIR = os.path.join(ROOT_DIR, "data")     # returns 'C:\\Users\\XGOBY\\RSAIBot\\data'
TF_MODELS_DIR = os.path.join(ROOT_DIR, r"src\TensorFlow_Models")    # returns 'C:\\Users\\XGOBY\\RSAIBot\\src\\TensorFlow_Models'

END_2_END_SLAM_DATA_DIR = os.path.join(DATA_DIR, r"end_2_end_slam_data")
EVENT_DRIVEN_SYS_DATA_DIR = os.path.join(DATA_DIR, r"event_driven_sys_data")
MAP_DATA_DIR = os.path.join(DATA_DIR, r"map_data")

# Object detection dir paths:
OBJ_DECT_DATA_DIR = os.path.join(DATA_DIR, r"obj_dect_data")
OBJ_DECT_TRAINING_DIR = os.path.join(ROOT_DIR, r"training")
OBJ_DECT_TRAINING_CKPTS_DIR = os.path.join(OBJ_DECT_TRAINING_DIR, r"checkpoints")
OBJ_DECT_TRAINING_PIPELINE_CONFIGS_DIR = os.path.join(OBJ_DECT_TRAINING_DIR, r"config_files")
OBJ_DECT_TRAINING_LABEL_MAPS_DIR = os.path.join(OBJ_DECT_TRAINING_DIR, r"label_maps")
OBJ_DECT_INFERENCE_GRAPHS_DIR = os.path.join(ROOT_DIR, r"inference_graph")
# end_2_end_slam_data

# Game play imitation data collected dir paths:
GAME_PLAY_IMITATION_DATA_DIR = os.path.join(DATA_DIR, "game_play_imitation_data")
MOUSE_MOTION_DATA_DIR = os.path.join(GAME_PLAY_IMITATION_DATA_DIR, "mouse_motion_data")

# mouse_nVirtKey_dict = {"LMB":0x01, "RMB":0x02}
mouse_nVirtKey_dict = {"LMB":0x01}
mouse_nVirtKey_dict_keys = list(mouse_nVirtKey_dict.keys())
keyboard_nVirtKey_dict = {"P":0x50, "T":0x54, "S":0x53, "R":0x52, "L":0x4C, "A":0x41, "B":0x42, "C":0x43, "I":0x49}
keyboard_nVirtKey_dict_keys = list(keyboard_nVirtKey_dict.keys())
GAME_WNDW_POS_AND_SIZE = (0, 0, 800, 600) # {most_left_x_wrt_screen, most_top_y_wrt_screen, window_width, window_height)
GAME_WNDW_POS = (0, 0)
GAME_WNDW_SIZE = (800, 600)
# GAME_WNDW_NAME = "RuneLite - PolarHobbes"
GAME_WNDW_NAME = "Old School RuneScape"
GAME_CLIENT_CENTRE_PX_COORDS = 400, 310
GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT = {"Old School RuneScape": {"left": 8, "top": 31 ,"right": 791, "bottom": 591},
                                              "RuneLite - PolarHobbes": {"left": 4, "top": 27 ,"right": 795, "bottom": 595}}
#l=8, r=784
#t=31, b=568

MESH_GRID_OPTIONS = {1:{"x_grid_pnts":(150, 650, 11), "y_grid_pnts":(60, 560, 11)}, 2:{"x_grid_pnts":(150, 650, 11), "y_grid_pnts":(60, 560, 11)},
                     2:{"x_grid_pnts":(150, 650, 11), "y_grid_pnts":(60, 560, 11)}, 2:{"x_grid_pnts":(150, 650, 11), "y_grid_pnts":(60, 560, 11)},}


NAVIGATION_TASKS = {"lumbridge_2_cows:":np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
                    "cows_2_lumbridge":np.array([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]),
                    }


WORLD_MAP_REGION_GRID_LABELS = [12850]

USERNAME = "xaviergoby"
PASSWORD = "keyboard"

# - Grid (centre) point (0, 0):
#   - Valid pixels x coords: [708, 709, 710, 711]
#   - Valid pixels y coords: [113, 114, 115, 116]

MM_CENTRE_SQ_LEFT_PXX = 708
MM_CENTRE_SQ_RIGHT_PXX = 711
MM_CENTRE_SQ_TOP_PXY = 113
MM_CENTRE_SQ_BOTTOM_PXY = 116

MM_PX_SQ_LEN = 4
