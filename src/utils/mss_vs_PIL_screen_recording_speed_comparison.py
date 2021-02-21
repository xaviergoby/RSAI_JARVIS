import time

import cv2
import mss
import numpy


def screen_record():
    try:
        from PIL import ImageGrab
    except ImportError:
        return 0

    # 800x600 windowed mode
    mon = (0, 40, 800, 640)

    title = "[PIL.ImageGrab] FPS benchmark"
    fps = 0
    last_time = time.time()

    while time.time() - last_time < 1:
    # while True:
        img = numpy.array(ImageGrab.grab(bbox=mon))
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        fps += 1

        cv2.imshow(title, rgb_img)
        # cv2.imshow(title, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # pil_img = img
            # print(f"PIL img type: {type(pil_img)}")
            # print(f"PIL img shape: {pil_img.shape}")
            # print(f"PIL img: {pil_img}")
            cv2.destroyAllWindows()
            break
    pil_img = rgb_img
    print(f"PIL img type: {type(pil_img)}")
    print(f"PIL img shape: {pil_img.shape}")
    print(f"PIL img: {pil_img}")
    return fps, pil_img


def screen_record_efficient():
    # 800x600 windowed mode
    mon = {"top": 40, "left": 0, "width": 800, "height": 640}

    title = "[MSS] FPS benchmark"
    fps = 0
    sct = mss.mss()
    last_time = time.time()

    while time.time() - last_time < 1:
    # while True:
        img = numpy.array(sct.grab(mon))
        # rgb_img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        bgr_img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        fps += 1

        cv2.imshow(title, rgb_img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            # mss_img = img
            # print(f"mss img type: {type(mss_img)}")
            # print(f"mss img shape: {mss_img.shape}")
            # print(f"mss img: {mss_img}")
            cv2.destroyAllWindows()
            break

    mss_img = rgb_img
    print(f"mss img type: {type(mss_img)}")
    print(f"mss img shape: {mss_img.shape}")
    print(f"mss img: {mss_img}")
    return fps, mss_img

pil_fps, PIL_img = screen_record()
mss_fps, mss_img = screen_record_efficient()
import random
rand_idx_int = random.randint(0,100)
print(f"PIL FPS: {pil_fps}")
print(f"MSS FPS: {mss_fps}")
print(f"PIL img val @ random int idx {rand_idx_int}: {PIL_img[rand_idx_int]}")
print(f"MSS img val @ random int idx {rand_idx_int}: {mss_img[rand_idx_int]}")