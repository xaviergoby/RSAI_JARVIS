import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

img1 = cv2.imread(r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\research_and_dev\slam\altered_mm_img_52_52_45.PNG", 0)
img2 = cv2.imread(r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\research_and_dev\slam\altered_mm_img_52_52_46.PNG", 0)

diff12 = img1 - img2
diff21 = img2 - img1

im12 = Image.fromarray(diff12)
im21 = Image.fromarray(diff21)
im12.save("diff{2}_{0}_{1}.PNG".format(diff12.shape[0], diff12.shape[1], 12))
im21.save("diff{2}_{0}_{1}.PNG".format(diff21.shape[0], diff21.shape[1], 21))


# crop1 = img[23:26+1, 25:27+1]
# crop2 = img[22:26+2, 24:27+2]
# plt.imshow(img1, cmap='gray')
# plt.imshow(img2, cmap='gray')
plt.imshow(diff12, cmap='gray')
plt.title("diff12")
# plt.imshow(diff21, cmap='gray')
# plt.title("diff21")
# print(img[23, 25]) # 255
# print(img[23, 24]) # 255
# print(img[26, 27]) # 255
#
# print(img[23, 28]) # 0
# print(img[26, 28]) # 0
# print(img[24, 24]) # 0
#
# print("img[23:26+1, 25:27+1]: {0}".format(img[23:26+1, 25:27+1]))
# print("img[22:26+2, 24:27+2]: {0}".format(img[22:26+2, 24:27+2]))
#
plt.show()