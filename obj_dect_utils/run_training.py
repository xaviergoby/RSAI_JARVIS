import subprocess
# import tensorflow as tf

# python model_main.py --logtostderr --model_dir=training/ --pipeline_config_path=training/faster_rcnn_inception_v2_pe.confiG

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.Session(config=config)

model_main_training_script_path = r"C:\Users\Xavier\RSAI_JARVIS\obj_dect_utils\model_main.py"
model_dir_path = r"C:\Users\Xavier\RSAI_JARVIS\training\checkpoints\tasks\mining"
pipeline_config_path = r"C:\Users\Xavier\RSAI_JARVIS\training\config_files\mining_ssd_mobilenet_v1_pets.config"
train_args_str = r"python train.py --logtostderr --train_dir={0} --pipeline_config_path={1}".format(model_dir_path, pipeline_config_path)
# train_args_str = r"python {0} --logtostderr --train_dir={1} --pipeline_config_path={2}".format(model_main_training_script_path, model_dir_path, pipeline_config_path)
subprocess.call(train_args_str, shell=True)
# python train.py --logtostderr --train_dir=training\ --pipeline_config_path=training\ssd_mobilenet_v1_pets.config



# model_main_training_script_path = r"C:\Users\Xavier\RSAI_JARVIS\obj_dect_utils\model_main.py"
# model_dir_path = r"C:\Users\Xavier\RSAI_JARVIS\training\checkpoints\tasks\mining"
# pipeline_config_path = r"C:\Users\Xavier\RSAI_JARVIS\training\config_files\mining_ssd_mobilenet_v1_pets.config"
# model_main_train_args_str = r"python {0} --logtostderr --model_dir={1} --pipeline_config_path={2}".format(model_main_training_script_path, model_dir_path, pipeline_config_path)
# subprocess.call(model_main_train_args_str, shell=True)