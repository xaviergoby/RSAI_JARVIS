# NOTE:
# THIS SCRIPT IS THE EXACT SAME ONE AS LOCATED AT:
# src\ui_automation_tools\keyboard_events_monitoring.py
# and located at:
# research_and_dev\event_driven_system\actuators\keyboard_event_handler.py

import win32api
import settings


def get_init_keyboard_states(keyboard_nVirtKey_dict, set_key_states=None):
	init_states_nVirtKey_dict = {}
	for key_state, hex_dec_val in keyboard_nVirtKey_dict.items():
		init_states_nVirtKey_dict[key_state] = win32api.GetKeyState(hex_dec_val)
	return init_states_nVirtKey_dict


def get_keyboard_click_event(init_state, keyboard_hex_dec_val):
	current_state = win32api.GetKeyState(keyboard_hex_dec_val)
	if init_state != current_state:
		if current_state not in [-128, -127]:
			new_init_state = current_state
			return new_init_state
		elif current_state in [-128, -127]:
			return False
	elif init_state == current_state:
		return False


def get_keyboard_click_events(init_states_keyboard_nVirtKey_dict, keyboard_nVirtKey_dict):
	click_events_dict = {}
	for key_charac_str, init_key_state in init_states_keyboard_nVirtKey_dict.items():
		key_code_dec = keyboard_nVirtKey_dict[key_charac_str]
		click_event = get_keyboard_click_event(init_key_state, key_code_dec)
		click_events_dict[key_charac_str] = click_event
	return click_events_dict


def keyboard_key_clicked(keyboard_click_events, keyboard_key=None):
	clicked = False
	if keyboard_key is not None:
		for keyboard_key_charac in keyboard_key:
			if keyboard_click_events[keyboard_key_charac] is not False:
				clicked = True
				return clicked
			else:
				pass
		return clicked
	elif keyboard_key is None:
		for keyboard_key_charac in list(settings.keyboard_nVirtKey_dict.keys()):
			if keyboard_click_events[keyboard_key_charac] is not False:
				clicked = True
				return clicked
			else:
				pass
		return clicked


def get_keyboard_key_clicked_str(keyboard_click_events):
	for keyboard_key_name in list(settings.keyboard_nVirtKey_dict.keys()):
		if keyboard_click_events[keyboard_key_name] is not False:
			return keyboard_key_name
		else:
			pass


def update_keyboard_states(init_keyboard_key_states, keyboard_key_clicked_events):
	updated_init_keyboard_key_states = init_keyboard_key_states
	for key_state, changed_state in keyboard_key_clicked_events.items():
		if changed_state is not False:
			updated_init_keyboard_key_states[key_state] = changed_state
		else:
			pass
	return updated_init_keyboard_key_states


