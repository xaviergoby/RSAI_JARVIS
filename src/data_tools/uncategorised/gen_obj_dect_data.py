from src.path_manipulation_tools import file_path_tools
from settings import *
import pyautogui
from src.ui_automation_tools.mouse_events_monitoring import key_check
import time
from ui_automation_tools.hw_input_output_tools import get_mouse_state



class GenObjDectData:
	"""
	The data which is being generated, is, in essence, nothing more than screen shots
	of the game as it is being played. However, the screen shot region may vary, i.e. preferably differing
	regions for when generated mini map data and ge data or wc data
	"""

	def gen_task_data(self, task_name, region=None):
		path = os.path.join(DATA_DIR, r"obj_dect\tasks\{0}\images".format(task_name))
		if file_path_tools.get_most_recent_data_file_name(path) is False:
			img_idx = 0
		else:
			latest_img_file = file_path_tools.get_most_recent_data_file_name(path)
			latest_img_idx = int("".join(map(str, [int(s) for s in latest_img_file.split() if s.isdigit()])))
			img_idx = latest_img_idx

		paused = False
		while True:

			if not paused:
				mouse_state = get_mouse_state()
				output = key_check()
				if ((mouse_state[1] == -127) or (mouse_state[1] == -128)) or (mouse_state[1] == 1 and len(output) != 0):
					img_idx = img_idx + 1
					img_screen_shot_name = os.path.join(path, "{0}_obj_dect_{1}.png".format(task_name, img_idx))
					pyautogui.screenshot(img_screen_shot_name,
				                        region=region)
					output = key_check()

			keys = key_check()

			if 'T' in keys:
				if paused:
					paused = False
					print('unpaused!')
					time.sleep(1)

				else:
					print('Pausing!')
					paused = True




	def gen_mini_map_data(self, region=None):
		pass

if __name__ == "__main__":
	GenObjDectData().gen_task_data("wc")