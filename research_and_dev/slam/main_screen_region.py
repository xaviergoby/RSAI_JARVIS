import settings
from src.ui_automation_tools import mouse_events_monitoring
import keyboard
import win32api as wapi

if __name__ == "__main__":
	# print("start")
	# while True:q
	# 	k = detect_keyboard_key_events(["ctrl+t", "q"])
	# 	k = detect_keyboard_key_events("q")
	# 	if k is not None:
	# 		print("got {0}".format(k))
	# 		print(type(k))
	paused = False
	checked_keys = []
	print(f"Pre while loop checked_keys: {checked_keys}")
	while True:
		print(f"keyboard._pressed_events: {keyboard._pressed_events}")
		print(f"\nWhile loop INIT checked_keys: {checked_keys}")
		print(f"While loop INIT state of paused = {paused}")
		print(f"wapi.GetAsyncKeyState(ord('P')): {wapi.GetAsyncKeyState(ord('P'))}")
		if "P" in checked_keys:
			print(f"P IS in checked_keys: {checked_keys}")
			print(f"paused is CURRENTLY: {paused}")
			if paused is False:
				paused = True
			elif paused is True:
				paused = False
			print(f"paused is NOW: {paused}")
		elif "P" not in checked_keys:
			print(f"P IS NOT in checked_keys: {checked_keys}")
		print(f"While loop FINAL checked_keys: {checked_keys}")
		print(f"While loop FINAL state of paused = {paused}")
		# print(f"Pre delay checked_keys: {checked_keys}")
		checked_keys = mouse_events_monitoring.key_check()
		# hw_input_output_tools.delay_timer(2)
		# print(f"Post delay checked_keys: {checked_keys}")