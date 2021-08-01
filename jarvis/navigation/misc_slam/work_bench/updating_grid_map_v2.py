# https://stackoverflow.com/questions/55517072/python-plotting-grid-based-on-values?noredirect=1&lq=1

import numpy as np
import matplotlib.pyplot as plt

nrows = 10
ncols = 10

Cellid = [2, 4 ,5, 11 ,45 ,48 ,98]
Cellval = [20, 45 ,55, 77,45 ,30 ,15]

data = np.zeros(nrows*ncols)
data[Cellid] = Cellval
data = np.ma.array(data.reshape((nrows, ncols)), mask=data==0)

fig, ax = plt.subplots()
ax.imshow(data, cmap="Greens", origin="lower", vmin=0)

# optionally add grid
ax.set_xticks(np.arange(ncols+1)-0.5, minor=True)
ax.set_yticks(np.arange(nrows+1)-0.5, minor=True)
ax.grid(which="minor")
ax.tick_params(which="minor", size=0)

plt.show()