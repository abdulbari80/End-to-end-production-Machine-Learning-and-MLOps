from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

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
    #model_name: str
    train_array_path: Path
    test_array_path: Path
    grid_results: str

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    grid_result_path: Path
    champ_model: str
    resuslt_metrics: str
    mlflow_uri: Path


