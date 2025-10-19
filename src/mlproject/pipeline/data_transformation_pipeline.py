from src.mlproject.config.configuration import ConfigurationManager
from src.mlproject.component.data_transformation import DataTransformation
from src.mlproject import logging

class DataTransformationPipeline:
    def __init__(self):
        pass
    def transform_data(self):
        config_obj = ConfigurationManager()
        data_transform_config_obj = config_obj.get_data_transformation_config()
        logging.info("Configuration manager is instantiated")
        data_transorm_obj = DataTransformation(config=data_transform_config_obj)
        data_transorm_obj.initiate_data_transformation(test_size=0.25)
        logging.info("Data transformed and stored in the artifacts with the pipeline object")

if __name__ == "__main__":
    "This module splits dataset into train and test sets"

