import numpy as np




class NavigabilityMap:


	def __init__(self, navigability_array):
		self.navigability_array = navigability_array


	def __getitem__(self, key):
		print(key)
		print(type(key))
		return self.navigability_array[key]


	def __setitem__(self, key, value):
		self.navigability_array[key] = value


	def __repr__(self):
		return 'MyArray({})'.format(self.navigability_array)

if __name__ == "__main__":
	zeros_array = np.zeros((32, 32))
	nav_map = NavigabilityMap(zeros_array)
	print(nav_map[0,0])