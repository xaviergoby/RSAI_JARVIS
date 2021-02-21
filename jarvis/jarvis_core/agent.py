import queue


class Agent:

	def __init__(self):
		self.pos = None
		self._pos = None
		self.state = None
		self.main_map_tile_pos = None
		self.env_state = None




	# @property
	# def pos(self):
	# 	if self._pos is None and self.env_state is None:
	# 		return None
	# 	elif self._pos is None and self.env_state is not None:
	# 		return None
	# 	elif self._pos is not None and self.env_state is not None:
	#
	#
	# 	# :
	# 	# 	return self._pos
	#
	# def update_pos(self, pos):
	# 	pass
	#
	# def update_state(self, state):
	# 	pass
	#
	# def update_main_map_tile_pos(self):
	# 	pass
	#
	# def update_env_state(self, env_state):
	# 	self.env_state = queue.Queue()

