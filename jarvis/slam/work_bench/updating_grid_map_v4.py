# https://stackoverflow.com/questions/34698864/count-frequencies-of-x-y-coordinates-display-in-2d-and-plot?noredirect=1&lq=1

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.table import Table

def table_plot(data):
	fig, ax = plt.subplots()
	ax.set_axis_off()
	
	tb = Table(ax, bbox=[0,0,1,1])
	
	nrows, ncols = data.shape
	width, height = 1.0 / ncols, 1.0 / nrows
	
	for (i, j), val in np.ndenumerate(data):
		tb.add_cell(i, j, width, height, text=str(val) if val else '', loc='center')
	
	for i in range(data.shape[0]):
		tb.add_cell(i, -1, width, height, text=str(i), loc='right',
		            edgecolor='none', facecolor='none')
	for i in range(data.shape[1]):
		tb.add_cell(-1, i, width, height/2, text=str(i), loc='center',
		            edgecolor='none', facecolor='none')
	
	tb.set_fontsize(16)
	ax.add_table(tb)
	return fig

coords = ((1,2), (2,5), (2,1), (4, 5), (5, 5))

# get maximum value for both x and y to allocate the array
x, y = map(max, zip(*coords))
data = np.zeros((x+1, y+1), dtype=int)

for i, j in coords:
	data[i,j] += 1


fig = table_plot(data)
plt.show()