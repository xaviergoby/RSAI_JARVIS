from abc import abstractmethod
import settings
import os
from research_and_dev.end2end_nav.handlers import nav_grid_handler
# research_and_dev/end2end_nav/screen_casters/abc_screen_caster_class.py
from research_and_dev.end2end_nav.screen_casters.abc_screen_caster_class import ABCScreenCaster


class E2EScreenCaster(ABCScreenCaster):

	main_data_storage_dir_name = "end_2_end_slam_data"

	def __init__(self, keyboard_keys_2_monitor_list, mesh_grid_opt_num=1, data_storage_dir_name="test_run_data"):
		super().__init__(keyboard_keys_2_monitor_list)
		self.keyboard_keys_2_monitor_list = keyboard_keys_2_monitor_list
		self.grid_opt_num = mesh_grid_opt_num
		self.data_storage_dir_name = data_storage_dir_name
		self.data_storage_dir = None

		# self.data_storage_dir = os.path.join(settings.DATA_DIR, r"{0}\{1}".format(self.main_data_storage_dir_name,
		#                                                                           self.data_storage_dir_name))

	def p_keyboard_key_action(self):
		super().p_keyboard_key_action()
	# pass

	def t_keyboard_key_action(self):
		super().t_keyboard_key_action()

	def lmc_action(self):
		super().lmc_action()

	def set_current_mouse_states(self, mouse_states):
		super().current_mouse_states = mouse_states

	def set_current_keyboard_states(self, keyboard_states):
		super().set_current_keyboard_states = keyboard_states

	@abstractmethod
	def set_data_storage_dir(self):
		self.data_storage_dir = os.path.join(settings.DATA_DIR, r"{0}\{1}".format(self.main_data_storage_dir_name,
		                                                                          self.data_storage_dir_name))

	def __set_grid_handler(self):
		self.grid_handler = nav_grid_handler.NavigationGridHandler(settings.MESH_GRID_OPTIONS[self.grid_opt_num])

	def set_handler(self):
		self.__set_grid_handler()

	def pre_screen_casting_setup(self):
		super().pre_screen_casting_setup()

	def start_screen_casting(self, roi):
		# mgrid = env_grid_handler.GridHandler(settings.MESH_GRID_OPTIONS[self.grid_opt_num])
		super().start_screen_casting(roi)


if __name__ == "__main__":
	# abc = ABCScreenCaster()
	keyboard_keys_2_monitor = ["P", "T"]
	e2e = E2EScreenCaster(keyboard_keys_2_monitor)
	print(e2e.keyboard_keys_2_monitor_list)
	print(e2e.paused)
	print("\nSimulating P keyboard key click event response action:")
	e2e.p_keyboard_key_action()
	print("\nPost P keyboard key click event response action:")
	print(e2e.paused)