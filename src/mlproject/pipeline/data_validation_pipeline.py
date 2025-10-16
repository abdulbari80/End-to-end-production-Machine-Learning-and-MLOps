from src.mlproject.config.configuration import ConfigurationManager
from src.mlproject.component.data_validation import DataValidation

class DataValidationPipeline:
    def __init__(self):
        pass

    def validate_column(self):
        data_valid_config_obj = ConfigurationManager().get_data_validation_config()
        data_validation_obj = DataValidation(data_valid_config_obj)
        data_validation_obj.get_column_validation()

if __name__ == '__main__':
    print("This validates data type in columns\n \
          and not meant to be run on its own")
