from src.mlproject.constant import *
from pathlib import Path
from src.mlproject.utils.common import read_yaml, create_directory
from src.mlproject.entity.config_entity import(DataIngestionConfig)

class ConfigurationManager:
    def __init__(
            self,
            config_path = CONFIG_FILE_PATH,
            params_path = SCHEMA_FILE_PATH,
            schema_path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)
        self.schema = read_yaml(schema_path)

        create_directory([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directory([config.root_dir])
        data_ingestion_config_obj = DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir)
        
        return data_ingestion_config_obj