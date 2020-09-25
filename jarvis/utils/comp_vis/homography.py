## https://zbigatron.com/mapping-camera-coordinates-to-a-2d-floor-plan/

import cv2  # import the OpenCV library
import numpy as np  # import the numpy library

# provide points from image 1

pts_src = np.array([[154, 174], [702, 349], [702, 572], [1, 572], [1, 191]])
# corresponding points from image 2 (i.e. (154, 174) matches (212, 80))
pts_dst = np.array([[212, 80], [489, 80], [505, 180], [367, 235], [144, 153]])

# calculate matrix H
h, status = cv2.findHomography(pts_src, pts_dst)

# provide a point you wish to map from image 1 to image 2
a = np.array([[154, 174]], dtype='float32')
a = np.array([a])

# finally, get the mapping
pointsOut = cv2.perspectiveTransform(a, h)

from research_and_dev.rsai_cv_navigability_mapping.world_maps.world_map import WorldMap
import numpy as np

top_left_origin_world_coords = (3136, 3519)
world_obstacles_array = np.load("world_array.npy")
world_map = WorldMap(world_obstacles_array, top_left_origin_world_coords)

start_coords = (3216, 3219)
end_coord1 = (3217, 3219)
end_coord2 = (3216, 3220)
end_coord3 = (3216, 3218)
end_coord4 = (3215, 3219)

px_coords = world_map.get_target_tile_lmc_rand_coords(start_coords, start_coords)
px_coords1 = world_map.get_target_tile_lmc_rand_coords(start_coords, end_coord1)
px_coords2 = world_map.get_target_tile_lmc_rand_coords(start_coords, end_coord2)
px_coords3 = world_map.get_target_tile_lmc_rand_coords(start_coords, end_coord3)
px_coords4 = world_map.get_target_tile_lmc_rand_coords(start_coords, end_coord4)
print(px_coords)
print(px_coords1)
print(px_coords2)
print(px_coords3)
print(px_coords4)


from numpy.linalg import inv


def toworld(x, y, inverse_homography_matrix):
	imagepoint = [x, y, 1]
	worldpoint = np.array(np.dot(inverse_homography_matrix, imagepoint))
	scalar = worldpoint[2]
	xworld = worldpoint[0] / scalar
	yworld = worldpoint[1] / scalar
	return xworld, yworld



pts_src = np.array([[3216, 3219], [3217, 3219], [3216, 3220], [3216, 3218], [3215, 3219]])
# corresponding points from image 2 (i.e. (154, 174) matches (212, 80))
pts_dst = np.array([[px_coords[0], px_coords[1]], [px_coords1[0], px_coords1[1]],
                    [px_coords2[0], px_coords2[1]], [px_coords3[0], px_coords3[1]],
                    [px_coords4[0], px_coords4[1]]])

# calculate matrix H
h, status = cv2.findHomography(pts_src, pts_dst)

inverse_homography_matrix = inv(h)

test_coords = (3220, 3219)
px_test_coords = world_map.get_target_tile_lmc_rand_coords(start_coords, test_coords)
print(px_test_coords)
test_world_coords = toworld(test_coords[0], test_coords[1], inverse_homography_matrix)
print(f"test_world_coords: {test_world_coords}")

a = np.array([[px_test_coords[0], px_test_coords[1]]], dtype='float32')
a = np.array([a])
print(f"a: {a}")

# finally, get the mapping
test_world_coords = cv2.perspectiveTransform(a, h)
print(f"test_world_coords: {test_world_coords}")








