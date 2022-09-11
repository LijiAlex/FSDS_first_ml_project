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
        try:
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_artifact_dir = os.path.join(self.get_training_pipeline_config().artifact_dir, DATA_INGESTION_ARTIFACT_DIR, self.time_stamp) 
            download_url = data_ingestion_config_info[DATA_INGESTION_DATASET_URL]
            tqz_download_dir = os.path.join(data_ingestion_artifact_dir,data_ingestion_config_info[DATA_INGESTION_TGZ_DIR])
            raw_data = os.path.join(data_ingestion_artifact_dir,data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR])
            injested_data_dir = os.path.join(data_ingestion_artifact_dir, data_ingestion_config_info[DATA_INGESTION_DIR_NAME_KEY])
            train_dir = os.path.join(injested_data_dir, data_ingestion_config_info[DATA_INGESTION_TRAIN_DIR])
            test_dir = os.path.join(injested_data_dir, data_ingestion_config_info[DATA_INGESTION_TEST_DIR])

            data_ingestion_config_info = DataIngestionConfig(
                dataset_download_url=download_url,
                tqz_download_dir=tqz_download_dir,
                raw_data_dir=raw_data,
                ingested_train_dir=train_dir,
                ingested_test_dir=test_dir
                )
            logging.info(f"DataIngestionConfig: {data_ingestion_config_info}")
            return data_ingestion_config_info

        except Exception as e:
            raise HousingException(e, sys) from e

    def get_data_validation_config(self)->DataValidationConfig:
        try:
            data_validation_config_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            data_validation_schema_file_name = data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME]
            file_path = os.path.join(ROOT_DIR, data_validation_config_info[DATA_VALIDATION_SCHEMA_DIR], data_validation_schema_file_name)
            data_validation_artifact_dir = os.path.join(self.get_training_pipeline_config().artifact_dir, DATA_VALIDATION_ARTIFACT_DIR, self.time_stamp)
            report_file_name = data_validation_config_info[DATA_VALIDATION_REPORT_NAME]
            report_file_path = os.path.join(data_validation_artifact_dir, report_file_name)
            report_page_file_name = data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_NAME]
            report_page_file_path = os.path.join(data_validation_artifact_dir, report_page_file_name)
            data_validation_config_info = DataValidationConfig(
                schema_file_path = file_path, 
                report_file_path = report_file_path, 
                report_page_file_path = report_page_file_path) 
            logging.info(f"DataValidationConfig: {data_validation_config_info}")
            return data_validation_config_info
        except Exception as e:
            raise HousingException(e, sys)  from e  

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            data_transformation_config_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            add_bedroom_per_room = data_transformation_config_info[ADD_BEDROOM_PER_ROOM_KEY]
            data_transformation_artifact_dir = os.path.join(self.get_training_pipeline_config().artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR, self.time_stamp) 
            transformed_dir = os.path.join(data_transformation_artifact_dir, TRANFORMED_DIR)
            transformed_train_dir = os.path.join(transformed_dir, data_transformation_config_info[TRANSFORMED_TRAIN_DIR])
            transformed_test_dir = os.path.join(transformed_dir, data_transformation_config_info[TRANSFORMED_TEST_DIR])
            preprocessing_dir = os.path.join(data_transformation_artifact_dir, PREPROCESSING_DIR)
            preprocessed_file_name = os.path.join(preprocessing_dir, data_transformation_config_info[PREPROCESSED_OBJECT_FILE_NAME] )

            data_transformation_config_info = DataTransformationConfig(
                add_bedroom_per_room = add_bedroom_per_room, 
                transformed_train_dir = transformed_train_dir, 
                transformed_test_dir = transformed_test_dir, 
                preprocessed_object_file_path = preprocessed_file_name
                )
            logging.info(f"DataTransformationConfig: {data_transformation_config_info}")
            return data_transformation_config_info
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_model_train_config(self)->ModelTrainConfig:
        try:
            model_train_config_info = self.config_info[MODEL_TRAINER_CONFIG_INFO]
            trained_model_dir = os.path.join(self.get_training_pipeline_config().artifact_dir, TRAINED_MODEL_DIR, self.time_stamp)
            trained_model_file_path = os.path.join(trained_model_dir, model_train_config_info[TRIANED_MODEL_FILENAME])
            base_accuracy = model_train_config_info[BASE_ACCURACY]
            model_train_config_info = ModelTrainConfig(
                trained_model_file_path = trained_model_file_path, 
                base_accuracy = base_accuracy
                )
            logging.info(f"ModelTrainingConfig: {model_train_config_info}")
            return model_train_config_info
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_model_evaluation_config(self)->ModelEvaluationConfig:
        model_evaluation_config_info = self.config_info[MODEL_EVALUATION_CONFIG_KEY]
        model_evaluation_file_name = model_evaluation_config_info[MODEL_EVALUATION_FILE_NAME]
        model_evaluation_file_path = os.path.join(MODEL_EVALUATION_DIR, model_evaluation_file_name)
        try:
            model_evaluation_config_info = ModelEvaluationConfig(
                model_evaluation_file_path = model_evaluation_file_path, 
                time_stamp = self.time_stamp
            )
            logging.info(f"ModelEvaluationConfig: {model_evaluation_config_info}")
            return model_evaluation_config_info
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_model_push_config(self)->ModelPushConfig:
        try:
            export_dir = os.path.join(self.get_training_pipeline_config().artifact_dir, MODEL_EXPORT_DIR, self.time_stamp)
            model_push_config_info = ModelPushConfig(
                export_dir_path = export_dir
                )
            logging.info(f"ModelPushConfig: {model_push_config_info}")
            return model_push_config_info
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_training_pipeline_config(self)->TrainingPipeLineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY], 
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )
            # Assigning values to named tuple
            # Here training_pipeline_config like an object of the tuple
            
            training_pipeline_config = TrainingPipeLineConfig(artifact_dir = artifact_dir) 
            logging.info(f"TrainingPipelineConfig: {training_pipeline_config}")
            return training_pipeline_config
        except Exception as e:
            raise HousingException(e, sys) from e