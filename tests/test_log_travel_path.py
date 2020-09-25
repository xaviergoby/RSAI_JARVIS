from settings import DATA_DIR
import os

print("test - line 10")
origin = "lumbridge"
print("test - line 12")
paths_travelled_dir_path = os.path.join(DATA_DIR, r"paths_travelled")
print("paths_travelled_dir_path: {0}".format(paths_travelled_dir_path))
print("test - line 15")
o2ds_travel_path_json_file_path = os.path.join(paths_travelled_dir_path, "{0}.json".format(origin))
print("o2ds_travel_path_json_file_path: {0}".format(o2ds_travel_path_json_file_path))
print("test - line 18")
from uncategorised import log_travel_path

print("test - line 20")
travelled_path_log = log_travel_path.TravelledPathLogger(origin ="lumbridge", destination ="gs_tree_farm")
print("test - line 22")
coords_and_delays_list = travelled_path_log.o2d_path_travelled_click_coords_and_delays_list
print("test - line 24")
print("coords_and_delays_list: {0}".format(coords_and_delays_list))
print("len(coords_and_delays_list): {0}".format(len(coords_and_delays_list)))
print("len(coords_and_delays_list[0]): {0}".format(len(coords_and_delays_list[0])))
print("test - line 28")
# plt.use('Agg')
# import matplotlib.pyplot as plt
print("test - line 32")

