# https://python-mss.readthedocs.io/examples.html
import time

import cv2
import mss
import numpy



with mss.mss() as sct:
    # Part of the screen to capture
    # monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
    mss_sct_monitor_dims_dict = {'mon': 1, "top": 8, "left": 31, "width": 783, "height": 560}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        # img = numpy.array(sct.grab(monitor))
        img = numpy.array(sct.grab(mss_sct_monitor_dims_dict))

        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)
        # cv2.setWindowTitle("OpenCV/Numpy normal", f"fps: {(1 / (time.time() - last_time))}")

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

