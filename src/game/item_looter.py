from src.ui_automation_tools import screen_tools
import pyautogui
from pyclick import HumanClicker
import win32gui
import time
import settings
import random
from src.ui_automation_tools import mouse_events_monitoring
from src.game import humanization_tools
import os
from src.path_manipulation_tools import file_path_tools
import cv2
from src.game import humanization_tools
from pyclick import HumanClicker
import keyboard


class ItemLooter:

	def __init__(self):
		self.obj_dect_data_dir = os.path.join(settings.DATA_DIR, r"obj_dect")
		self.inv_item_img_icons_dir_path = os.path.join(self.obj_dect_data_dir, r"grnd_items\images")
		self.inv_img_icon = os.path.join(self.obj_dect_data_dir, r"game_main_interface\inv_icon.PNG")
		self.saved_inv_item_img_icon_file_names = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
		self.saved_inv_item_img_icon_names_list = [inv_item_img_icon_name.split(".")[0] for
		                                           inv_item_img_icon_name in self.saved_inv_item_img_icon_file_names]
		self.inv_item_img_metadata = self.__initialize_inv_item_imgs_metadata()

	def get_saved_inv_item_img_file_names(self):
		saved_inv_item_img_icon_file_names = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
		return saved_inv_item_img_icon_file_names


	def __initialize_inv_item_imgs_metadata(self):
		inv_item_imgs_metadata = {}
		inv_item_img_file_names_list = self.get_saved_inv_item_img_file_names()
		for inv_item_img_file_name in inv_item_img_file_names_list:
			# the stem of a file (name/full_path) is, e.g. a file name w/o its ext, e.g. w/o .PNG for an img file
			img_file_stem = file_path_tools.get_file_stem_name(inv_item_img_file_name)
			img_file_path = os.path.join(self.inv_item_img_icons_dir_path, inv_item_img_file_name)
			img_dims = cv2.imread(img_file_path).shape[:2]
			img_height = img_dims[0]
			img_width = img_dims[1]
			inv_item_imgs_metadata[img_file_stem] = {"file_name":inv_item_img_file_name,
			                                         "file_path": img_file_path,
			                                         "width": img_width,
			                                         "height": img_height
			                                         }
		return inv_item_imgs_metadata


if __name__ == "__main__":
	looter = ItemLooter()
	print(looter.inv_item_img_metadata)
	time.sleep(2)
	tem_pos_and_size_list = [inv_item for inv_item in
	                         pyautogui.locateAllOnScreen(looter.inv_item_img_metadata["cow_hide2"]["file_path"], confidence=0.8)
	                         if 8 <= inv_item[0] <= 585 and 31 <= inv_item[1] <= 591]
	button7location = pyautogui.locateOnScreen(looter.inv_item_img_metadata["cow_hide2"]["file_path"], region=(0,0, 585, 591), confidence=0.7)
	print(tem_pos_and_size_list)
	print(button7location)