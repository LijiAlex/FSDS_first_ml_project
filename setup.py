from setuptools import setup, find_packages
from typing import List

# Declaring variables for setup function
PROJECT_NAME = "housing-predictor"
VERSION = "0.0.2"
AUTHOR = "Liji Alex"
DESCRIPTION = "Housing prediction ml end to end project"
PACKAGES = ["housing"]
REQUIREMENT_FILE_NAME = "requirements.txt"

def get_requirements_list()->List[str]:
    """
    Description: This function is going to return list of libraries 
     mentioned in requirements.txt

    Returns:
        List[str]: A list containing the name of libraries in requirements.txt
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")



setup(
    name = PROJECT_NAME,
    version = VERSION,
    author = AUTHOR,
    description = DESCRIPTION,
    # packages = PACKAGES,
    packages = find_packages(),
    install_requires = get_requirements_list()
)
