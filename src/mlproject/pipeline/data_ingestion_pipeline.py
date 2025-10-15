from src.mlproject.config.configuration import ConfigurationManager
from src.mlproject.component.data_ingestion import DataIngestion
from src.mlproject import logging

class DataIngestionPipeline:
    def __init__(self):
        pass

    def ingest_data(self):
        """This downloads and extract data and returns none"""
        try: 
            config_obj = ConfigurationManager()
            data_ingestion_config = config_obj.get_data_ingestion_config()
            data_ingestion_obj = DataIngestion(config=data_ingestion_config)
            data_ingestion_obj.download_file()
            data_ingestion_obj.extract_zip_file()
        except Exception as e:
            logging.exception(e)
            raise(e)

if __name__ == '__main__':
    print("This is a data ingestion pipeline\n \
          and not meant to be run independently")