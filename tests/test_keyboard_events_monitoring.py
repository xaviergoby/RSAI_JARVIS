from src.ui_automation_tools.keyboard_events_monitoring import *
import time


def test_keyboard_key_click_event_methods(keyboard_keys_2_monitor_list):
	init_key_states = get_init_keyboard_states(settings.keyboard_nVirtKey_dict)
	print(f"Initial keyboard key states: {init_key_states}")
	while True:
		keyboard_key_clicked_events = get_keyboard_click_events(init_key_states, settings.keyboard_nVirtKey_dict)
		if keyboard_key_clicked(keyboard_key_clicked_events, keyboard_keys_2_monitor_list) is True:
			print("\nKeyboard Key Click Event Detected")
			clicked_keyboard_key = get_keyboard_key_clicked_str(keyboard_key_clicked_events)
			print("Keyboard Key Clicked: {0}".format(clicked_keyboard_key))
			print("Updating {0} initial key states...\n".format(clicked_keyboard_key))
			init_key_states = update_keyboard_states(init_key_states, keyboard_key_clicked_events)
			print(f"New Updated Keyboard Key States: {init_key_states}")
		else:
			# print("No Keyboard Key Click Event Detected")
			init_key_states = update_keyboard_states(init_key_states, keyboard_key_clicked_events)
		time.sleep(0.5)

if __name__ == "__main__":
	keyboard_keys_2_monitor_list = ["P", "T"]
	test_keyboard_key_click_event_methods(keyboard_keys_2_monitor_list)