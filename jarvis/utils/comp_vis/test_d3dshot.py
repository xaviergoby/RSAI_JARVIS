import d3dshot
import time
from PIL import Image
# im = Image.open('image.jpg')
import tkinter as tk
from PIL import Image, ImageTk
window = tk.Tk()
d = d3dshot.create()
# d.capture(region=(8, 31, 791, 591))
d.screenshot_every(1, region=(8, 31, 791, 591))
# time.sleep(1)
# d.stop()


while True:
	time.sleep(1)
	res = d.get_latest_frame()
	img = ImageTk.PhotoImage(res)
	lbl = tk.Label(window, image = img).pack()
	window.mainloop()
	


# res.show()
#
#
#
# import tkinter as tk
# from PIL import Image, ImageTk  # Place this at the end (to avoid any conflicts/errors)
#
# window = tk.Tk()
# #window.geometry("500x500") # (optional)
# # imagefile = {path_to_your_image_file}
# img = ImageTk.PhotoImage(res)
# lbl = tk.Label(window, image = img).pack()
# window.mainloop()
#
#
# d.screenshot_every(1)