import json
import numpy as np
import os
from settings import DATA_DIR

x = np.array([1, 2, 3])
print(x)
origin = "lumbridge"
from src.path_manipulation_tools import file_path_tools
paths_travelled_dir_path = os.path.join(DATA_DIR, r"paths_travelled")
o2ds_travel_path_json_file_path = os.path.join(paths_travelled_dir_path, "{0}.json".format(origin))