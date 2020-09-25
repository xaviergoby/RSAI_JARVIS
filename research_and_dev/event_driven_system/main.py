from research_and_dev.event_driven_system.sensors import sensors_cls
from research_and_dev.event_driven_system.actuators import actuators_cls
from research_and_dev.event_driven_system.nav_grids import local_main_view_nav_grid
from research_and_dev.event_driven_system.nav_data_tools import nav_data_toolkit
from research_and_dev.event_driven_system.rsai_bots import rsai_bot_v1
from src.ui_automation_tools import screen_tools
from research_and_dev.event_driven_system.mini_map import Minimap



game_client_dims = (791, 591)
local_nav_sq_grid_side_len = 15
current_world_grid_loc = None
minimap = Minimap(game_client_dims, local_nav_sq_grid_side_len, current_world_grid_loc)


screen_tools.set_window_pos_and_size()


events_list = []
bot_sensors_cls = sensors_cls.Sensors()
bot_actuators_cls = actuators_cls.Actuators()
bot_nav_grid_map_cls = local_main_view_nav_grid.LocalNavigationGridMap(grid_opt=1)
bot_nav_data_cls = nav_data_toolkit.NavigationDataToolkit()
bot = rsai_bot_v1.RSAIBot(bot_sensors_cls, bot_actuators_cls,
                          bot_nav_grid_map_cls, bot_nav_data_cls,
                          events_list=events_list)
print(bot.bot_current_loc)
bot.run_bot()

