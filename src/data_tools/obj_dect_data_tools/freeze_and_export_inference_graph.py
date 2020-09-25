import os
import subprocess
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import settings



task_name = "mining"
task_ckpt_file_number = "7822"
task_ckpt_file_name = "model.ckpt-{0}".format(task_ckpt_file_number)
pipeline_config_file_name = "mining_ssd_mobilenet_v1_pets.config"

export_inference_graph_py_path = os.path.join(settings.ROOT_DIR, r"models\research\object_detection\export_inference_graph.py")
task_ckpt_file_path = os.path.join(settings.OBJ_DECT_TRAINING_CKPTS_DIR, r"tasks\{0}\{1}".format(task_name, task_ckpt_file_name))
pipeline_config_file_path = os.path.join(settings.OBJ_DECT_TRAINING_PIPELINE_CONFIGS_DIR, pipeline_config_file_name)
task_inference_graph_output_dir_path = os.path.join(settings.OBJ_DECT_INFERENCE_GRAPHS_DIR, r"tasks\{0}".format(task_name))

# export_inference_graph_py_path
#
# pipeline_config_file_path
# task_ckpt_file_path
#   C:\Users\Xavier\RSAI_JARVIS\training\checkpoints\tasks\mining\model.ckpt-7822
# task_inference_graph_output_dir_path

export_inference_graph_cmd_str = "python {0} --input_type image_tensor --pipeline_config_path {1} --trained_checkpoint_prefix {2} --output_directory {3}".format(export_inference_graph_py_path,
                                                                                                                                                                 pipeline_config_file_path,
                                                                                                                                                                 task_ckpt_file_path,
                                                                                                                                                                 task_inference_graph_output_dir_path)
print(export_inference_graph_py_path)
print("\n")
print(task_ckpt_file_path)
print("\n")
print(pipeline_config_file_path)
print("\n")
print(task_inference_graph_output_dir_path)
print("\n")
print(export_inference_graph_cmd_str)
subprocess.call(export_inference_graph_cmd_str, shell=True)

# C:\Users\Xavier\RSAI_JARVIS\models\research\object_detection\export_inference_graph.py
# task_obj_dect_data_dir = os.path.join(settings.OBJ_DECT_DATA_DIR, r"tasks\{0}".format(task_name))

# python {export_inference_graph_py_path} --input_type image_tensor --pipeline_config_path {pipeline_config_file_path} --trained_checkpoint_prefix {task_ckpt_file_path} --output_directory {inference_graph_output_dir_path}

# python export_inference_graph.py --input_type image_tensor --pipeline_config_path training/ssd_mobilenet_v1_pets.config --trained_checkpoint_prefix training/model.ckpt-9292 --output_directory inference_graph
# python export_inference_graph.py --input_type image_tensor --pipeline_config_path ssd_mobilenet_v1_pets.config --trained_checkpoint_prefix training/model.ckpt-9292 --output_directory inference_graph