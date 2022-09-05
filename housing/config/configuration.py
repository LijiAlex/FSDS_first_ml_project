# use entity/config_entity.py and input from config/config.yaml
import sys
from housing.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig
from housing.entity.config_entity import ModelEvaluationConfig, ModelPushConfig, ModelTrainConfig, TrainingPipeLineConfig
from housing.constant import *
from housing.util.util import read_yaml_file
from housing.exception import HousingException
from housing.logger import logging

class Configuration:

    def __init__(self, 
    config_file_path:str = CONFIG_FILE_PATH, 
    current_time_stamp:str = CURRENT_TIME_STAMP
    ) -> None:
        self.config_info = read_yaml_file(file_path = config_file_path)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = current_time_stamp

    def get_data_ingestion_config(self)->DataIngestionConfig:
        pass

    def get_data_validation_config(self)->DataValidationConfig:
        pass    

    def get_data_transformation_config(self)->DataTransformationConfig:
        pass

    def get_model_train_config(self)->ModelTrainConfig:
        pass

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        pass

    def get_mode_push_config(self)->ModelPushConfig:
        pass

    def get_training_pipeline_config(self)->TrainingPipeLineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            TRAINING_PIPELINE_NAME_KEY, 
            TRAINING_PIPELINE_ARTIFACT_DIR_KEY
            )
            # Assigning values to named tuple
            # Here training_pipeline_config like an object of the tuple
            
            training_pipeline_config = TrainingPipeLineConfig(artifact_dir = artifact_dir) 
            logging.info(f"TrainingPipelineConfig: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e, sys) from e