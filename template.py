import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = 'mlproject'

list_of_files = [
   ".github/workflows/.gitkeep",
   f"src/{project_name}/__init__.py",
   f"src/{project_name}/component/__init__.py",
   f"src/{project_name}/pipeline/__init__.py",
   f"src/{project_name}/utils/__init__.py",
   f"src/{project_name}/utils/common.py",
   f"src/{project_name}/config/__init__.py",
   f"src/{project_name}/config/configuration.py",
   f"src/{project_name}/constant/__init__.py",
   f"src/{project_name}/entity/__init__.py",
   f"src/{project_name}/entity/config_entity.py",
   "config/config.yaml",
   "notebook/eda.py",
   "templates/index.html",
   "app.py",
   "main.py",
   "params.yaml",
   "schema.yaml",
   "Dockerfile",
   ".dockerignore",
   "requirements.txt",
   "setup.py"
]

num_dir = 0
num_file = 0
for file in list_of_files:
    filepath = Path(file)
    dir, filename = os.path.split(filepath)

    if dir != '':
        try:
            os.makedirs(dir, exist_ok=True)
            logging.info(f"{dir} created for {filename}")
            num_dir += 1
        except FileExistsError:
            logging.info(f"{dir} already exists")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        try:
            with open(filepath, 'w') as f:
                pass
            logging.info(f"Empty {filename} created in directory {dir}")
            num_file += 1
        except FileExistsError:
            logging.info(f"{filepath} already exists")
logging.info(f"{num_dir} directories were created.")
logging.info(f"{num_file} files were created.")
