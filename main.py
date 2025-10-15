from src.mlproject.config.configuration import ConfigurationManager
from src.mlproject.component.data_ingestion import DataIngestion
from src.mlproject import logging

class DataTransfer:
    def __init__(self):
        pass

    def get_data(self):
        config_obj = ConfigurationManager()
        data_ingestion_config = config_obj.get_data_ingestion_config()
        data_ingestion_obj = DataIngestion(config=data_ingestion_config)
        return data_ingestion_obj

def main():
    data_obj = DataTransfer().get_data()
    logging.info("Data download starts >>>>>")
    data_obj.download_file()
    logging.info(">>>>> Data download fininshed and extraction starts! >>>>>")
    data_obj.extract_zip_file()
    logging.info(">>>>> Data extracted!")

if __name__ == '__main__':
    main()