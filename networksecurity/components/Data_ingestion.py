import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
import os, sys
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from typing import List
import numpy as np
import pymongo
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class Dataingestion():
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def exporting_collection_as_dataframe(self): # Reading data from mongodb and converting to dataframe
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            mongo_client=MongoClient(MONGO_DB_URL)
            collection=mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_to_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set=train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logger.logging.info("Performed train test split on the dataframe")
            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logger.logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logger.logging.info("Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.exporting_collection_as_dataframe()
            dataframe=self.export_data_to_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            dataingestionartifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, 
                                                        test_file_path=self.data_ingestion_config.test_file_path)
            
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
