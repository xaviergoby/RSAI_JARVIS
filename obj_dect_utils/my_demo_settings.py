import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))   # returns C:\Users\XGOBY\TFObjdectTest
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), r"my_demo_workspace\training_demo\data")     # returns C:\Users\XGOBY\TFObjdectTest\my_demo_workspace\training_demo\data
nVirtKey_dict = {"LMB":0x01, "RMB":0x02}
print(ROOT_DIR)
print(DATA_DIR)