from housing.logger import logging
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from housing.constant import *
import sys, os 
from housing.util.util import read_yaml_file
import pandas as pd
import json

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

class DataValidation:
    def __init__( self, data_validation_config: DataValidationConfig, 
        data_ingestion_artifact:DataIngestionArtifact)-> None:
        try:
            logging.info(f"{'*'*20}Data Validation{'*'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            #schema_file_path = self.data_validation_config.schema_file_path, 
            #logging.info(f"Reading schema info from [{schema_file_path}]")
            #self.schema_info = read_yaml_file(file_path = schema_file_path)
            #logging.info(f"Schema Info:{self.schema_info}")
        except Exception as e:
            raise HousingException(e, sys) from e

    def is_train_test_exists(self):
        try:
            logging.info(f"Checking if train test file exists")
            is_train_file_exists = False
            is_test_file_exists = False

            is_train_file_exists = os.path.exists(self.data_ingestion_artifact.train_file_path)
            is_test_file_exists = os.path.exists(self.data_ingestion_artifact.test_file_path)

            logging.info(f"Train File [{self.data_ingestion_artifact.train_file_path}] exists? {is_train_file_exists}")
            logging.info(f"Test File[{self.data_ingestion_artifact.test_file_path}] exists? {is_test_file_exists}")

            if not (is_train_file_exists and is_test_file_exists):
                raise Exception(f"Train or Test file not available")
        except Exception as e:
            raise HousingException(e, sys) from e

    def validate_dataset_schema(self):
        try:
            validation_status = False
            # check how this can be done effectively
            # outline done in example.ipynb but need to find out the most effective method
            """
            Check
            1. Number of columns
            2. Column names
            3. Domain value of categorical data
            """
            return validation_status
        except Exception as e:
            raise HousingException(e, sys) from e

    def is_data_drift_found(self):
        try:
            data_drift = False
            report = self.save_data_drift_report()
            self.save_data_drift_report_page()
            # check how this can be done effectively - maybe take help of constants
            data_drift = report['data_drift']['data']['metrics']['dataset_drift']
            if not data_drift:
                raise Exception(f"Data drift detected")
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_train_test_dataframe(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise HousingException(e, sys) from e

    def save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_train_test_dataframe()
            # get the data drift report
            profile.calculate(train_df, test_df)
            # profile report in json format, profile.json returns string in json format, json.loads returns json as per input str
            report = json.loads(profile.json())
            logging.info(f"Report generated")
            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            logging.info(f"Writing report to [{report_file_path}]")
            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            logging.error("Exception Raised:", str(e))
            raise HousingException(e, sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs = [DataDriftTab()])
            train_df, test_df = self.get_train_test_dataframe()
            dashboard.calculate(train_df, test_df)
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)
            dashboard.save(report_page_file_path)
            logging.info(f"HTML report saved to [{report_page_file_path}]")
        except Exception as e:
            raise HousingException(e, sys) from e

    
    def detect_outlier(self):
        pass


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path = self.data_validation_config.schema_file_path, 
                report_file_path = self.data_validation_config.report_file_path, 
                report_page_file_path = self.data_validation_config.report_page_file_path, 
                is_validated = True,
                message = "Data Validation Performed Successfully"
            )
        except Exception as e:
            raise HousingException(e, sys) from e
        
