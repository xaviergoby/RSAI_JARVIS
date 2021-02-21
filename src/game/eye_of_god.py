# "C:\Users\XGOBY\RSAIBot\src\game\wc_obj_dect_3.jpg"
# "wc_obj_dect_3.jpg"
# "wc_obj_dect_3_TLC.jpg"
# "wc_obj_dect_3_LVUPEV.jpg"
# "RMB_tooltip.png"

from PIL import Image
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
fac = 3
# Simple image to string
file_name = "wc_obj_dect_3_TLC2.jpg"
img = Image.open(file_name)
img = cv2.imread("wc_obj_dect_3_TLC.jpg")
print("Type pre resizing: {0}".format(type(img)))
# img = cv2.imread("wc_obj_dect_3_TLC2.jpg", cv2.IMREAD_UNCHANGED)
img = cv2.resize(img,(0,0),fx=fac,fy=fac)
print("Type post resizing: {0}".format(type(img)))
# print(pytesseract.image_to_string(Image.open(file_name)))
txt = pytesseract.image_to_string(img, lang="eng")
# txt = pytesseract.image_to_string(img, config='--psm 10', lang="eng")
# txt = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789', lang='eng')
print("enlargement factor: {0}".format(fac))
print(txt)

# im = Image.open("wc_obj_dect_3_TLC2.jpg") # the second one
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# im.save("wc_obj_dect_3_TLC2_2.jpg")
# obj_id_info = pytesseract.image_to_string(Image.open("wc_obj_dect_3_TLC2_2.jpg"))
# print(obj_id_info)


# def ocr_core(filename):
#     obj_id_info = pytesseract.image_to_string(Image.open(filename))
#     return obj_id_info

# print(ocr_core("wc_obj_dect_3_TLC.jpg"))