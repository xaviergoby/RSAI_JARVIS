import cv2
import matplotlib.pyplot as plt
import numpy as np


# frame_file_path = r"/jarvis/tests/mining_with_obj_dect_sys.PNG"
frame_file_path = r"C:\Users\Xavier\RSAI_JARVIS\jarvis\tests\mining_with_obj_dect_sys.PNG"
frame = cv2.imread(frame_file_path, cv2.IMREAD_UNCHANGED)


frame_width = frame.shape[1]
frame_height = frame.shape[0]

# frame_width = 783
# frame_height = 560
# frame centre in local crs:
	# x = col j = 

frame_shape = np.array([frame_width, frame_height])

print(f"frame_width: {frame_width}")
print(f"frame_height: {frame_height}")


fx_cent = int((frame_width+1)/2)
fy_cent = int(frame_height/2)

fc = np.array([fx_cent, fy_cent])

print(f"fxc: {fx_cent}")
print(f"fyc: {fy_cent}")

# obj1_t1_cent = (347, 350)
# obj2_t1_cent = (285, 480)

obj1_t1_cent = np.array([347, 350])
obj2_t1_cent = np.array([285, 480])

# Calculate the magnitude of the distance between the centre of the frame and obj1 and obj2
# obj1_t1_ds_2_fc = (obj1_t1_cent[0] - fx_cent, obj1_t1_cent[1] - fy_cent)
# obj2_t1_ds_2_fc = (obj2_t1_cent[0] - fx_cent, obj2_t1_cent[1] - fy_cent)

obj1_t1_ds_2_fc = obj1_t1_cent - fc
obj2_t1_ds_2_fc = obj2_t1_cent - fc

print(f"obj1_t1_ds_2_fc: {obj1_t1_ds_2_fc}")
print(f"obj2_t1_ds_2_fc: {obj2_t1_ds_2_fc}")

# compute the location of obj1 and obj2 w.r.t to the centre of the frame
# obj1_t1_cent_wrt_fc = (fx_cent + obj1_t1_ds_2_fc[0], fy_cent + obj1_t1_ds_2_fc[1])
# obj2_t1_cent_wrt_fc = (fx_cent + obj2_t1_ds_2_fc[0], fy_cent + obj2_t1_ds_2_fc[1])

obj1_t1_cent_wrt_fc = fc + obj1_t1_ds_2_fc
obj2_t1_cent_wrt_fc = fc + obj2_t1_ds_2_fc

print(f"*** obj1_t1_cent_wrt_fc: {obj1_t1_cent_wrt_fc}")
print(f"*** obj2_t1_cent_wrt_fc: {obj2_t1_cent_wrt_fc}")

# plt.imshow(frame, cmap='gray')
# plt.title("frame screen shot")
# plt.show()

obj1_t2_cent = np.array([347 + 25, 350 + 32])
obj2_t2_cent = np.array([285 + 25, 480 + 32])

obj1_t2_ds_2_fc = obj1_t2_cent - fc
obj2_t2_ds_2_fc = obj2_t2_cent - fc

print(f"obj1_t2_ds_2_fc: {obj1_t2_ds_2_fc}")
print(f"obj2_t2_ds_2_fc: {obj2_t2_ds_2_fc}")

obj1_t2_cent_wrt_fc = fc + obj1_t2_ds_2_fc
obj2_t2_cent_wrt_fc = fc + obj2_t2_ds_2_fc

print(f"*** obj1_t2_cent_wrt_fc: {obj1_t2_cent_wrt_fc}")
print(f"*** obj2_t2_cent_wrt_fc: {obj2_t2_cent_wrt_fc}")

# bot_tot_px_displacement = obj2_t2_cent_wrt_fc - obj2_t1_cent_wrt_fc
bot_tot_px_displacement = obj1_t2_cent_wrt_fc - obj1_t1_cent_wrt_fc
equal_tot_bot_px_ds_2_objs = bot_tot_px_displacement == bot_tot_px_displacement
print("equal tot bot px ds between all objs?: {0}".format(equal_tot_bot_px_ds_2_objs))

ds_magnitude = np.sqrt(bot_tot_px_displacement[0]**2+bot_tot_px_displacement[1]**2)