
import pandas as pd
import os

class CollectAndMergeSeriesFeatures:

	def __init__(self, *args, **kwargs):
		self.CWD_PATH = os.getcwd()
		for arg in args:
			try:
				iterator = iter(arg)
			except TypeError: # not an iterable
				print(f"The input {arg} is not an iterable")
			# not iterable
			else: # iterable
				for key in arg:
					setattr(self, key, arg[key])
		for key in kwargs:
			if isinstance(kwargs[key], dict):
				print(type(kwargs[key]))
				for dict_key in kwargs[key].keys():
					setattr(self, dict_key, kwargs[key][dict_key])
			else:
				pass
			
		
		# for arg in args:
		# 	try:
		# 		iterator = iter(arg)
		# 	except TypeError: # not an iterable
		# 		print(f"The input {arg} is not an iterable")
		# 	# not iterable
		# 	else: # iterable
		# 		for key in arg:
		# 			setattr(self, key, arg[key])
					
		# self.features_df = self.get_features_df()

	def __str__(self):
		meta_info = "The features contained within this CollectAndMergeSeriesFeatures obj instance are: {0}".format(self.features_names_list)
		return meta_info

	# def _create_features_dict(self):
	# 	features_dict = {}
	# 	for f in self.features_names_list:
	# 		feature = self.__dict__.get(f, None)
	# 		print(feature)
	# 		features_dict[f] = feature
	# 	return features_dict
	#
	# def _set_features_dict(self):
	# 	features_dict = self._create_features_dict()
	# 	self.features_dict = features_dict


if __name__ == "__main__":
	from sys_settings.obj_dect_settings_opts import OBJ_DECT_SETTINGS
	import os
	import sys
	# sys.path.append("..")
	CWD_PATH = os.getcwd()
	print(CWD_PATH)
	# d = {"name": "John", "surname": "Doe"}
	res = CollectAndMergeSeriesFeatures(settings = OBJ_DECT_SETTINGS["task"]["cow_slaying"])