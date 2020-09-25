from abc import ABC, abstractmethod
import numpy as np
from collections import OrderedDict



class ABCTaskHandler(ABC):


	@abstractmethod
	def update_task(self, *args, **kwargs):
		raise NotImplementedError

	@abstractmethod
	def start_task(self, *args, **kwargs):
		raise NotImplementedError

	@abstractmethod
	def stop_task(self, *args, **kwargs):
		raise NotImplementedError

	@abstractmethod
	def pause_task(self, *args, **kwargs):
		raise NotImplementedError

