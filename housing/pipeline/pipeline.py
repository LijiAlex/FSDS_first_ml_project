from distutils.command.config import config
from housing.config.configuration import Configuration
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainArtifact
from housing.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainConfig
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.model_training import ModelTrainer
from housing.component.data_transformation import DataTransformation

import os, sys

class Pipeline:
    def __init__(self, config:Configuration = Configuration()) -> None:
        try:
            self.config = config
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(self.config.get_data_validation_config(), data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_data_transformation(self, data_validation_artifact, data_ingestion_artifact)->DataTransformationArtifact:
        try:
            data_transformation= DataTransformation(data_transformation_config=self.config.get_data_transformation_config(), 
            data_validation_artifact=data_validation_artifact, data_ingestion_artifact=data_ingestion_artifact)
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_model_trainer(self, data_transformation_artifact)-> ModelTrainArtifact:
        try:
            model_trainer = ModelTrainer(model_train_config=self.config.get_model_train_config(), 
            data_transformation_artifact=data_transformation_artifact)
            return model_trainer.initiate_model_training()
        except Exception as e:
            raise HousingException(e, sys) from e

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact, data_ingestion_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
        except Exception as e:
            raise HousingException(e, sys) from e
