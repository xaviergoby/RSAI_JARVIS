from settings import DATA_DIR
import os

# click_coords_and_delays_list = []

origin = "lumbridge"
paths_travelled_dir_path = os.path.join(DATA_DIR, r"paths_travelled")
o2ds_travel_path_json_file_path = os.path.join(paths_travelled_dir_path, "{0}.json".format(origin))
from src.data_tools import log_travel_path
# with open()
print(paths_travelled_dir_path)
print(o2ds_travel_path_json_file_path)
# full_path = log_travel_path.TravelledPathLogger("lumbridge", "gs_tree_farm")
travelled_path_log = log_travel_path.TravelledPathLogger(origin ="lumbridge", destination ="gs_tree_farm")
# full_path = travelled_path_log.o2d_path_travelled_click_coords_and_time_list[0]
# print(full_path)