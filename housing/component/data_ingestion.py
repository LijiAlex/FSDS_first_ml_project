from cmath import inf
from housing.entity.config_entity import DataIngestionConfig
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
import sys, os
import tarfile
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self, data_ingetion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'*'*20}Data Ingestion Log{'*'*20}")
            self.data_ingestion_config = data_ingetion_config
        except Exception as e:
            raise HousingException(e, sys) from e

    def download_housing_data(self)->str:
        try:
            # remote url to download data
            download_url = self.data_ingestion_config.dataset_download_url
            # folder location to download file
            tqz_download_dir = self.data_ingestion_config.tqz_download_dir
            # create folder
            os.makedirs(tqz_download_dir, exist_ok=True)
            # get the file name
            housing_file_name = os.path.basename(download_url)
            # complete path to download
            tgz_file_path = os.path.join(tqz_download_dir, housing_file_name)
            # tgz_file_path = r"D:\Ineuron\Projects\HousingPrediction\FSDS_first_ml_project\housing\artifact\data_ingestion\2022-09-12-12-11-06\tgz_data\housing.tgz"
            logging.info(f"Downloading file [{housing_file_name}] from [{download_url}] into [{tgz_file_path}]")
            # get file from url
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f"Download completed. File [{tgz_file_path}] downloaded successfully")
            return tgz_file_path
        except Exception as e:
            raise HousingException(e, sys) from e


    def extract_tgz_file(self, tgz_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            # create folder
            os.makedirs(raw_data_dir, exist_ok=True)
            # extract the tgz file
            logging.info(f"Extracting [{tgz_file_path}] into [{raw_data_dir}]")
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(raw_data_dir)
            logging.info(f"Extraction completed successfully")
        except Exception as e:
            raise HousingException(e, sys) from e

    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            # gives the folder where raw data is present
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            # get raw data file name
            raw_data_file = os.listdir(raw_data_dir)[0]
            # path to raw data file
            housing_file_path = os.path.join(raw_data_dir, raw_data_file)
            logging.info(f"Reading csv [{raw_data_file}] from [{housing_file_path}]")
            # get data frame
            housing_data_frame = pd.read_csv(housing_file_path)
            

            # stratified split on median_income(column in data frame)
            housing_data_frame["income_cat"] = pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            raw_data_file)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        raw_data_file)

            # create folders and save data
            if strat_train_set is not None:
                logging.info(f"Exporting training data [{train_file_path}]")
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path, index=False)
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting training data [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path, 
                test_file_path, 
                is_ingested = True, 
                message = "Data ingested successfully")
            logging.info(f"DataIngestionArtifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise HousingException(e, sys) from e

    def __del__(self):
        """
        Acts as destructor. Called before all references to the class object are deleted.
        """
        logging.info(f"{'*' *25} Data Ingestion log completed {'*' *25}")


