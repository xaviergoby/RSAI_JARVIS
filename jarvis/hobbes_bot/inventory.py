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


class InventoryHandler:

    def __init__(self):
        self.obj_dect_data_dir = os.path.join(settings.DATA_DIR, r"obj_dect")
        self.inv_item_img_icons_dir_path = os.path.join(self.obj_dect_data_dir, r"inv_items\images")
        self.inv_img_icon = os.path.join(self.obj_dect_data_dir, r"game_main_interface\inv_icon.PNG")
        self.saved_inv_item_img_icon_file_names = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
        self.saved_inv_item_img_icon_names_list = [inv_item_img_icon_name.split(".")[0] for
                                                   inv_item_img_icon_name in self.saved_inv_item_img_icon_file_names]
        self.inv_item_img_metadata = self.__initialize_inv_item_imgs_metadata()
        self.__load_known_inv_items_file_names()
        self.__init_known_inv_items_names()
        self.__init_known_inv_items_names_imgs_dict()
        self.__init_known_inv_items_count_dict()


    def __load_known_inv_items_file_names(self):
        # __load_known_inv_items_file_names
        known_inv_items_file_names = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
        # saved_inv_item_img_icon_file_names
        self.known_inv_items_file_names = known_inv_items_file_names
        return known_inv_items_file_names

    def __init_known_inv_items_names(self):
        # inv_items_img_file_names_with_ext = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
        inv_items_img_file_names_without_ext = list(map(file_path_tools.get_file_stem_name, self.known_inv_items_file_names))
        self.known_inv_items_names = inv_items_img_file_names_without_ext

    def __init_known_inv_items_names_imgs_dict(self):
        known_inv_items_names_imgs_dict = {}
        # inv_items_img_file_names_with_ext = file_path_tools.get_dir_contents_list(self.inv_item_img_icons_dir_path)
        # inv_items_img_file_names_without_ext = list(map(file_path_tools.get_file_stem_name, inv_items_img_file_names_with_ext))
        for inv_item_file_name_i in range(len(self.known_inv_items_names)):
            img_abs_file_path = os.path.join(self.inv_item_img_icons_dir_path,
                                             self.known_inv_items_names[inv_item_file_name_i])
            # inv_item_img = cv2.imread(img_abs_file_path).shape[:2]
            inv_item_img = cv2.imread(img_abs_file_path)
            inv_item_name = self.known_inv_items_names[inv_item_file_name_i]
            known_inv_items_names_imgs_dict[inv_item_name] = inv_item_img
        self.known_inv_items_imgs_dict = known_inv_items_names_imgs_dict

    def __init_known_inv_items_count_dict(self):
        known_inv_items_count_dict = {}
        for inv_item_file_name_i in range(len(self.known_inv_items_names)):
            inv_item_name = self.known_inv_items_names[inv_item_file_name_i]
            known_inv_items_count_dict[inv_item_name] = 0
        self.known_inv_items_count_dict = known_inv_items_count_dict


    def __initialize_inv_item_imgs_metadata(self):
        inv_item_imgs_metadata = {}
        known_inv_items_file_names = self.__load_known_inv_items_file_names()
        for inv_item_img_file_name in known_inv_items_file_names:
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


    def get_saved_inv_item_img_icon_names(self):
        saved_inv_item_img_icon_file_names = self.__load_known_inv_items_file_names()
        saved_inv_item_img_icon_names_list = [inv_item_img_icon_name.split(".")[0] for inv_item_img_icon_name in saved_inv_item_img_icon_file_names]
        return saved_inv_item_img_icon_names_list


    def get_inv_item_pos_and_size_by_name(self, inv_item_name):
        inv_item_img_file_path = self.inv_item_img_metadata[inv_item_name]["file_path"]
        # button7location = pyautogui.locateOnScreen('calc7key.png', grayscale=True)
        inv_item_pos_and_size_list = [inv_item for inv_item in pyautogui.locateAllOnScreen(inv_item_img_file_path, confidence=0.9)
                                      if 585 <= inv_item[0] <= 791 and 245 <= inv_item[1] <= 519]
        return inv_item_pos_and_size_list


    def get_inv_item_img_centre_pos_and_dims_list(self, inv_item_img_stem):
        inv_item_img_centre_pos_list = []
        inv_item_pos_and_size_list = self.get_inv_item_pos_and_size_by_name(inv_item_img_stem)
        for inv_item_x_pos_and_size in inv_item_pos_and_size_list:
            x_centre = inv_item_x_pos_and_size[0] + inv_item_x_pos_and_size[2]//2
            y_centre = inv_item_x_pos_and_size[1] + inv_item_x_pos_and_size[3]//2
            width = inv_item_x_pos_and_size[2]
            height = inv_item_x_pos_and_size[3]
            inv_item_img_centre_pos_list.append([x_centre, y_centre, width, height])
        return inv_item_img_centre_pos_list


    def drop_all_inv_item_by_name(self, inv_item_img_stem):
        hc = HumanClicker()
        delay = random.uniform(0.5, 0.7)
        # clock_coords = humanization_tools.humanize_game_tile_click_loc_coords(400, 310)
        # hc.move((clock_coords[0], clock_coords[1]), delay)
        # pyautogui.click()
        inv_item_img_centre_pos_and_dims_list = self.get_inv_item_img_centre_pos_and_dims_list(inv_item_img_stem)
        while len(inv_item_img_centre_pos_and_dims_list) != 0:
            click_coords_list = []
            for inv_item_img_centre_pos_and_dims in inv_item_img_centre_pos_and_dims_list:
                click_coords = humanization_tools.humanize_click_pos_coords(inv_item_img_centre_pos_and_dims[0],
                                                                            inv_item_img_centre_pos_and_dims[1],
                                                                            inv_item_img_centre_pos_and_dims[2],
                                                                            inv_item_img_centre_pos_and_dims[3])
                x_click_coord = click_coords[0]
                y_click_coord = click_coords[1]
                click_coords_list.append([x_click_coord, y_click_coord])
            hc = HumanClicker()
            delay = random.uniform(0.4, 0.6)
            hc.move((click_coords_list[0][0], click_coords_list[0][1]), delay)
            pyautogui.keyDown('shift')
            delay = random.uniform(0.01, 0.1)
            time.sleep(delay)
            pyautogui.click()
            time.sleep(delay)
            pyautogui.keyUp('shift')
            if len(click_coords_list) > 1:
                keyboard.press('shift')
                for click_coords in click_coords_list[1:]:
                    x_click_coord = click_coords[0]
                    y_click_coord = click_coords[1]
                    delay = random.uniform(0.5, 0.7)
                    hc.move((x_click_coord, y_click_coord), delay)
                    hc.click()
            time.sleep(delay)
            keyboard.release('shift')
            inv_item_img_centre_pos_and_dims_list = self.get_inv_item_img_centre_pos_and_dims_list(inv_item_img_stem)
            return


    def get_inv_item_count_by_name(self, inv_item_name):
        inv_item_pos_and_size_list = self.get_inv_item_pos_and_size_by_name(inv_item_name)
        inv_item_pos_and_size_list_cnt = len(inv_item_pos_and_size_list)
        return inv_item_pos_and_size_list_cnt


    def get_inv_item_name_cnt_pair_dict(self):
        all_inv_item_name_cnt_pair_dict = {}
        for inv_item_img_icon_file_name in self.saved_inv_item_img_icon_file_names:
            inv_item_img_file_stem = file_path_tools.get_file_stem_name(inv_item_img_icon_file_name)
            all_inv_item_name_cnt_pair_dict[inv_item_img_file_stem] = self.get_inv_item_count_by_name(inv_item_img_file_stem)
        return all_inv_item_name_cnt_pair_dict





if __name__ == "__main__":
    from src.ui_automation_tools import screen_tools
    screen_tools.set_window_pos_and_size(hwnd=None, x_new=0, y_new=0, new_width=800, new_height=600,
                                         wndw_name=settings.GAME_WNDW_NAME)
    inv = InventoryHandler()
    inv.drop_all_inv_item_by_name("iron_ore")
    print(inv.get_inv_item_name_cnt_pair_dict())




