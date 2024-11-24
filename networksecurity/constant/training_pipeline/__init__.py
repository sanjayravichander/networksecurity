import os
import sys
import numpy as np
import pandas as pd

# Defining constant variables for training pipeline
TARGET_COLUMN= "phising"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "PhisingData.csv"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

# Defining the DATA_INGESTION_CONFIGURATION
DATA_INGESTION_COLLECTION_NAME: str = "Network_Data"
DATA_INGESTION_DATABASE_NAME: str = "SANJAYR"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
