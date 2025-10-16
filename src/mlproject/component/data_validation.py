import pandas as pd
from src.mlproject.entity.config_entity import DataValidationConfig
from src.mlproject import logging

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
    
    def get_column_validation(self) -> bool:
        """This validates column data types and assign status"""
        try:
            validation_status = None
            all_schema = self.config.all_schema.keys()
            df = pd.read_csv(self.config.unzip_data_dir)
            columns = list(df.columns)
            # Checks in column names match with the schema
            for col in columns:
                if col not in all_schema:
                    validation_status = False
                    logging.info(f"Sorry {col} NOT matching with schema")
                else:
                    validation_status = True
                    logging.info(f"Success! {col} matches with schema")
                with open(self.config.STATUS_FILE, 'w') as file:
                    file.write(f"Column validation status: {validation_status}")
        except Exception as e:
            raise e
            
