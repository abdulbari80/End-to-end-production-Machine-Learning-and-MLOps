import os
import yaml
from box.exceptions import BoxValueError
from box.config_box import ConfigBox
from pathlib import Path
from typing import Any
from src.mlproject import logging


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
            
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("Sorry! yaml file is empty")
    except Exception as e:
        raise e
    

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

def get_size(path: Path) -> str:
    """This retrieves size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"