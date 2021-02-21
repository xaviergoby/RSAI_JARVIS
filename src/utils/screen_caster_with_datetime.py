import cv2
from datetime import datetime
# import mss
from mss import mss
from PIL import ImageGrab
import numpy as np
import time

# Open the Camera
# cap = cv2.VideoCapture(0)
width = 800
height = 640
monitor = {"top": 80, "left": 0, "width": width, "height": height}
cords = {'top': 40, 'left': 0, 'width': 800, 'height': 640}
# sct = mss.mss()
sct = mss()
# sct = mss.mss().monitors[1]
# sct = mss.mss().monitors[1]
# sct.get_pixels(mon)
while True:
    # with mss.mss() as sct:
    #     monitor = sct.monitors[1]
    #     im = sct.grab(monitor)
    mss_screen_shot = sct.grab(monitor)
    mss_screen_shot_array = np.array(sct.grab(monitor))
    mss_screen_shot_asarray = np.asarray(sct.grab(monitor))
    print(f"mss_screen_shot type: {type(mss_screen_shot)}")
    print(f"mss_screen_shot: {mss_screen_shot}")
    print(f"mss_screen_shot_array type: {type(mss_screen_shot_array)}")
    print(f"mss_screen_shot_asarray type: {type(mss_screen_shot_asarray)}")
    time.sleep(1)
    break
    # mss_screen_shot.
    # with mss() as sct:
    #     img = np.array(sct.grab(cords))
    # sct = mss.mss()
    # img = np.array(mss.mss().grab(monitor))
    # mon = {"top": shape[0], "left": shape[1], "width": shape[2] - shape[1], "height": shape[3] - shape[0]}


    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()

    # Put current DateTime on each frame
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(img,str(datetime.now()),(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
    # Display the image
    # cv2.imshow('a',img)
    # wait for keypress
#     k = cv2.waitKey(10)
#     if k == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()


