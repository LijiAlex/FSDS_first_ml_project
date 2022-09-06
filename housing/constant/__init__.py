import os
from datetime import datetime

ROOT_DIR = os.getcwd() # to get current working directory

CONFIG_DIR = 'config'
CONFIG_FILE = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_DATASET_URL = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR = "raw_data_dir"
DATA_INGESTION_TGZ_DIR = "tgz_download_dir"
DATA_INGESTION_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR = "ingested_train_dir"
DATA_INGESTION_TEST_DIR = "ingested_test_dir"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME = "schema_file_name"

DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
ADD_BEDROOM_PER_ROOM_KEY = "add_bedroom_per_room"
TRANFORMED_DIR = "transformed_dir"
TRANSFORMED_TRAIN_DIR = "transformed_train_dir"
TRANSFORMED_TEST_DIR = "transformed_test_dir"
PREPROCESSING_DIR = "preprocessing_dir"
PREPROCESSED_OBJECT_FILE_NAME = "preprocessed_object_file_name"

MODEL_TRAINER_CONFIG_INFO = "model_trainer_config"
TRAINED_MODEL_DIR = "trained_model"
TRIANED_MODEL_FILENAME = "model_file_name"
BASE_ACCURACY = "base_accuracy"

MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_DIR = "model_evaluation"
MODEL_EVALUATION_FILE_NAME = "model_evaluation_file_name"

MODEL_PUSH_CONFIG_INFO_KEY = "model_pusher_config"
MODEL_EXPORT_DIR = "model_export_dir"