from collections import namedtuple

"""
Consider named tuple as structs or classes with only attribute
"""
"""
1. Download url
2. Location to keep downloded file- compressed file
3. Place to extract the tgz file ie keep raw dataset- decompressed file
4. Train dataset folder
5. Test dataset folder
"""
DataIngestionConfig = namedtuple("DataIngestionConfig",
["dataset_download_url", "tqz_download_dir", "raw_data_dir", "ingested_train_dir", "ingested_test_dir"])

"""
1. valid scheme file path
"""
DataValidationConfig = namedtuple("DataValidationConfig", ["schema_file_path"])

"""
1. 
2. url of transformed train data dir
3. url of transformed test data dir
4. 
"""
DataTransformationConfig = namedtuple("DataTransformationConfig", 
["add_bedroom_per_room", "transformed_train_dir", "transformed_test_dir", "preprocessed_object_file_path"])

"""
1. path to pickle file where model is saved
2. minimum accuracy a model should achieve
"""
ModelTrainConfig = namedtuple("ModelTrainConfig", ["trained_model_file_path", "base_accuracy"])

"""
1. 
2. Timestamp of model evaluation
"""
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path", "time_stamp"])

"""
1. Where deployed model has to be kept
"""
ModelPushConfig = namedtuple("ModelPushConfig", ["export_dir_path"])

"""
1. Where artifacts are kept
"""
TrainingPipeLineConfig = namedtuple("TrainingPipeLineConfig", ["artifact_dir"])

