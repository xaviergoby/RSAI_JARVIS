import numpy as np
import matplotlib.pyplot as plt


world_array = np.load("world_array.npy")
world_array2 = np.load("world_obstacles_array.npy")


plt.imshow(world_array2)
plt.show()
