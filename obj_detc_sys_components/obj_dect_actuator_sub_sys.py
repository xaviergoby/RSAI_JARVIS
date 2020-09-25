import numpy as np
import time
from PIL import ImageGrab
import random
from pyclick import HumanClicker


class ObjDectActuatorSubSystem:
	
	def __init__(self, roi):
		self.roi = roi
		self.lmc_click_time = 0
	
	# def perform_lmc(self, lmc_y_c, lmc_x_c):
	# 	wait_time = random.uniform(10, 15)
	# 	if time.time() - self.lmc_click_time > wait_time or self.lmc_click_time == 0:
	# 		y_c, x_c = lmc_y_c, lmc_x_c
	# 		hc = HumanClicker()
	# 		hc.move((x_c, y_c), random.uniform(0.5, 0.9))
	# 		hc.click()
	# 		self.lmc_click_time = time.time()
	# 	else:
	# 		return
	
	def perform_lmc(self, lmc_y_c, lmc_x_c):
		wait_time = random.uniform(10, 15)
		y_c, x_c = lmc_y_c, lmc_x_c
		hc = HumanClicker()
		hc.move((x_c, y_c), random.uniform(0.5, 0.9))
		hc.click()