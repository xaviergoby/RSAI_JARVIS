from abc import ABC, abstractmethod


class ObjDectABCDataCollector(ABC):
	
	@abstractmethod
	def _get_num_of_rgb_images(self):
		raise NotImplementedError
	
	@abstractmethod
	def _get_num_of_grey_images(self):
		raise NotImplementedError
	
	@abstractmethod
	def _get_num_of_npy_arrays(self):
		raise NotImplementedError
	
	# @property
	# @abstractmethod
	# def tot_num_rgb_images(self):
	# 	return self._get_num_of_rgb_images()
	#
	# @property
	# @abstractmethod
	# def tot_num_grey_images(self):
	# 	return self._get_num_of_grey_images()
	#
	# @property
	# @abstractmethod
	# def tot_num_npy_arrays(self):
	# 	return self._get_num_of_npy_arrays()
	
	@abstractmethod
	def run_data_collector(self):
		raise NotImplementedError

