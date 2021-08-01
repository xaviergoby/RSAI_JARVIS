import numpy as np




class MetaArray(np.ndarray):
	"""Array with metadata."""

	def __new__(cls, array, dtype=None, order=None, **kwargs):
		obj = np.asarray(array, dtype=dtype, order=order).view(cls)
		obj.metadata = kwargs
		return obj

	def __array_finalize__(self, obj):
		if obj is None:
			self.metadata = getattr(obj, 'metadata', None)


# a = MetaArray([1,2,3], comment='/Documents/Data/foobar.txt')
# np.save("array_with_meta_data", a, allow_pickle=False)
# print(a.metadata)

meta_data_array_path = r"C:\Users\Xavier\PycharmProjects\VideoClassificationAndVisualNavigationViaRepresentationLearning\research_and_dev\rsai_cv_navigability_mapping\misc\single_grid_world_map.py"
metadata_array = np.load(meta_data_array_path, )
print(metadata_array.metadata)
print(metadata_array.metadata)
