import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


# 384, 128
# 3136, 3136
world_obstacles_array = np.load("world_array.npy")
grid = Grid(matrix=world_obstacles_array)

start = grid.node(2, 300)
end = grid.node(127, 0)

finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(start, end, grid)
print(path)
print('Path length:', len(path))
