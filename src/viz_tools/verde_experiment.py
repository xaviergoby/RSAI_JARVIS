import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Do this before importing pyplot!
import matplotlib.pyplot as plt
import verde as vd
from matplotlib.patches import Rectangle

# spacing = 100
spacing = 1
# west, east, south, north = 0, 1000, 0, 1000
west, east, south, north = 0, 64, 0, 64
region = (west, east, south, north)

# create the grid coordinates
easting, northing = vd.grid_coordinates(region=region, spacing=spacing)

def plot_region(ax, region):
    "Plot the region as a solid line."
    west, east, south, north = region
    ax.add_patch(
        plt.Rectangle((west, south), east, north, fill=None, label="Region Bounds")
    )


# def plot_grid(ax, coordinates, linestyles="dotted", region=None, pad=50, **kwargs):
def plot_grid(ax, coordinates, linestyles="dotted", region=None, pad=0.25, **kwargs):
    "Plot the grid coordinates as dots and lines."
    data_region = vd.get_region(coordinates)
    ax.vlines(
        coordinates[0][0],
        ymin=data_region[2],
        ymax=data_region[3],
        linestyles=linestyles,
        zorder=0,
    )
    ax.hlines(
        coordinates[1][:, 1],
        xmin=data_region[0],
        xmax=data_region[1],
        linestyles=linestyles,
        zorder=0,
    )
    ax.scatter(*coordinates, **kwargs)
    if pad:
        padded = vd.pad_region(region, pad=pad)
        plt.xlim(padded[:2])
        plt.ylim(padded[2:])


plt.figure(figsize=(6, 6))
ax = plt.subplot(111)
plot_region(ax=ax, region=region)
plot_grid(
    ax=ax,
    coordinates=(easting, northing),
    region=region,
    label="Square Region Grid Nodes",
    marker=".",
    color="black",
    s=100,
    pad=0.25
)

plt.xlabel("Easting")
plt.ylabel("Northing")
plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15))
plt.show()