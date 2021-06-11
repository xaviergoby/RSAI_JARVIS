import cv2
import numpy as np
from matplotlib import pyplot as plt


def img_navigability_mapper(img_array, tile_pixels_path_size):
	# --> Load image
	# img = cv2.imread('Obstacle_image.png', cv2.IMREAD_UNCHANGED)
	img = img_array
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# --> Filter image colors
	# Create Walls/icon mask
	water_low = np.asarray([0, 0, 150])
	walls_high = np.asarray([150, 150, 255])

	mask_walls = cv2.inRange(img_hsv, water_low, walls_high)

	# Create Water mask
	water_low = np.asarray([50, 50, 50])
	water_high = np.asarray([118, 143, 193])

	mask_water = cv2.inRange(img_hsv, water_low, water_high)

	# --> Add masks
	mask = cv2.bitwise_or(mask_walls, mask_water)

	# cv2.imshow("mask", mask)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# --> Set obstacles to 1 and rest to 0 on mask
	mask[mask == 0] = 0
	mask[mask == 255] = 1

	# --> Reduce mask to world scale
	# chunk_size = 8
	chunk_size = tile_pixels_path_size
	horizontal_chunk_count = int(mask.shape[0] / chunk_size)
	vertical_chunk_count = int(mask.shape[0] / chunk_size)

	world_obstacles_array = np.ones((horizontal_chunk_count, vertical_chunk_count))

	print(world_obstacles_array)

	# -> Iterate through chucks
	for chunk_x in range(horizontal_chunk_count):
		for chunk_y in range(vertical_chunk_count):
			obstacle_counter = 0

			# --> Iterate inside chunk
			for row in range(chunk_size):
				for column in range(chunk_size):
					if mask[(chunk_x * chunk_size) + row][(chunk_y * chunk_size) + column] == 1:
						obstacle_counter += 1
					else:
						pass

			if obstacle_counter >= chunk_size:
				world_obstacles_array[chunk_x][chunk_y] = 0

	np.save("world_map_array", world_obstacles_array)

	return world_obstacles_array


if __name__ == "__main__":
	img_file_name = '12850.png'
	tile_pixels_path_size = 4
	img_array = cv2.imread(img_file_name, cv2.IMREAD_UNCHANGED)
	navigability_mapped_img_array = img_navigability_mapper(img_array, tile_pixels_path_size)
	wndw_name = img_file_name.split(".")[0]
	cv2.imshow(wndw_name, navigability_mapped_img_array)
	cv2_close_key = cv2.waitKey(0) & 0xFF
	if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
		cv2.waitKey(0)
		cv2.destroyAllWindows()
# cv2.waitKey(0)
# cv2.destroyAllWindows()
