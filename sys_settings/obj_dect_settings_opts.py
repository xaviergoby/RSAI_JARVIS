

OBJ_DECT_SETTINGS = {"task": {"cow_slaying":
	                              {"MODEL_NAME": "inference_graph",
	                               "FROZEN_GRAPH_CKPT_FILE": "frozen_inference_graph.pb",
	                               "CLASS_LABELS_FILE": "object-detection.pbtxt",
	                               "NUM_CLASSES": 1,
	                               },
                              "mining": {},
                              }
                     }

if __name__ == "__main__":
	from sys_settings.obj_dect_settings_cls import CollectAndMergeSeriesFeatures
	import os
	import sys
	sys.path.append("..")
	CWD_PATH = os.getcwd()
	print(CWD_PATH)
	res = CollectAndMergeSeriesFeatures(settings = OBJ_DECT_SETTINGS["task"]["cow_slaying"])
	# print("(From within __name__ == '__main__' code block)\nHey there you in the Anaconda (Command) Prompt!")