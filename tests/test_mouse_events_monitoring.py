from src.ui_automation_tools.mouse_events_monitoring import *
from src.ui_automation_tools.screen_tools import *
import time
from settings import mouse_nVirtKey_dict

def test_get_mouse_state():
	"""
	This function is meant for testing out the get_mouse_state() method from
	ui_automation_tools.py in a very simple way with only print statements! The reason
	for the desirability of print statements is because this function is not only meant for
	testing purposes but also for demonstrating how it is exactly that the state of a mouse changes
	and how this information is provided to us. There are 4 possible scenarions:

	Terminology:
	LMB: Left mouse button (RMB is obv now)
	init state: state before mouse action taken
	mid state: state during mouse action taking place
	final state: state after mouse action taken
	clicked: this literally means clicking as you would click on any button
	pressed: this means the LMB is being maintained pressed
	unpressed: this means that the LMB is now free

	NOTE: The time.sleep(2) line is very important! By having a second or 2 of idling time between each succesive
	while loop this provides the necessary amount of time required for the user to take some action with his/her
	mouse so that the state transitions which take place for each scenario become legibile for user reading the
	print statement outputs in the console.

	Scenario #1:            #Scenario #2:
	init state = 1          init state = 0
	* LMB clicked *         * LMB clicked *
	final state = 0         final state = 1

	#Scenario #3:           #Scenario #4:
	init state = 0          init state = 1
	* LMB pressed *         * LMB pressed *
	mid state = -127        mid state = -128
	* LMB unpressed *       * LMB unpressed *
	final state = 1         final state = 0

	:return:
	"""
	while True:
		print("\nChecking and getting mouse state and coordinates....")
		mouse_coords_and_state = get_mouse_state()
		mouse_coords = mouse_coords_and_state[0]
		mouse_state = mouse_coords_and_state[1]
		print("mouse (x, local_y) coords: {0}".format(mouse_coords))
		print("mouse state: {0}".format(mouse_state))
		seconds_to_sleep = 3
		print("Sleeping for...")
		for i in range(seconds_to_sleep):
			print("{0} seconds".format(i+1))
			time.sleep(1)


def test_mouse_click_event_methods():
	init_key_states = get_init_mouse_states(mouse_nVirtKey_dict)
	while True:
		coords = pyautogui.position()
		mouse_click_events = get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
		if mouse_button_clicked(mouse_click_events, ["LMB"]) is True:
			print("\nMouse Click Event Detected")
			clicked_mouse_button = get_mouse_button_clicked_str(mouse_click_events)
			print("Mouse Button Clicked: {0}".format(clicked_mouse_button))
			print("{0} Click Location Coordinates: {1}".format(clicked_mouse_button, coords))
			print("Updating LMB & RMB initial key states...\n")
			init_key_states = update_mouse_states(init_key_states, mouse_click_events)
		else:
			print("No Click Event Detected")
		time.sleep(0.1)
		
		
def test_click_event_methods():
	init_key_states = get_init_mouse_states(mouse_nVirtKey_dict)
	while True:
		coords = pyautogui.position()
		click_events = get_mouse_click_events(init_key_states, mouse_nVirtKey_dict)
		if mouse_button_clicked(click_events, ["LMB"]) is True:
			print("\nMouse Click Event Detected")
			clicked_mouse_button = get_mouse_button_clicked_str(click_events)
			print("Mouse Button Clicked: {0}".format(clicked_mouse_button))
			print("{0} Click Location Coordinates: {1}".format(clicked_mouse_button, coords))
			print("Updating LMB & RMB initial key states...\n")
			init_key_states = update_mouse_states(init_key_states, click_events)
		else:
			print("No Click Event Detected")
		time.sleep(0.1)


