import settings
from research_and_dev.event_driven_system.actuators import mouse_event_handler
from research_and_dev.event_driven_system.actuators import keyboard_event_handler
from src.utils import time_tools
import pyautogui


class Actuators:
	
	def __init__(self, mouse_buttons_2_monitor=settings.mouse_nVirtKey_dict_keys,
	             keyboard_keys_2_monitor=settings.keyboard_nVirtKey_dict_keys):
		self.mouse_buttons_2_monitor = mouse_buttons_2_monitor
		self.keyboard_keys_2_monitor = keyboard_keys_2_monitor
		self.current_mouse_states = None
		self.current_keyboard_states = None
	
	def init_mouse_states(self):
		init_mouse_states = mouse_event_handler.get_init_mouse_states(settings.mouse_nVirtKey_dict)
		self.current_mouse_states = init_mouse_states
	
	def init_keyboard_states(self):
		init_keyboard_states = keyboard_event_handler.get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
		self.current_keyboard_states = init_keyboard_states
	
	def init_all_states(self):
		self.init_mouse_states()
		self.init_keyboard_states()
	
	def get_mouse_states_change_events(self):
		mouse_states_change_events = mouse_event_handler.get_mouse_click_events(self.current_mouse_states,
		                                                                        settings.mouse_nVirtKey_dict)
		return mouse_states_change_events
	
	@property
	def lmb_clicked(self):
		mouse_states_change_events = self.get_mouse_states_change_events()
		lmb_clicked = mouse_event_handler.mouse_button_clicked(mouse_states_change_events,
		                                                       self.mouse_buttons_2_monitor)
		if lmb_clicked is True:
			###
			self.lmb_clicked_screen_px_coords = pyautogui.position()
			###
			return True
		else:
			return False

	###
	def get_lmb_clicked_screen_px_coords(self):
		return self.lmb_clicked_screen_px_coords
	###

	def get_keyboard_states_change_events(self):
		keyboard_states_change_events = keyboard_event_handler.get_keyboard_click_events(self.current_keyboard_states,
		                                                                                 settings.keyboard_nVirtKey_dict)
		return keyboard_states_change_events
	
	@property
	def P_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		p_clicked = keyboard_event_handler.keyboard_key_clicked(keyboard_states_change_events, ["P"])
		if p_clicked is True:
			return True
		else:
			return False
	
	@property
	def T_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		t_clicked = keyboard_event_handler.keyboard_key_clicked(keyboard_states_change_events, ["T"])
		if t_clicked is True:
			return True
		else:
			return False
	
	@property
	def C_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		c_clicked = keyboard_event_handler.keyboard_key_clicked(keyboard_states_change_events, ["C"])
		if c_clicked is True:
			return True
		else:
			return False
		
	@property
	def I_clicked(self):
		keyboard_states_change_events = self.get_keyboard_states_change_events()
		i_clicked = keyboard_event_handler.keyboard_key_clicked(keyboard_states_change_events, ["I"])
		if i_clicked is True:
			return True
		else:
			return False
	
	@property
	def keyboard_clicked(self):
		P_clicked = self.P_clicked
		T_clicked = self.T_clicked
		C_clicked = self.C_clicked
		I_clicked = self.I_clicked
		if P_clicked is True or T_clicked is True or C_clicked is True or I_clicked is True:
			return True
		else:
			return False
	
	def update_current_mouse_states(self):
		old_mouse_states = self.current_mouse_states
		mouse_click_events = self.get_mouse_states_change_events()
		new_mouse_states = mouse_event_handler.update_mouse_states(old_mouse_states, mouse_click_events)
		self.current_mouse_states = new_mouse_states
	
	def update_current_keyboard_states(self):
		old_keyboard_states = self.current_keyboard_states
		keyboard_click_events = self.get_keyboard_states_change_events()
		new_keyboard_states = keyboard_event_handler.update_keyboard_states(old_keyboard_states, keyboard_click_events)
		self.current_keyboard_states = new_keyboard_states
	
	def update_all_states(self):
		self.update_current_mouse_states()
		self.update_current_keyboard_states()


if __name__ == "__main__":
	l = Actuators()
	time_tools.delay_timer(3)
	l.init_all_states()
	while True:
		if l.lmb_clicked is True:
			print("LMB Clicked")
		elif l.P_clicked is True:
			print("P Key Clicked")
		elif l.T_clicked is True:
			print("T Key Clicked")
		elif l.C_clicked is True:
			print("C Key Clicked")
		elif l.I_clicked is True:
			print("I Key Clicked")
		else:
			continue
		l.update_all_states()
