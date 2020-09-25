# import matplotlib
# matplotlib.use('module://backend_interagg')
# local_x = list(range(0, 100))
# local_y = list(range(0, 100))
# import matplotlib.pyplot as plt
# plt.plot(local_x, local_y)
# plt.show()s

import cv2

modes = {-1:"unchanged", 0:"grayscale", 1:"colour"}
mode = 0
mode_txt = modes[mode]
img = cv2.imread('test_mm_screen_shot.PNG',mode)
ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
print(img.shape)

import matplotlib
matplotlib.use('module://backend_interagg')
import matplotlib.pyplot as plt

edges = cv2.Canny(img,100,200)

crop = thresh1[30:50,30:50]
crop = thresh1[35:45,35:45]
plt.imshow(thresh1)
# plt.imshow(edges,cmap = 'gray')
plt.show()


# cv2.imshow('mode: {0}'.format(mode_txt), img)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.destroyAllWindows()



