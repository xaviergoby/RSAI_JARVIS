import itertools
import matplotlib
matplotlib.use("TkAgg")  # Do this before importing pyplot!
import matplotlib.pyplot as plt
import numpy as np
import settings



# Get "Old School RuneScape": {"left": 8, "top": 31 ,"right": 791, "bottom": 591}
env_screen_region_pos_and_size = settings.GAME_CLIENT_BOUNDING_REGION_PX_COORDS_DICT[settings.GAME_WNDW_NAME]
x_left = env_screen_region_pos_and_size["left"]
y_top = env_screen_region_pos_and_size["top"]
x_right = env_screen_region_pos_and_size["right"]
y_bottom = env_screen_region_pos_and_size["bottom"]

# x_px_coords = np.arange(x_left, x_right+1, 1)
# x_px_coords = np.linspace(x_left, x_right+1, 16)
x_px_coords = np.array([320, 360, 400, 440, 480])
# y_px_coords = np.arange(y_top, y_bottom+1, 1)
# y_px_coords = np.linspace(y_top, y_bottom+1, 12)
y_px_coords = np.array([220, 260, 300, 340, 380])

x_mesh_px_coords = np.arange(8, 792+1, 784//16)
y_mesh_px_coords = np.arange(31, 591+1, 588//14)
# y_mesh_px_coords = np.arange(31, 588+1, 588//14)
mesh_grid_points_coords = list(itertools.product(x_px_coords, y_px_coords))
# mesh_grid_points_coords = list(itertools.product(x_px_coords, y_px_coords))
mesh_grid_points_coords_array = np.asarray(mesh_grid_points_coords)
# mesh_grid_points_coords_array = np.asarray(mesh_grid_points_coords)
# plt.plot(mesh_grid_points_coords_array[:,0], mesh_grid_points_coords_array[:,1])
# plt.plot(mesh_grid_points_coords_array[:,0], mesh_grid_points_coords_array[:,1], 'o', markersize=5)
# plt.scatter(x_px_coords, y_px_coords)
# plt.show()
fig, ax = plt.subplots()
ax.plot(mesh_grid_points_coords_array[:,0], mesh_grid_points_coords_array[:,1], 'o', markersize=5)
# ax.scatter(x_coords, y_coords)
ax.xaxis.tick_top()
ax.invert_yaxis()
ax.set_xlim(left=8, right=791)
ax.set_ylim(bottom=591, top=31)
plt.grid(True)
# plt.grid(b=True, which='minor', color='r', linestyle='--')
plt.show()
