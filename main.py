from src.mlproject.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.mlproject.pipeline.data_validation_pipeline import DataValidationPipeline
from src.mlproject import logging

STEP_1 = "Data Ingestion"
STEP_2 = "Data Validation"

def main():
    """
    # Triggers data ingestion
    logging.info(f"{STEP_1} starts >>>>>")
    DataIngestionPipeline().ingest_data()
    logging.info(">>>>> f{STEP_1} finished!")
"""
    # Triggers data vaidation
    logging.info(f"{STEP_2} starts >>>>>")
    DataValidationPipeline().validate_column()
    logging.info(">>>>> f{STEP_1} finished!")
    
if __name__ == '__main__':
    main()