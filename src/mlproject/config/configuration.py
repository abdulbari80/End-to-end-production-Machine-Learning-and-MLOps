from src.mlproject.constant import *
from pathlib import Path
from src.mlproject.utils.common import read_yaml, create_directory
from src.mlproject.entity.config_entity import(DataIngestionConfig,
                                               DataTransformationConfig,
                                               ModelTrainerConfig,
                                               ModelEvaluationConfig
                                               )

class ConfigurationManager:
    """This configures path to access .yaml files and create/ access artifacts"""
    def __init__(
            self,
            config_path = Path("config/config.yaml")):
        
        self.config = read_yaml(config_path)

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
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directory([config.root_dir])
        data_transformation_config_obj = DataTransformationConfig(
            root_dir = config.root_dir,
            data_path=config.data_path,
            data_transform_obj_name=config.data_transform_obj_name,
            train_array=config.train_array,
            test_array=config.test_array)
        
        return data_transformation_config_obj
    
    def get_model_training_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        create_directory([config.root_dir])
        model_train_config_obj = ModelTrainerConfig(
            root_dir=config.root_dir,
            #model_name=config.model_name,
            train_array_path=config.train_array_path,
            test_array_path=config.test_array_path,
            grid_results=config.grid_results)
        
        return model_train_config_obj

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
    
        create_directory([config.root_dir])
        model_eval_config_obj = ModelEvaluationConfig(
            root_dir=config.root_dir,
            test_data_path=config.test_data_path,
            grid_result_path=config.grid_result_path,
            champ_model=config.champ_model,
            resuslt_metrics=config.resuslt_metrics,
            mlflow_uri="http://127.0.0.1:5000")
        
        return model_eval_config_obj