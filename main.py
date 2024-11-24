#from networksecurity.components import Data_ingestion
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.components.Data_ingestion import Dataingestion
import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=Dataingestion(dataingestionconfig)
        logger.logging.info("Starting data ingestion")
        
        dataingestionartifact=dataingestion.initiate_data_ingestion()
    except Exception as e:
        raise NetworkSecurityException(e, sys)