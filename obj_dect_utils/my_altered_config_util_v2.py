import tensorflow as tf
from google.protobuf import text_format
import os
from object_detection.protos import pipeline_pb2
from tensorflow.python.lib.io import file_io


def save_pipeline_config(pipeline_config, directory):
	"""Saves a pipeline config obj_id_info file to disk.
	Args:pipeline_config: A pipeline_pb2.TrainEvalPipelineConfig.
	directory: The model directory into which the pipeline config file will be saved.
	"""
	if not file_io.file_exists(directory):
		file_io.recursive_create_dir(directory)
	pipeline_config_path = os.path.join(directory, "pipeline.config")
	config_text = text_format.MessageToString(pipeline_config)
	with tf.gfile.Open(pipeline_config_path, "wb") as f:
		tf.logging.info("Writing pipeline config file to %s",
						pipeline_config_path)
		f.write(config_text)


def get_configs_from_pipeline_file(pipeline_config_path, config_override=None):
	""" Reads config from a file containing pipeline_pb2.TrainEvalPipelineConfig.
	Args:
	pipeline_config_path: Path to pipeline_pb2.TrainEvalPipelineConfig obj_id_info
	proto.
	config_override: A pipeline_pb2.TrainEvalPipelineConfig obj_id_info proto to
	override pipeline_config_path.
	Returns:
	Dictionary of configuration obj_centroids. Keys are `model`, `train_config`,
	`train_input_config`, `eval_config`, `eval_input_config`. Value are the
	corresponding config obj_centroids.
	"""

	# assign pipeline_config to a <class 'object_detection.protos.pipeline_pb2.TrainEvalPipelineConfig'> object instance
	pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
	with tf.gfile.GFile(pipeline_config_path, "r") as f:
		proto_str = f.read()
		text_format.Merge(proto_str, pipeline_config)
	if config_override:
		text_format.Merge(config_override, pipeline_config)
	# print(pipeline_config)
	return pipeline_config


def create_configs_from_pipeline_proto(pipeline_config):
	"""Creates a configs dictionary from pipeline_pb2.TrainEvalPipelineConfig.
	Args:pipeline_config: pipeline_pb2.TrainEvalPipelineConfig proto object.
	Returns:
		Dictionary of configuration obj_centroids. Keys are `model`, `train_config`,
		`train_input_config`, `eval_config`, `eval_input_configs`. Value are
		the corresponding config obj_centroids or list of config obj_centroids (only for
		eval_input_configs).
		"""
	configs = {}
	configs["model"] = pipeline_config.model
	configs["train_config"] = pipeline_config.train_config
	configs["train_input_config"] = pipeline_config.train_input_reader
	configs["eval_config"] = pipeline_config.eval_config
	configs["eval_input_configs"] = pipeline_config.eval_input_reader
	# Keeps eval_input_config only for backwards compatibility. All clients should
	# read eval_input_configs instead.
	if configs["eval_input_configs"]:
		configs["eval_input_config"] = configs["eval_input_configs"][0]
	if pipeline_config.HasField("graph_rewriter"):
		configs["graph_rewriter_config"] = pipeline_config.graph_rewriter

	return configs


# C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\training\ssd_mobilenet_v1_pets.config
task_name = "wc"
num_classes = 1
batch_size = 1
tf_record_input_reader_input_path = ["C:/Users/XGOBY/RSAIBot/src/TensorFlow_Models/xml_annots/{0}_train.record".format(task_name)]
train_input_reader_label_map_path = "C:/Users/XGOBY/RSAIBot/src/TensorFlow_Models/training/{0}/object-detection.pbtxt".format(task_name)

task_pipeline_config_path = r"C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\training\ssd_mobilenet_v1_pets.config"
task_fine_tune_checkpoint = "C:/Users/XGOBY/RSAIBot/src/TensorFlow_Models/ssd_mobilenet_v1_coco_11_06_2017/model.ckpt"
# task_pipeline_config_save_dir_path = r"C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\training\{0}".format(task_name)

# Return a <class 'object_detection.protos.pipeline_pb2.TrainEvalPipelineConfig'> object instance
configs = get_configs_from_pipeline_file(task_pipeline_config_path)
print("Current configs.model.ssd.num_classes key value: {0}".format(configs.model.ssd.num_classes))
configs.model.ssd.num_classes = num_classes
configs.train_config.batch_size = batch_size
configs.train_config.fine_tune_checkpoint = task_fine_tune_checkpoint
configs.train_input_reader.tf_record_input_reader.input_path = tf_record_input_reader_input_path
configs.train_input_reader.label_map_path = train_input_reader_label_map_path
print("New changed configs.model.ssd.num_classes key value: {0}".format(configs.model.ssd.num_classes))

# Create a configs dictionary from pipeline_pb2.TrainEvalPipelineConfig.
# config_as_dict = create_configs_from_pipeline_proto(configs)

# pipeline_config is a pipeline_pb2.TrainEvalPipelineConfig. class obj instance, i.e. configs
task_pipeline_config_save_dir_path = r"C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\training\{0}".format(task_name)
save_pipeline_config(configs, task_pipeline_config_save_dir_path)


