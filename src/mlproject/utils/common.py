import os
import yaml
import json
import joblib
from box.exceptions import BoxValueError
from box.config_box import ConfigBox
from ensure import ensure_annotations
from pathlib import Path
from typing import Any
from src.mlproject import logging


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """This reads and returns yaml file

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"success! yaml file: {path_to_yaml} loaded")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Sorry! yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directory(path_to_directory: list, verbose=True):
    """This creates a list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created.\
                                     Defaults to False.
    Returns: 
        None
    """
    for path in path_to_directory:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logging.info(f"Success! created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """This saves json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    Returns: 
        None
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"Success! A json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """This loads json data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logging.info(f"Success! loaded a json file from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """This saves binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    Returns: 
        None
    """
    joblib.dump(value=data, filename=path)
    logging.info(f"A binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """This loads binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logging.info(f"Success! binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """This retrieves size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"