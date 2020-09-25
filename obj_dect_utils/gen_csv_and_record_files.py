from obj_dect_utils import xml_to_csv

# Creating .csv files for a specific tasks train and test images & .xml datasets
# E.g. w/ task_name = "slaying_cows"
# Then running xml_to_csv.main(task_name) creates the 2 followingly named files inside the dir C:\Users\XGOBY\RSAIBot\src\TensorFlow_Models\xml_annots
# slaying_cows_train_labels.csv"
# slaying_cows_test_labels.csv"
task_name = "wc"
xml_to_csv.main(task_name)

# Creating .record
# os.system("python gen_tf_records.py")
# __name__ = "generate_tfrecord"
# tf.app.run()
# generate_tfrecord.run()
import subprocess
train_args_str = r"python gen_tf_records.py --csv_input=xml_annots\{0}_train_labels.csv --image_dir=images\tasks\{0}\train --output_path=xml_annots\{0}_train.record".format(task_name)
test_args_str = r"python gen_tf_records.py --csv_input=xml_annots\{0}_test_labels.csv --image_dir=images\tasks\{0}\test --output_path=xml_annots\{0}_test.record".format(task_name)
subprocess.call(train_args_str, shell=True)
subprocess.call(test_args_str, shell=True)
