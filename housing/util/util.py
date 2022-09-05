import yaml
import os
import sys
from housing.exception import HousingException

print(os.listdir("."))
config_file_path = os.path.join("..\config","config.yaml")

def read_yaml_file(file_path:str)->dict:
    """
    Reads YAML file and returns contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e

