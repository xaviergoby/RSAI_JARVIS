import random
from pyclick import HumanClicker


class Mouse:

	@staticmethod
	def lmc(lmc_y_c, lmc_x_c):
		y_c, x_c = lmc_y_c, lmc_x_c
		hc = HumanClicker()
		hc.move((x_c, y_c), random.uniform(0.5, 0.9))
		hc.click()