from src.ui_automation_tools import screen_tools
import pyautogui
from pyclick import HumanClicker
import win32gui
import time
import settings
import random
from src.ui_automation_tools import mouse_events_monitoring

win_name = settings.GAME_WNDW_NAME
# win_name = "RuneLite - PolarHobbes"
hwnd = win32gui.FindWindow(None, win_name)
wndw_x_wrt_screen = 0  # -8
wndw_y_wrt_screen = 0  # -31
wndw_width_in_screen = 800
wndw_height_in_screen = 600
screen_tools.set_window_pos_and_size(hwnd=None, x_new=wndw_x_wrt_screen, y_new=wndw_y_wrt_screen,
                                     new_width=wndw_width_in_screen, new_height=wndw_height_in_screen,
                                     wndw_name=win_name)

# fishx = 300
fishx = 450
# fixhy = 205
fixhy = 320

i1x = 670
i1y = 350
# + 40 i#local_y to drop

i2x = 710
i2y = 350

tin_mine_coords = [[390, 280], [345, 320], [400, 360]]
iron_mine_coords = [[390, 280], [345, 320], [400, 360]]
silver_mine_coords = [[390, 280], [345, 320]]
gold_mine_coords = [[]]
rslite_inv_coords = [[630, 350], [670, 350], [710, 350], [630, 390], [670, 390], [710, 390]]
osrs_inv_coords = [[610, 350], [650, 350], [690, 350], [6100, 390], [650, 390], [690, 390]]
# ore_pick = random.randint(0, 2)
paused = False
while True:
	if not paused:
		hc = HumanClicker()
		# delay_seconds = random.uniform(1, 2)
		# delay_seconds = 1
		# print("Clicking on wish in ...")
		# for delay_sec in range(round(delay_seconds), 0, -1):
		# 	print("{0} seconds".format(delay_sec))
		# 	time.sleep(1)
		# print("Clicking now!")
		ore_pick = random.randint(0, 2)
		for ore_pick in range(0,len(iron_mine_coords)):
			resource_x_y_coord = iron_mine_coords[ore_pick]
			resourxe_x_coord = resource_x_y_coord[0]
			resourxe_y_coord = resource_x_y_coord[1]
			hc.move((resourxe_x_coord, resourxe_y_coord), random.uniform(0.6, 0.8))
			for click_num in range(100): # 50 100 60
				time.sleep(random.uniform(0.01, 0.001))
				hc.click()
			# hc.click()
			# hc.click()
			for inv_coord in rslite_inv_coords[:4]:
				inv_x_coord = inv_coord[0]
				inv_y_coord = inv_coord[1]
				hc.move((inv_x_coord, inv_y_coord), random.uniform(0.2, 0.25))
				pyautogui.click(inv_x_coord, inv_y_coord, button="right")
				hc.move((inv_x_coord, inv_y_coord + 40), random.uniform(0.2, 0.25))
				pyautogui.click(x=inv_x_coord, y=inv_y_coord + 40)
			# keys = hw_input_output_tools.key_check()
			# if 'P' in keys:  # P for Pause
			# 	if paused:
			# 		paused = False
			# 		print('unpaused!')
			# 		start_time = time.time()
			# 	else:
			# 		print('Pausing!')
			# 		paused = True
			# 		time.sleep(1)
				# hc.click()
			# time.sleep(2)

	keys = mouse_events_monitoring.key_check()
	if 'P' in keys:  # P for Pause
		if paused:
			paused = False
			print('unpaused!')
			time.sleep(1)
			start_time = time.time()
		else:
			print('Pausing!')
			paused = True
			time.sleep(1)
		# pyautogui.click((i1x, i1y + 40), 0.2)
		# hc.move((i1x, i1y + 40), 0.2)
		# hc.click()
		# hc.move((i2x, i2y), 0.5)
		# pyautogui.click(button="right")
		# pyautogui.click((i2x, i2y + 40), 0.2)
		# hc.move((i2x, i2y + 40), 0.5)
		# hc.click()
