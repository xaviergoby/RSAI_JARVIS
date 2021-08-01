import numpy as np
from abc import ABC, abstractmethod


# class ABCWorldMap:
class ABCWorldMap(ABC):


	# def __init__(self):
	def __init__(self, world_map_array, grid_labels):
		self.world_map_array = world_map_array
		self.grid_labels = grid_labels
		# super(ABCWorldMap, self).__init__()
	# self.data = np.zeros((10, 10))


	def __getitem__(self, key):
		return self.world_map_array[key]


	def __setitem__(self, key, value):
		self.world_map_array[key] = value


	def __repr__(self):
		return 'MyArray({})'.format(self.world_map_array)


	@property
	def shape(self):
		return self.world_map_array.shape


	@property
	@abstractmethod
	def grid_origin_world_coord(self):
		raise NotImplementedError


a = ABCWorldMap()

a[0, 0] = 1
print(f"a[0,0]: {a[0, 0]}")
print(a)
print(a.shape)
# a[:] = np.arange(10)
# print(a)
