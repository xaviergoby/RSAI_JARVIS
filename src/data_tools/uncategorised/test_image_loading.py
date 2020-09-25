import numpy as np
from PIL import Image
import cv2
from src.ui_automation_tools import screen_tools
import win32gui
from PIL import ImageGrab
# import sys
# np.set_printoptions(threshold=sys.maxsize)



# img_file_name = "slaying_obj_dect_125.jpg"
win_name = "Old School RuneScape"
hwnd = win32gui.FindWindow(None, win_name)
wndw_x_wrt_screen = 0  # -8
wndw_y_wrt_screen = 0  # -31
wndw_width_in_screen = 800
wndw_height_in_screen = 600
screen_tools.set_window_pos_and_size(hwnd = None, x_new = wndw_x_wrt_screen, y_new = wndw_y_wrt_screen,
                                     new_width = wndw_width_in_screen, new_height = wndw_height_in_screen,
                                     wndw_name= win_name)

client_rect_pos_n_size = win32gui.GetClientRect(hwnd)
wndw_left_border_pxs_width = 8
wndw_top_border_pxs_height = 31
client_area_width = wndw_width_in_screen-8
client_area_height = wndw_height_in_screen-8
client_region = (wndw_left_border_pxs_width, wndw_top_border_pxs_height, client_area_width, client_area_height)

mm_left_x = 584
mm_top_y = wndw_top_border_pxs_height
mm_width = client_area_width
mm_height = 190 + 8
mm_region = (mm_left_x, mm_top_y, mm_width, mm_height)
# region = (0, 0, client_rect_pos_n_size[2], client_rect_pos_n_size[3])

# client_rect_pos_n_size = win32gui.GetClientRect(hwnd)
screen_shot1 = np.array(ImageGrab.grab(bbox=client_region))
screen_shot2 = np.array(ImageGrab.grab(bbox=mm_region))
# img = Image.open(img_file_name)
# img = cv2.imread(img_file_name, 0)
cv2.imshow('screen_shot1', cv2.cvtColor(screen_shot1, cv2.COLOR_BGR2RGB))
cv2.imshow('screen_shot2', cv2.cvtColor(screen_shot2, cv2.COLOR_BGR2RGB))
# cv2.imshow('window', screen_shot)
cv2.waitKey(0)
cv2.destroyAllWindows()
