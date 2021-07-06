import cv2
import numpy as np

# img = cv2.imread('cnt_num_rand_objs_in_img_test_img.PNG')
img = cv2.imread('cnt_num_rand_objs_in_img_test_img_2.PNG')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# _, thresh = cv2.threshold(img, 225, 255, cv2.THRESH_BINARY_INV)
# _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
_, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)
# _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
kernal = np.ones((2, 2), np.uint8)

# dilation = cv2.dilate(thresh, kernal, iterations=2)
dilation = cv2.dilate(thresh, kernal, iterations=5)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

objects = str(len(contours))
print(f"Number of detected objects counted: {objects}")

text = "Obj:" + str(objects)
cv2.putText(dilation, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (240, 0, 159), 1)

cv2.imshow('Original', img)
cv2.imshow('Thresh', thresh)
cv2.imshow('Dilation', dilation)

cv2.waitKey(0)
cv2.destroyAllWindows()
