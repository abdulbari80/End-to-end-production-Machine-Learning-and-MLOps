from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    unzip_data_dir: Path
    all_schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    data_transform_obj_name: str
    train_array: str
    test_array: str

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    model_name: str
    train_array_path: Path
    test_array_path: Path
    grid_result: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    grid_result_path: Path
    model_name: str
    metric_file_name: str
    mlflow_uri: Path

@dataclass(frozen=True)
class UnitTestConfig:
    data_transform_obj_path: Path
    train_arrary_path: Path
    test_array_path: Path
    training_result_path: Path
    prod_model_path: Path