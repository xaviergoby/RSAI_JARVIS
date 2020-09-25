import queue
import cv2
import pyautogui
import numpy as np


class RSAIBot:

    def __init__(self, bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls, bot_nav_data_handler_cls, events_list=None):
        self.paused = False
        self.events_list = [] if events_list is None else events_list
        self.events_queue = queue.Queue()
        self.bot_sensors_cls = bot_sensors_cls
        self.bot_actuators_cls = bot_actuators_cls
        self.bot_nav_grid_map_cls = bot_nav_grid_map_cls
        self.bot_nav_data_cls = bot_nav_data_handler_cls
        self.bot_components_cls_list = [bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls, bot_nav_data_cls]
        self._set_init_empty_events_list()
        self._init_current_location()
        
        
    def _set_init_empty_events_list(self):
        for bot_component_cls in self.bot_components_cls_list:
            bot_component_cls.events_list = self.events_list

    # def _set_bot_init_current_locs(self):
    #     for bot_nav_component_cls in [self.bot_nav_grid_map_cls, self.nav_data_toolkit_cls]:
    #         bot_nav_component_cls.init_world_coords =

    def _init_current_location(self):
        self.bot_current_loc = self.bot_nav_data_cls.load_bot_init_world_loc()

    # @staticmethod
    def _update_run(self):
        cv2_close_key = cv2.waitKey(1) & 0xFF
        if cv2_close_key == ord('E') or cv2_close_key == ord('e'):
            return self._end_run()

    #@staticmethod
    def _end_run(self):
        cv2.destroyAllWindows()
        return True
    
    def run_bot(self):
        self.bot_actuators_cls.init_all_states()
        while True:
            #####
            self.sensors_percept = self.bot_sensors_cls.get_sensors_percept()
            self.bot_sensor_percept_array = self.sensors_percept[0]
            bot_sensor_percept_rgb_img = self.sensors_percept[1]
            self.bot_sensors_cls.display_sensor_percept(sensor_percept_array=self.bot_sensor_percept_array)
            #####
            if self.paused is False:
                #### runtime tasks
                if self.bot_actuators_cls.lmb_clicked is True:
                    print("lmb clicked!")
                    lmc_mouse_screen_pos = pyautogui.position()
                    lmc_px_x, lmc_px_y = lmc_mouse_screen_pos[0], lmc_mouse_screen_pos[1]
                    grid_pnt_x, grid_pnt_y = self.bot_nav_grid_map_cls.get_lmc_nn_grid_pnt(lmc_px_x, lmc_px_y)
                    print(f"grid_pnt_x: {grid_pnt_x}")
                    print(f"grid_pnt_y: {grid_pnt_y}")
                    bot_current_x_coord = self.bot_current_loc[0] + grid_pnt_x
                    bot_current_y_coord = self.bot_current_loc[1] + grid_pnt_y
                    self.bot_current_loc = [bot_current_x_coord, bot_current_y_coord]
                    # self.nav_data_toolkit_cls.update_loc_memory(self.init_world_coords)
                    print(f"bot_current_x_coord: {bot_current_x_coord}")
                    print(f"bot_current_y_coord: {bot_current_y_coord}")


                elif self.bot_actuators_cls.P_clicked is True:
                    self.paused = True
                    print("paused...")

                elif self.bot_actuators_cls.T_clicked is True:
                    pass
                    # np.s
                # print("paused...")
                ####

                
            elif self.paused is True:
                #### runtime tasks
                if self.bot_actuators_cls.P_clicked is True:
                    print("unpaused...")
                    self.paused = False
                ####p
                

            self.bot_actuators_cls.update_all_states()

            if self._update_run() is True:
                self.bot_nav_data_cls.load_bot_init_world_loc()
                self.bot_nav_data_cls.update_loc_memory(self.bot_current_loc)
                break
            
            
            
            
        
        


if __name__ == "__main__":
    from research_and_dev.event_driven_system.sensors import sensors_cls
    from research_and_dev.event_driven_system.actuators import actuators_cls
    from research_and_dev.event_driven_system.nav_grids import local_main_view_nav_grid
    from research_and_dev.event_driven_system.nav_data_tools import nav_data_toolkit

    events_list = []
    bot_sensors_cls = sensors_cls.Sensors()
    bot_actuators_cls = actuators_cls.Actuators()
    bot_nav_grid_map_cls = local_main_view_nav_grid.LocalNavigationGridMap(grid_opt=1)
    bot_nav_data_cls = nav_data_toolkit.NavigationDataToolkit()
    bot = RSAIBot(bot_sensors_cls, bot_actuators_cls, bot_nav_grid_map_cls, bot_nav_data_cls, events_list=events_list)
    print(bot.bot_current_loc)
    bot.run_bot()















