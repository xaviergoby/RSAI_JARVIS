# NOTE:
# THIS SCRIPT IS THE EXACT SAME ONE AS LOCATED AT:
# research_and_dev\event_driven_system\actuators\hw_event_handler.py

import settings
from src.ui_automation_tools import mouse_events_monitoring
from src.ui_automation_tools import keyboard_events_monitoring
from src.utils import time_tools


class HardWareStatesListener:


	def __init__(self, mouse_buttons_2_monitor=["LMB"],
	             keyboard_keys_2_monitor=list(settings.keyboard_nVirtKey_dict.keys())):
		self.mouse_buttons_2_monitor = mouse_buttons_2_monitor
		self.keyboard_keys_2_monitor = keyboard_keys_2_monitor
		self.current_mouse_states = None
		self.current_keyboard_states = None

	def init_mouse_states(self):
		init_mouse_states = mouse_events_monitoring.get_init_mouse_states(settings.mouse_nVirtKey_dict)
		self.current_mouse_states = init_mouse_states

	def init_keyboard_states(self):
		init_keyboard_states = keyboard_events_monitoring.get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
		self.current_keyboard_states = init_keyboard_states

	def init_all_states(self):
		self.init_mouse_states()
		self.init_keyboard_states()

	def get_mouse_states_change_events(self):
		mouse_states_change_events = mouse_events_monitoring.get_mouse_click_events(self.current_mouse_states,
		                                                                            settings.mouse_nVirtKey_dict)
		return mouse_states_change_events

	@property
	def lmb_clicked(self):
		mouse_states_change_events = self.get_mouse_states_change_events()
		lmb_clicked = mouse_events_monitoring.mouse_button_clicked(mouse_states_change_events,
		                                                           self.mouse_buttons_2_monitor)
		if lmb_clicked is True:
			return True
		else:
			return False

	def get_keyboard_states_change_events(self):
		keyboard_states_change_events = keyboard_events_monitoring.get_keyboard_click_events(self.current_keyboard_states,
		                                                                                     settings.keyboard_nVirtKey_dict)
		return keyboard_states_change_events

	@property
	def P_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		p_clicked = keyboard_events_monitoring.keyboard_key_clicked(keyboard_states_change_events, ["P"])
		if p_clicked is True:
			return True
		else:
			return False

	@property
	def T_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		t_clicked = keyboard_events_monitoring.keyboard_key_clicked(keyboard_states_change_events, ["T"])
		if t_clicked is True:
			return True
		else:
			return False

	@property
	def keyboard_clicked(self):
		P_clicked = self.P_clicked
		T_clicked = self.P_clicked
		if P_clicked is True or T_clicked is True:
			return True
		else:
			return False


	def update_current_mouse_states(self):
		old_mouse_states = self.current_mouse_states
		mouse_click_events = self.get_mouse_states_change_events()
		new_mouse_states = mouse_events_monitoring.update_mouse_states(old_mouse_states, mouse_click_events)
		self.current_mouse_states = new_mouse_states

	def update_current_keyboard_states(self):
		old_keyboard_states = self.current_keyboard_states
		keyboard_click_events = self.get_keyboard_states_change_events()
		new_keyboard_states = keyboard_events_monitoring.update_keyboard_states(old_keyboard_states, keyboard_click_events)
		self.current_keyboard_states = new_keyboard_states

	def update_all_states(self):
		self.update_current_mouse_states()
		self.update_current_keyboard_states()



if __name__ == "__main__":
	l = HardWareStatesListener()
	time_tools.delay_timer(3)
	l.init_all_states()
	while True:
		if l.lmb_clicked is True:
			print("LMB Clicked")
		elif l.P_clicked is True:
			print("P Key Clicked")
		elif l.T_clicked is True:
			print("T Key Clicked")
		else:
			continue
		l.update_all_states()
